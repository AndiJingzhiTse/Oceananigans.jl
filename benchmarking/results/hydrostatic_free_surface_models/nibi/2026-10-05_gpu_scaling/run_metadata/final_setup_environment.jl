using Pkg
using TOML

environment = abspath(only(ARGS))
benchmark_dir = realpath(joinpath(@__DIR__, "..", ".."))
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

# MPIPreferences and OpenMPI_jll must both point to the module's MPI runtime.
mpi_prefix = ENV["EBROOTOPENMPI"]
preferences = Dict(
    "MPIPreferences" => Dict("_format" => "1.0", "binary" => "system", "abi" => "OpenMPI",
                             "libmpi" => joinpath(mpi_prefix, "lib", "libmpi"),
                             "mpiexec" => "mpiexec", "preloads" => String[], "cclibs" => String[]),
    "OpenMPI_jll" => Dict("libmpi_path" => joinpath(mpi_prefix, "lib", "libmpi.so")))
open(joinpath(environment, "LocalPreferences.toml"), "w") do io
    TOML.print(io, preferences; sorted=true)
end
