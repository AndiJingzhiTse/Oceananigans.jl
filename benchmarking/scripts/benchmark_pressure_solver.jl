length(ARGS) in (2, 3) || error("Usage: benchmark_pressure_solver.jl CONFIG.toml OUTPUT_DIRECTORY [native]")
for variable in ("TMPDIR", "TMP", "TEMP", "OMPI_MCA_orte_tmpdir_base")
    directory = get(ENV, variable, "")
    isdir(directory) || error("Set $variable to an existing data-filesystem directory")
    resolved = realpath(directory)
    any(root -> resolved == root || startswith(resolved, root * "/"), ("/tmp", "/var/tmp")) &&
        error("$variable must not resolve into a system temporary directory")
end
include(joinpath(@__DIR__, "../src/pressure_solver_benchmark.jl"))
backend = Symbol(get(ARGS, 3, "native"))
PressureSolverBenchmark.run_case(ARGS[1], ARGS[2]; backend)
