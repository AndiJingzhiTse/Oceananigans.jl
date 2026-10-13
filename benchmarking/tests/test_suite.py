"""Test plans, launch commands, validation and restart behavior without production jobs."""
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import benchmark_suite as runner
from suite import plan, report


def fixture(folder, config):
    folder.mkdir(parents=True, exist_ok=True)
    entries, layout = [], []
    for rank in range(config['ranks']):
        py = config['partition'][1]
        shape = [config['x_sizes'][rank // py], config['y_sizes'][rank % py], config['global_resolution'][2]]
        entries.append(dict(rank=rank, grid_size=shape, float_type='Float64', configuration=config,
                            metadata={'num_threads': 1}, finite_state=True, retained_free_surface_substeps=21,
                            window_seconds=[10, 11, 12, 13, 14], time_per_step_seconds=1.0,
                            time_per_step_median_seconds=1.2, time_per_step_max_seconds=1.4))
        if config.get('model_type') == 'NonhydrostaticModel':
            entries[-1].update(model_type='NonhydrostaticModel', free_surface='RigidLid',
                               pressure_solver='ConjugateGradientPoissonSolver',
                               pressure_solver_converged=True, retained_free_surface_substeps=None)
        layout.append(dict(rank=rank, hostname='node', affinity=str(rank), threads=1,
                           physical_core=f'0:{rank}', gpu_uuid=f'GPU-{rank}' if config['device'] == 'GPU' else None))
    (folder / 'results.json').write_text(json.dumps(entries))
    (folder / 'layout.json').write_text(json.dumps(layout))
    (folder / 'finished.txt').write_text('finished')
    (folder / 'exit_code.txt').write_text('0')
    return entries


class SuiteTests(unittest.TestCase):
    def server(self, cpu=192, gpu=8):
        return dict(max_cpu_cores=cpu, max_gpus=gpu)

    def test_nonhydrostatic_plan_preserves_workloads_and_records_supported_methods(self):
        server = self.server(gpu=64)
        hydro = plan.build_plan(server)
        nonhydro = plan.build_plan(dict(server, model_type='NonhydrostaticModel'))
        for h, n in zip(hydro, nonhydro):
            self.assertEqual((h['id'], h['partition'], h['state']), (n['id'], n['partition'], n['state']))
            if 'configuration' not in h:
                continue
            cfg = n['configuration']
            for key in ('global_resolution', 'x_sizes', 'y_sizes', 'dt', 'samples', 'time_steps'):
                self.assertEqual(h['configuration'][key], cfg[key])
            self.assertEqual(cfg['model_type'], 'NonhydrostaticModel')
            self.assertEqual(cfg['timestepper'], 'RungeKutta3')
            self.assertEqual(cfg['free_surface'], 'RigidLid')
            self.assertEqual(cfg['momentum_advection'], 'WENO7')
            self.assertEqual(cfg['closure'], 'ScalarDiffusivity')
            self.assertIsNone(cfg['free_surface_substeps'])
            self.assertEqual(cfg['pressure_max_iterations'], math.prod(cfg['global_resolution']))

    def test_nonhydrostatic_validation_requires_model_and_pressure_convergence(self):
        cfg = plan.configuration('cpu_mpi_scaling_super_fine', 2,
                                 global_resolution=[72,36,8], model_type='NonhydrostaticModel')
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)/'case'
            entries = fixture(folder, cfg)
            self.assertEqual(report.validate(folder,cfg)['retained_substeps'], [])
            entries[0]['pressure_solver_converged'] = False
            (folder/'results.json').write_text(json.dumps(entries))
            with self.assertRaisesRegex(ValueError, 'unconverged pressure solver'):
                report.validate(folder,cfg)
            entries[0]['pressure_solver_converged'] = True
            entries[0]['model_type'] = 'HydrostaticFreeSurfaceModel'
            (folder/'results.json').write_text(json.dumps(entries))
            with self.assertRaisesRegex(ValueError, 'Unexpected nonhydrostatic model'):
                report.validate(folder,cfg)

    def test_model_comparison_requires_validated_matching_workloads_and_protocol(self):
        series = 'gpu_scaling_super_fine'
        h = plan.build_plan(self.server(gpu=1),(series,))[0]
        n = plan.build_plan(dict(self.server(gpu=1),model_type='NonhydrostaticModel'),(series,))[0]
        h.update(state='COMPLETED',measurement=dict(fastest=1,median=1.2))
        n.update(state='COMPLETED',measurement=dict(fastest=2,median=2.4))
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);reference=root/'hydro';reference.mkdir()
            (reference/'suite.json').write_text(json.dumps(dict(cases=[h])))
            path=root/'comparison.md'
            report.write_model_comparison(path,root/'nonhydro',[n],[reference])
            text=path.read_text()
            self.assertIn('2.000 / 2.000',text)
            self.assertIn('100.0% / 100.0%',text)
            self.assertIn('Rigid',text.replace('rigid','Rigid'))
            n['configuration']['time_steps']=100
            report.write_model_comparison(path,root/'nonhydro',[n],[reference])
            self.assertIn('Unmatched: time_steps',path.read_text())
            self.assertNotIn('2.000 / 2.000',path.read_text())
            n['configuration']['time_steps']=10
            n['state']='FAILED'
            report.write_model_comparison(path,root/'nonhydro',[n],[reference])
            self.assertNotIn('2.400000',path.read_text())

    def test_sequences_start_at_one_and_record_next_boundary(self):
        cases = plan.build_plan(self.server(), ('cpu_mpi_scaling_super_fine', 'gpu_scaling_super_fine'))
        cpu = [c for c in cases if c['series'].startswith('cpu')]
        gpu = [c for c in cases if c['series'].startswith('gpu')]
        self.assertEqual([c['ranks'] for c in cpu], [1,3,6,12,24,48,96,192,384])
        self.assertEqual([c['ranks'] for c in gpu], [1,2,4,8,16])
        self.assertEqual(cpu[-1]['state'], 'RESOURCE_LIMIT')
        self.assertEqual(gpu[-1]['state'], 'RESOURCE_LIMIT')

    def test_all_series_and_canonical_resolutions(self):
        cases = plan.build_plan(self.server())
        self.assertEqual(set(c['series'] for c in cases), set(plan.SERIES))
        for series in ('cpu_resolution', 'gpu_resolution'):
            grids = [c['configuration']['global_resolution'] for c in cases if c['series'] == series]
            self.assertEqual(grids, [[360,180,50],[720,360,100],[1440,720,200]])

    def test_every_factor_pair_and_geometry_failure(self):
        cases = plan.build_plan(self.server(), ('cpu_partition_cores_super_fine',))
        self.assertEqual([c['partition'] for c in cases][:3], [[192,1,1],[96,2,1],[64,3,1]])
        self.assertEqual(len(cases), 14)
        self.assertEqual(cases[-1]['partition'], [1,192,1])
        self.assertEqual(cases[-1]['state'], 'GEOMETRY_LIMIT')
        for case in cases:
            if 'configuration' in case:
                self.assertEqual(sum(case['configuration']['x_sizes']),1440)
                self.assertEqual(sum(case['configuration']['y_sizes']),720)

    def test_partition_cases_share_allocations_and_nsight_doubles(self):
        cases = plan.build_plan(self.server(gpu=32), ('gpu_partition_super_fine','gpu_nsight_scaling_super_fine'))
        groups = plan.allocation_groups(cases)
        self.assertEqual(len(groups['gpu_partition_super_fine/2_ranks']),2)
        self.assertEqual(len(groups['gpu_partition_super_fine/4_ranks']),3)
        self.assertEqual([c['partition'] for c in groups['gpu_partition_super_fine/8_ranks']],
                         [[8,1,1],[4,2,1],[2,4,1],[1,8,1]])
        self.assertEqual([c['partition'] for c in groups['gpu_partition_super_fine/16_ranks']],
                         [[16,1,1],[8,2,1],[4,4,1],[2,8,1],[1,16,1]])
        profiles = [c['ranks'] for c in cases if c['series'].startswith('gpu_nsight') and c['state']=='PLANNED']
        self.assertEqual(profiles, [1,2,4,8,16,32])

    def test_larger_grids_start_at_memory_feasible_baselines(self):
        for series, first, grid, dt in (
            ('gpu_scaling_super_super_fine', 4, [2880,1440,200], 30),
            ('gpu_scaling_super_super_super_fine', 16, [5760,2880,200], 15)):
            cases = plan.build_plan(self.server(gpu=256), (series,))
            self.assertEqual(cases[0]['ranks'], first)
            self.assertEqual(cases[0]['configuration']['baseline_ranks'], first)
            self.assertTrue(all(c['configuration']['global_resolution'] == grid for c in cases))
            self.assertTrue(all(c['configuration']['dt'] == dt for c in cases))
            self.assertEqual(cases[-1]['ranks'], 512)
            self.assertEqual(cases[-1]['state'], 'RESOURCE_LIMIT')

    def test_partition_baseline_and_larger_geometry_limits(self):
        cases = plan.build_plan(self.server(gpu=64), ('gpu_partition_super_fine',))
        self.assertEqual(cases[0]['partition'], [1,1,1])
        self.assertEqual(cases[0]['state'], 'PLANNED')
        valid32 = [c['partition'] for c in cases if c['ranks']==32 and c['state']=='PLANNED']
        valid64 = [c['partition'] for c in cases if c['ranks']==64 and c['state']=='PLANNED']
        self.assertEqual(valid32, [[32,1,1],[16,2,1],[8,4,1],[4,8,1],[2,16,1]])
        self.assertEqual(valid64, [[32,2,1],[16,4,1],[8,8,1],[4,16,1]])
        self.assertEqual(sum(c['state']=='GEOMETRY_LIMIT' for c in cases), 4)

    def test_partition_efficiency_uses_measured_single_gpu(self):
        import matplotlib.pyplot as plt
        cases = plan.build_plan(self.server(gpu=2), ('gpu_partition_super_fine',))
        for c in cases:
            if c['state']=='PLANNED':
                c.update(state='COMPLETED', measurement=dict(fastest=1,median=2,retained_substeps=[21]))
        baseline = report.scaling_baselines(cases)['gpu_partition_super_fine']
        self.assertEqual(report.efficiencies(cases[1], baseline), (0.5,0.5))
        rows = [dict(case=c['id'].split('/')[-1],ranks=c['ranks'],state=c['state'],
                     efficiency_fastest=report.efficiencies(c,baseline)[0],
                     efficiency_median=report.efficiencies(c,baseline)[1])
                for c in cases if c['state']=='COMPLETED']
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(plt,'close'):
                report.plot_series(Path(tmp),'gpu_partition_super_fine',rows)
                fig = plt.gcf()
            self.assertEqual(list(fig.axes[0].lines[0].get_ydata()), [100,50,50])
            self.assertEqual(fig.axes[0].get_ylim()[0],0)
            self.assertIn('MPI efficiency',fig.axes[0].get_ylabel())
            plt.close(fig)

    def test_rerun_replaces_whole_series_without_old_baseline(self):
        series = 'gpu_scaling_super_super_super_fine'
        new = plan.build_plan(self.server(gpu=32),(series,))
        old = plan.build_plan(self.server(gpu=32),(series,))
        old[0].update(state='COMPLETED',measurement=dict(fastest=2,median=2))
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);reference=root/'old';reference.mkdir()
            (reference/'suite.json').write_text(json.dumps(dict(cases=old)))
            selected=report.report_cases(root,new,[reference])
            self.assertEqual([c for c,_ in selected],new)
            self.assertNotIn(series,report.scaling_baselines([c for c,_ in selected]))
            replacement=root/'new';replacement.mkdir()
            (replacement/'suite.json').write_text(json.dumps(dict(cases=new)))
            selected=report.report_cases(root,old,replacement_suites=[replacement])
            self.assertEqual([c for c,_ in selected],new)

    def test_weak_scaling_keeps_local_work_fixed(self):
        cases = plan.build_plan(self.server(gpu=64), ('gpu_weak_scaling_super_fine',))
        self.assertEqual([c['ranks'] for c in cases], [1,4,16,64,256])
        for case in cases:
            cfg = case['configuration']
            nx, ny, nz = cfg['global_resolution']
            self.assertEqual(nx * ny * nz // case['ranks'], 207360000)
            self.assertEqual(nz, 200)
            self.assertEqual(set(cfg['x_sizes']), {1440})
            self.assertEqual(set(cfg['y_sizes']), {720})
            self.assertEqual(cfg['dt'], 60 * 1440 / nx)
            self.assertEqual(cfg['scaling_type'], 'weak')
        self.assertEqual(cases[-1]['state'], 'RESOURCE_LIMIT')

    def test_weak_and_larger_grid_efficiencies_and_tables(self):
        import csv
        with tempfile.TemporaryDirectory() as tmp:
            cases = plan.build_plan(self.server(gpu=16),
                                    ('gpu_weak_scaling_super_fine', 'gpu_scaling_super_super_fine'))
            for case in cases:
                if case['state'] == 'PLANNED':
                    time = 2 if case['series'].startswith('gpu_weak') else 8 / case['ranks']
                    case.update(state='COMPLETED', measurement=dict(fastest=time, median=time,
                                retained_substeps=[21], nodes=max(1, case['ranks']//4),
                                gpu_memory_used_bytes=48 * 2**30))
            report.write_report(Path(tmp), cases, plotting=False)
            with (Path(tmp)/'results.csv').open() as stream:
                rows = list(csv.DictReader(stream))
            for row in rows:
                if row['state'] == 'COMPLETED':
                    self.assertEqual(float(row['efficiency_median']), 1)
            content = (Path(tmp)/'plot.md').read_text()
            self.assertIn('48.00', content)
            self.assertIn('207,360,000', content)
            self.assertIn('4 GPUs', content)
            self.assertIn('Throughput (cells/s)', content)

    def test_gpu_device_memory_is_validated_across_ranks(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            cfg = plan.configuration('gpu_scaling_super_fine', 2)
            entries = fixture(folder, cfg)
            for entry in entries:
                entry['gpu_memory_used_bytes'] = (entry['rank'] + 1) * 2**30
            (folder/'results.json').write_text(json.dumps(entries))
            result = report.validate(folder, cfg)
            self.assertEqual(result['gpu_memory_used_bytes'], 2 * 2**30)
            self.assertEqual(result['nodes'], 1)
            entries[1].pop('gpu_memory_used_bytes')
            (folder/'results.json').write_text(json.dumps(entries))
            with self.assertRaises(ValueError):
                report.validate(folder, cfg)

    def test_combined_efficiency_plot_uses_distinct_scaling_definitions(self):
        import matplotlib.pyplot as plt
        cases = []
        for series, grid, ranks, elapsed in (
            ('gpu_scaling_super_super_fine', 'super_super_fine', 4, 2),
            ('gpu_scaling_super_super_fine', 'super_super_fine', 8, 4),
            ('gpu_weak_scaling_super_fine', 'super_fine', 1, 2),
            ('gpu_weak_scaling_super_fine', 'super_super_fine', 4, 4)):
            cases.append(dict(series=series, ranks=ranks, state='COMPLETED',
                              configuration=plan.configuration(series, ranks, grid),
                              measurement=dict(fastest=elapsed, median=elapsed)))
        cases.append({**cases[1], 'state': 'FAILED'})
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(plt, 'close'):
                self.assertTrue(report.plot_scaling_efficiency(Path(tmp), cases))
                fig = plt.gcf()
            self.assertEqual(list(fig.axes[0].lines[0].get_ydata()), [100, 25])
            self.assertEqual(list(fig.axes[1].lines[0].get_ydata()), [100, 50])
            for ax in fig.axes:
                self.assertEqual(list(ax.lines[-1].get_ydata()), [100, 100])
            plt.close(fig)

    def test_uneven_local_grids_use_correct_rank_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            cfg = plan.configuration('cpu_mpi_scaling_super_fine', 6, partition=[2,3,1])
            cfg['global_resolution'] = [15,22,8]
            cfg['x_sizes'], cfg['y_sizes'] = [8,7], [8,7,7]
            entries = fixture(folder,cfg)
            self.assertEqual(report.validate(folder,cfg)['fastest'],1.0)
            entries[0]['grid_size']=[7,8,8]
            (folder/'results.json').write_text(json.dumps(entries))
            with self.assertRaises(ValueError): report.validate(folder,cfg)

    def test_rejects_duplicate_physical_cores_and_false_windows(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);cfg=plan.configuration('cpu_mpi_scaling_super_fine',3)
            entries=fixture(folder,cfg)
            layout=json.loads((folder/'layout.json').read_text());layout[1]['physical_core']=layout[0]['physical_core']
            (folder/'layout.json').write_text(json.dumps(layout))
            with self.assertRaises(ValueError):report.validate(folder,cfg)
            fixture(folder,cfg);entries[0]['time_per_step_seconds']=0.5
            (folder/'results.json').write_text(json.dumps(entries))
            with self.assertRaises(ValueError):report.validate(folder,cfg)

    def test_profile_checksums_and_kernel_summary_required(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);cfg=plan.configuration('gpu_nsight_scaling_super_fine',1)
            fixture(folder,cfg);rank=folder/'rank_0';rank.mkdir()
            trace=rank/'fixture.nsys-rep';trace.write_bytes(b'unit test, not a real trace')
            (rank/'trace_path.txt').write_text(str(trace));(rank/'trace_bytes.txt').write_text(str(trace.stat().st_size))
            (rank/'trace_sha256.txt').write_text(hashlib.sha256(trace.read_bytes()).hexdigest())
            (rank/'exit_code.txt').write_text('0')
            (rank/'summary_cuda_gpu_kern_sum.csv').write_text('Total Time (ns),Instances,Name\n100,2,compute_hydrostatic_free_surface_Gc!\n')
            self.assertEqual(report.validate(folder,cfg)['kernel_nanoseconds']['Gc'],100)
            trace.write_bytes(b'x'*trace.stat().st_size)
            with self.assertRaises(ValueError):report.validate(folder,cfg)

    def test_accounting_outage_keeps_valid_completed_case(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);cases=plan.build_plan(self.server(cpu=1,gpu=0),('cpu_mpi_scaling_super_fine',))
            cases[0].update(state='SUBMITTED',job_id='123')
            fixture(folder/cases[0]['id'],cases[0]['configuration'])
            data=dict(server=dict(backend='slurm',matplotlib=False),cases=cases)
            with patch.object(runner,'command',return_value=subprocess.CompletedProcess([],1,'database down')):
                self.assertTrue(runner.refresh(folder,data))
            self.assertEqual(cases[0]['state'],'COMPLETED')
            self.assertTrue((folder/'plot.md').exists())

    def test_slurm_resources_and_commands_are_quoted(self):
        server=runner.load_server();server.update(backend='slurm',gpus_per_node=8,gpu_type='h100',gpu_account='test',max_gpus=16)
        case=plan.build_plan(dict(max_cpu_cores=192,max_gpus=16),('gpu_scaling_super_fine',))[4]
        args=runner.sbatch_command(server,[case],Path('/tmp/path with spaces/allocation.sh'))
        self.assertIn('--nodes=2',args);self.assertIn('--gpus-per-task=h100:1',args)
        self.assertEqual(args[-1],'/tmp/path with spaces/allocation.sh')

    def test_generated_shell_handles_spaces_and_has_valid_syntax(self):
        with tempfile.TemporaryDirectory(prefix='suite with spaces ') as tmp:
            folder = Path(tmp)
            server = runner.load_server()
            server.update(backend='slurm', max_gpus=4, gpus_per_node=8)
            cases = plan.build_plan(dict(max_cpu_cores=192,max_gpus=4), ('gpu_partition_super_fine',))
            group = plan.allocation_groups(cases)['gpu_partition_super_fine/4_ranks']
            for case in group:
                (folder/case['id']).mkdir(parents=True)
            script = runner.group_script(folder,server,group)
            subprocess.run(['bash','-n',str(script)],check=True)
            self.assertEqual(script.read_text().count('date -u +%FT%TZ'), 6)
            self.assertIn('compute_hardware.txt',script.read_text())

    def test_executable_snapshot_is_self_contained_for_reporting(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            server = runner.load_server()
            runner.prepare(folder,server,('gpu_partition_super_fine',))
            result = subprocess.run([sys.executable,str(folder/'run_metadata/benchmark_suite.py'), '--output',str(folder),'--refresh'],text=True,capture_output=True)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertTrue((folder/'plot.md').exists())

    def test_cpu_hardware_capture_does_not_query_unassigned_gpus(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            server = runner.load_server()
            server.update(backend='slurm')
            cases = plan.build_plan(self.server(), ('cpu_partition_cores_super_fine',))
            group = next(iter(plan.allocation_groups(cases).values()))
            for case in group:
                (folder/case['id']).mkdir(parents=True)
            script = runner.group_script(folder, server, group)
            subprocess.run(['bash', '-n', str(script)], check=True)
            self.assertNotIn('nvidia-smi', script.read_text())

    def test_plots_timing_efficiency_and_profile_kernel_shares(self):
        with tempfile.TemporaryDirectory() as tmp:
            cases = plan.build_plan(self.server(gpu=1), ('gpu_nsight_scaling_super_fine',))
            cases[0].update(state='COMPLETED',measurement=dict(fastest=1,median=1.1,retained_substeps=[21],kernel_nanoseconds=dict(Gc=100,Gu=200,Gv=300,Others=400)))
            report.write_report(Path(tmp),cases,plotting=True)
            self.assertTrue((Path(tmp)/'gpu_nsight_scaling_super_fine.svg').exists())
            self.assertTrue((Path(tmp)/'gpu_nsight_scaling_super_fine_kernels.svg').exists())
            self.assertIn('10.00%',(Path(tmp)/'plot.md').read_text())
            svg = (Path(tmp)/'gpu_nsight_scaling_super_fine.svg').read_text()
            self.assertIn('Ideal: 100%', svg)
            self.assertIn('Ideal: one-rank fastest / ranks', svg)

    def test_resolution_ratio_accounts_for_volume_and_missing_grids(self):
        import matplotlib.pyplot as plt
        with tempfile.TemporaryDirectory() as tmp:
            rows = [dict(case=name, state='COMPLETED', fastest=t, median=2*t)
                    for name, t in (('default', 1), ('fine', 8), ('super_fine', 64))]
            with patch.object(plt, 'close'):
                report.plot_series(Path(tmp), 'gpu_resolution', rows)
                fig = plt.gcf()
            ax = fig.axes[0]
            self.assertEqual(list(ax.lines[0].get_ydata()), [1/8, 1/8])
            self.assertEqual(list(ax.lines[1].get_ydata()), [1/8, 1/8])
            self.assertEqual('Previous-grid / next-grid time', ax.get_ylabel())
            self.assertEqual(list(ax.lines[2].get_ydata()), [1/8, 1/8])
            plt.close(fig)
            with patch.object(plt, 'close'):
                report.plot_series(Path(tmp), 'gpu_resolution', [rows[0], rows[2]])
                fig = plt.gcf()
            self.assertEqual(len(fig.axes[0].lines[0].get_ydata()), 0)
            plt.close(fig)

    def test_local_startup_failure_is_terminal(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);server=runner.load_server();server.update(max_cpu_cores=1,max_gpus=0,matplotlib=False)
            cases=plan.build_plan(server,('cpu_mpi_scaling_super_fine',))
            (folder/cases[0]['id']).mkdir(parents=True)
            data=dict(server=server,cases=cases)
            process=MagicMock();process.wait.return_value=127
            with patch.object(runner.subprocess,'Popen',return_value=process):
                runner.execute(folder,data)
            self.assertEqual(cases[0]['state'],'INTERRUPTED')
            self.assertTrue(runner.refresh(folder,data))

    def test_local_timeout_terminates_mpi_process_group(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp);server=runner.load_server();server.update(max_cpu_cores=1,max_gpus=0,matplotlib=False)
            cases=plan.build_plan(server,('cpu_mpi_scaling_super_fine',))
            (folder/cases[0]['id']).mkdir(parents=True)
            data=dict(server=server,cases=cases)
            process=MagicMock();process.pid=1234;process.wait.side_effect=[subprocess.TimeoutExpired('bash',1),0]
            with patch.object(runner.subprocess,'Popen',return_value=process),patch.object(runner.os,'killpg') as kill:
                runner.execute(folder,data)
            self.assertEqual(cases[0]['state'],'TIMEOUT')
            kill.assert_called_once_with(1234,runner.signal.SIGTERM)

    def test_rebased_server_config_preserves_environment_and_references(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'server.json'
            path.write_text(json.dumps(dict(max_cpu_cores=1,max_gpus=0,environment={'JULIA_DEPOT_PATH':'/tmp/depot with spaces'},reference_suites=['/tmp/reference'],gpu_scaling_partition='x')))
            server=runner.load_server(path)
            self.assertEqual(server['reference_suites'],['/tmp/reference'])
            self.assertIn("export JULIA_DEPOT_PATH='/tmp/depot with spaces'",runner.environment_lines(server))
            case=next(c for c in plan.build_plan(dict(max_cpu_cores=192,max_gpus=4,gpu_scaling_partition='x'),('gpu_scaling_super_fine',)) if c['ranks']==4)
            self.assertEqual(case['configuration']['partition'],[4,1,1])

    def test_historical_weak_results_without_new_schema_fields(self):
        baseline=dict(series='gpu_weak_scaling_super_fine',state='COMPLETED',ranks=1,configuration={},measurement=dict(fastest=1,median=1))
        case=dict(series='gpu_weak_scaling_super_fine',state='COMPLETED',ranks=4,configuration={},measurement=dict(fastest=1.25,median=1.25))
        self.assertEqual(report.efficiencies(case,baseline),(0.8,0.8))
        larger=dict(series='gpu_scaling_super_super_fine',state='COMPLETED',ranks=4,configuration={},measurement=dict(fastest=1,median=1))
        self.assertEqual(report.scaling_baselines([larger])[larger['series']],larger)

    def test_resume_does_not_resubmit_pending_jobs(self):
        cases=plan.build_plan(self.server(),('gpu_partition_super_fine',))
        two_gpu_cases=[c for c in cases if c['ranks']==2]
        two_gpu_cases[0]['state']='PENDING';two_gpu_cases[1]['state']='RUNNING'
        groups=plan.allocation_groups(cases)
        self.assertNotIn('gpu_partition_super_fine/2_ranks',groups)

    def test_report_excludes_failed_timings_and_uses_one_rank_baseline(self):
        with tempfile.TemporaryDirectory() as tmp:
            cases=plan.build_plan(self.server(gpu=2),('gpu_scaling_super_fine',))
            cases[0].update(state='COMPLETED',measurement=dict(fastest=2,median=2.2,retained_substeps=[21]))
            cases[1].update(state='FAILED',details='OOM')
            report.write_report(Path(tmp),cases,plotting=False)
            text=(Path(tmp)/'plot.md').read_text()
            self.assertIn('100.0% / 100.0%',text);self.assertIn('OOM',text)
            self.assertIn('Highest completed count: **1 ranks**',text)


if __name__=='__main__':unittest.main()
