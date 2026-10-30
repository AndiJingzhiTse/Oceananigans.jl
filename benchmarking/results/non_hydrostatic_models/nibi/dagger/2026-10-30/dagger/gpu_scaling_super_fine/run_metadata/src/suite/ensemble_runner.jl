# Four independent models; shared physics and validation stay in worker.jl.
using Distributed, JSON
include(joinpath(@__DIR__, "ensemble_member.jl"))

settings = JSON.parsefile(only(ARGS))
directory = settings["directory"]
cd(directory)
mode = settings["execution_mode"]
mode in ("baseline", "dagger") || error("Unknown ensemble dispatcher")
ENV["CUDA_VISIBLE_DEVICES"] = "" # The coordinator does not own a model/GPU.
workers_for_models = Int[]
setup_start = time_ns()
try
    for member in settings["members"]
        environment = Pair{String, String}[String(k) => String(v) for (k, v) in member["environment"]]
        push!(environment, "CUDA_VISIBLE_DEVICES" => member["gpu_uuid"])
        process = only(addprocs(1; exeflags=`--threads=1 --project=$(settings["project"])`,
                                env=environment))
        push!(workers_for_models, process)
    end
    @sync for process in workers_for_models
        @async remotecall_wait(Base.include, process, Main, joinpath(@__DIR__, "ensemble_member.jl"))
    end
    if mode == "dagger"
        # Initialize workers before importing Dagger, as required by Distributed.
        @eval using Dagger
        @sync for process in workers_for_models
            @async remotecall_wait(Core.eval, process, Main, :(using Dagger))
        end
        @eval function submit_dagger_member(process, member, worker_file, events, gate)
            return Dagger.@spawn scope=Dagger.scope(worker=process, thread=1) ensemble_member(member, worker_file, events, gate)
        end
    end
    events = RemoteChannel(() -> Channel{Any}(64))
    gates = [RemoteChannel(() -> Channel{Bool}(1)) for _ in workers_for_models]
    setup_seconds = (time_ns() - setup_start) / 1e9
    dispatch_start = time_ns()
    tasks = Any[]
    for (index, process) in enumerate(workers_for_models)
        member, gate = settings["members"][index], gates[index]
        worker_file = settings["worker_file"]
        if mode == "dagger"
            # Submit all four complete simulations before fetching any task.
            task = Base.invokelatest(submit_dagger_member, process, member, worker_file, events, gate)
            push!(tasks, task)
        else
            push!(tasks, remotecall(ensemble_member, process, member, worker_file, events, gate))
        end
    end
    event_records = Any[]
    ready = Set{Int}()
    while length(ready) < length(tasks)
        event = take!(events)
        push!(event_records, event)
        event[1] == "failed" && error("Ensemble member $(event[2]) failed: $(event[3])")
        event[1] == "ready" && push!(ready, event[2])
    end
    println("ENSEMBLE_ALL_READY mode=$mode members=$(length(ready))")
    flush(stdout)
    timed_start_epoch = time()
    timed_start = time_ns()
    for gate in gates
        put!(gate, true)
    end
    timed = Set{Int}()
    while length(timed) < length(tasks)
        event = take!(events)
        push!(event_records, event)
        event[1] == "failed" && error("Ensemble member $(event[2]) failed: $(event[3])")
        event[1] == "timed" && push!(timed, event[2])
    end
    timed_seconds = (time_ns() - timed_start) / 1e9
    println("ENSEMBLE_TIMED mode=$mode seconds=$timed_seconds")
    flush(stdout)
    completed = fetch.(tasks)
    dispatch_seconds = (time_ns() - dispatch_start) / 1e9
    entries, layouts = Any[], Any[]
    for member in settings["members"]
        entry = only(JSON.parsefile(joinpath(member["directory"], "results.json")))
        entry["ensemble_member"] = member["id"]
        push!(entries, entry)
        layout = only(JSON.parsefile(joinpath(member["directory"], "layout.json")))
        layout["ensemble_member"] = member["id"]
        push!(layouts, layout)
    end
    for (name, value) in (("results.json", entries), ("layout.json", layouts),
                         ("ensemble.json", Dict("execution_mode" => mode,
                             "setup_seconds" => setup_seconds,
                             "dispatch_seconds" => dispatch_seconds,
                             "timed_seconds" => timed_seconds,
                             "timed_start_epoch" => timed_start_epoch,
                             "events" => event_records, "completed" => completed,
                             "julia_version" => string(VERSION),
                             "dagger_version" => mode == "dagger" ? string(pkgversion(Dagger)) : nothing)))
        open(joinpath(directory, name), "w") do io
            JSON.json(io, value; pretty=true)
        end
    end
    println("PASS: four validated independent GPU simulations; mode=$mode")
finally
    isempty(workers_for_models) || rmprocs(workers_for_models; waitfor=30)
end
