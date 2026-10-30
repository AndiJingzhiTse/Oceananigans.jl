using Distributed, JSON, Dates

function ensemble_member(member, worker_file, events, gate)
    id, directory = member["id"], member["directory"]
    mkpath(directory)
    status = 1
    return open(joinpath(directory, "job.out"), "w") do log
        return redirect_stdio(stdout=log, stderr=log) do
            try
                # One host core and one visible GPU per independent simulation.
                cpu = member["cpu"]
                mask = zeros(UInt8, max(128, cld(cpu + 1, 8)))
                mask[cpu ÷ 8 + 1] = UInt8(1) << (cpu % 8)
                ccall(:sched_setaffinity, Cint, (Cint, Csize_t, Ptr{UInt8}), 0, length(mask), mask) == 0 || error("Cannot pin ensemble computation thread")
                simulation = Module(gensym(:EnsembleSimulation))
                on_ready = () -> begin
                    put!(events, ("ready", id, time()))
                    take!(gate)
                    put!(events, ("timing_started", id, time()))
                end
                on_timed = () -> put!(events, ("timed", id, time()))
                Core.eval(simulation, :(const BENCHMARK_CASE_DIR = $(directory)))
                Core.eval(simulation, :(const BENCHMARK_ON_READY = $(QuoteNode(on_ready))))
                Core.eval(simulation, :(const BENCHMARK_ON_TIMED = $(QuoteNode(on_timed))))
                Base.include(simulation, worker_file)
                status = 0
                return Dict("id" => id, "worker" => myid(), "pid" => getpid())
            catch exception
                showerror(stderr, exception, catch_backtrace())
                put!(events, ("failed", id, sprint(showerror, exception)))
                rethrow()
            finally
                write(joinpath(directory, "exit_code.txt"), string(status, '\n'))
                write(joinpath(directory, "finished.txt"), string(now(UTC), '\n'))
            end
        end
    end
end
