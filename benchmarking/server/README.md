# Server benchmark plans

Each server has `config.json` (resources/software), `series.json` (exact workloads)
and a README. The same series file supplies HydrostaticFreeSurfaceModel and
NonhydrostaticModel, each with baseline and Dagger execution: four available
combinations per server. The shared workflow supports any subset,
including all four, on either local or Slurm backends. See the
[workflow requirements](../requirements.md) for selections and the replaceable
Dagger integration contract.
The baseline is direct execution of these workloads. The default Dagger adapter
uses the existing whole-function wrapper and can be replaced. Use the same
`benchmark_suite.py --study ... --execute` command on local and Slurm servers;
server configuration selects the backend. Implementation validation does not
launch the full production benchmark series.

| Server | Configuration | Series | Cases per model/variant |
|---|---|---|---:|
| [Rondeau](rondeau/README.md) | [config.json](rondeau/config.json) | [series.json](rondeau/series.json) | 16 |
| [Nibi](nibi/README.md) | [config.json](nibi/config.json) | [series.json](nibi/series.json) | 30 |
| [Rorqual](rorqual/README.md) | [config.json](rorqual/config.json) | [series.json](rorqual/series.json) | 30 |
| [Fir](fir/README.md) | [config.json](fir/config.json) | [series.json](fir/series.json) | 30 |

Rondeau has six series and excludes partition benchmarks. The three clusters
retain seven series including their fine-grid partition comparisons.
No extra boundary cases, CPU series, ensembles or resolution extensions are
appended. Lower capacity produces explicit RESOURCE_LIMIT outcomes.

`config.json` resolves `series_file` relative to its own folder. A study embeds
the resolved definitions in `suite.json` and `run_metadata/series.json`.
Series names and kinds are checked; GPU counts and partitions must be positive
and unique. Scaling uses balanced horizontal partitions; explicit partition
and weak-scaling cases retain their listed decompositions.

Results stay under `../results/<model_family>/<server>/baseline/` and `dagger/`.
Comparisons belong in the enclosing model/server folder and match equivalent
cases within that model. Historical result locations remain unchanged.
See [the main instructions](../README.md) for the result tree, timing protocol,
planning commands and the replaceable Dagger integration.

[Andi-5070ti](Andi-5070ti/config.json) retains its existing local configuration;
no new workload specification was requested for that machine. Legacy series
remain available to inspect existing studies. New plans for the four servers
above must select from their own configured GPU series.
