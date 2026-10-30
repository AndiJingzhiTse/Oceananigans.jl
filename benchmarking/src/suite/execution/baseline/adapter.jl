module BenchmarkAdapter

function execute_window!(window!, model, Δt, steps, context)
    window!(model, Δt, steps, context.is_gpu, context.device)
    return nothing
end

metadata() = Dict("package_versions" => Dict{String, String}())

end
