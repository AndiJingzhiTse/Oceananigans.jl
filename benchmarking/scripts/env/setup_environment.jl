using Pkg
using TOML

isempty(ARGS) && error("Usage: setup_environment.jl ENVIRONMENT [--adapter DIRECTORY]")
length(ARGS) in (1, 3) || error("Expected ENVIRONMENT [--adapter DIRECTORY]")
length(ARGS) == 3 && ARGS[2] != "--adapter" && error("Expected --adapter DIRECTORY")
environment = abspath(first(ARGS))
benchmark_dir = dirname(dirname(@__DIR__))
repository = dirname(benchmark_dir)
mkpath(environment)

# A separate environment keeps cluster preferences and dependencies out of the
# package's Project.toml. Julia 1.10 needs Pkg.develop rather than [sources].
project = Dict("deps" => copy(TOML.parsefile(joinpath(benchmark_dir, "Project.toml"))["deps"]),
               "compat" => copy(TOML.parsefile(joinpath(benchmark_dir, "Project.toml"))["compat"]))
project["deps"]["OpenMPI_jll"] = "fe0851c0-eecd-5654-98d4-656369965a5c"
project["compat"]["OpenMPI_jll"] = "4.1"
open(joinpath(environment, "Project.toml"), "w") do io
    TOML.print(io, project; sorted=true)
end
Pkg.activate(environment)
Pkg.develop([PackageSpec(path=repository), PackageSpec(path=benchmark_dir)])
Pkg.instantiate()

# Execution dependencies belong to the selected adapter, not the root package.
if length(ARGS) == 3
    @eval using JSON
    manifest = JSON.parsefile(joinpath(abspath(ARGS[3]), "adapter.json"))
    dependencies = get(manifest, "dependencies", Dict())
    specs = [PackageSpec(name=name, uuid=dependency["uuid"], version=dependency["version"])
             for (name, dependency) in dependencies]
    isempty(specs) || Pkg.add(specs)
end

# MPIPreferences and OpenMPI_jll must both point to the module's MPI runtime.
mpi_prefix = get(ENV, "EBROOTOPENMPI", "")
isempty(mpi_prefix) && exit() # Local installs retain their existing/default MPI preferences.
preferences = Dict(
    "MPIPreferences" => Dict("_format" => "1.0", "binary" => "system", "abi" => "OpenMPI",
                             "libmpi" => joinpath(mpi_prefix, "lib", "libmpi"),
                             "mpiexec" => "mpiexec", "preloads" => String[], "cclibs" => String[]),
    "OpenMPI_jll" => Dict("libmpi_path" => joinpath(mpi_prefix, "lib", "libmpi.so")))
open(joinpath(environment, "LocalPreferences.toml"), "w") do io
    TOML.print(io, preferences; sorted=true)
end
