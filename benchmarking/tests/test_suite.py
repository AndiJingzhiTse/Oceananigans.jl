"""Test plans, launch commands, validation and restart behavior without production jobs."""
import hashlib
import json
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
        profiles = [c['ranks'] for c in cases if c['series'].startswith('gpu_nsight') and c['state']=='PLANNED']
        self.assertEqual(profiles, [1,2,4,8,16,32])

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

    def test_resume_does_not_resubmit_pending_jobs(self):
        cases=plan.build_plan(self.server(),('gpu_partition_super_fine',))
        cases[0]['state']='PENDING';cases[1]['state']='RUNNING'
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
