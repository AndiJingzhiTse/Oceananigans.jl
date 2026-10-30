module BenchmarkAdapter

using Dagger

function execute_window!(window!, model, Δt, steps, context)
    isempty(context.options) || error("The whole-function adapter accepts no options")
    task = Dagger.@spawn scope=Dagger.scope(worker=1, thread=1) window!(model, Δt, steps, context.is_gpu, context.device)
    fetch(task)
    return nothing
end

metadata() = Dict("package_versions" => Dict("Dagger" => string(pkgversion(Dagger))))

end
