"""Check ensemble placement, validation and throughput arithmetic."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

from test_suite import plan, fixture
from suite.ensemble import member_configuration, validate_ensemble
from suite.variants import comparison_rows, write_comparison


class EnsembleTests(unittest.TestCase):
    def config(self, mode='baseline'):
        server = dict(machine='rondeau', model_type='NonhydrostaticModel', max_cpu_cores=128,
                      max_gpus=4, execution_mode=mode, pressure_preconditioner='LocalFFTPreconditioner',
                      series_definitions={})
        return plan.build_plan(server, ('gpu_ensemble',))[0]['configuration']

    def artifacts(self, folder, config):
        records, layouts = [], []
        for i in range(1, 5):
            child = folder / f'member_{i}'
            cfg = member_configuration(config, i)
            fixture(child, cfg)
            (child / 'configuration.json').write_text(json.dumps(cfg))
            data = json.loads((child / 'results.json').read_text())
            record = copy.deepcopy(data[0])
            record['ensemble_member'] = i
            records.append(record)
            layout = json.loads((child / 'layout.json').read_text())
            layout[0]['gpu_uuid'] = f'GPU-{i}'
            layout[0]['affinity'] = str(i-1)
            (child / 'layout.json').write_text(json.dumps(layout))
            layouts.append(dict(layout[0], ensemble_member=i))
        (folder / 'results.json').write_text(json.dumps(records))
        (folder / 'layout.json').write_text(json.dumps(layouts))
        (folder / 'ensemble_launch.json').write_text(json.dumps(dict(members=[dict(id=i,cpu=i-1,gpu_uuid=f'GPU-{i}') for i in range(1,5)])))
        summary = dict(execution_mode=config['execution_mode'], timed_seconds=61, dispatch_seconds=90,
                       setup_seconds=10, completed=[dict(id=i, worker=i+1, pid=100+i) for i in range(1,5)],
                       events=[(name, i, stamp) for name, stamp in
                               [('ready', 1), ('timing_started', 2), ('timed', 62)] for i in range(1,5)])
        (folder / 'ensemble.json').write_text(json.dumps(summary))
        return summary

    def test_plan_is_four_independent_models_at_two_resolutions(self):
        cases = plan.build_plan(dict(max_cpu_cores=128,max_gpus=4,model_type='NonhydrostaticModel'),('gpu_ensemble',))
        self.assertEqual([c['id'] for c in cases],['gpu_ensemble/default','gpu_ensemble/fine'])
        for c in cases:
            self.assertEqual(c['ranks'],4)
            self.assertEqual(c['configuration']['ranks'],1)
            self.assertEqual(c['configuration']['partition'],[1,1,1])
            self.assertEqual(c['configuration']['ensemble_size'],4)
        limited = plan.build_plan(dict(max_cpu_cores=128,max_gpus=2),('gpu_ensemble',))
        self.assertEqual({c['state'] for c in limited},{'RESOURCE_LIMIT'})

    def test_members_use_direct_timestepping_and_reproducible_distinct_seeds(self):
        for mode in ('baseline','dagger'):
            cfg=self.config(mode)
            cfg['execution_adapter'] = {'id': 'outer-simulation-scheduler'}
            members=[member_configuration(cfg,i) for i in range(1,5)]
            self.assertTrue(all('execution_adapter' not in m for m in members))
            self.assertEqual([m['initial_condition_seed'] for m in members],[1234,1235,1236,1237])
            self.assertTrue(all(m['execution_mode']=='baseline' and m['ensemble_execution_mode']==mode for m in members))

    def test_acceptance_requires_all_members_distinct_gpus_and_overlap(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); cfg=self.config(); summary=self.artifacts(root,cfg)
            m=validate_ensemble(root,cfg)
            self.assertAlmostEqual(m['ensemble_simulations_per_hour'],4*3600/61)
            self.assertEqual(m['median'],1.2)
            # CUDA and nvidia-smi spell the same device UUID differently.
            child=root/'member_1/layout.json'
            child_layout=json.loads(child.read_text());child_layout[0]['gpu_uuid']='1'
            child.write_text(json.dumps(child_layout))
            layout=json.loads((root/'layout.json').read_text());layout[0]['gpu_uuid']='1'
            (root/'layout.json').write_text(json.dumps(layout))
            validate_ensemble(root,cfg)
            layout=json.loads((root/'layout.json').read_text())
            child=root/'member_4/layout.json'
            child_layout=json.loads(child.read_text());child_layout[0]['gpu_uuid']='GPU-1'
            child.write_text(json.dumps(child_layout));layout[3]['gpu_uuid']='GPU-1'
            (root/'layout.json').write_text(json.dumps(layout))
            with self.assertRaisesRegex(ValueError,'different GPU|share a GPU'):validate_ensemble(root,cfg)
            self.artifacts(root,cfg)
            summary['events']=[(name,i,(i*100 if name=='timing_started' else i*100+1) if name!='ready' else 1)
                               for name in ('ready','timing_started','timed') for i in range(1,5)]
            (root/'ensemble.json').write_text(json.dumps(summary))
            with self.assertRaisesRegex(ValueError,'did not overlap'):validate_ensemble(root,cfg)
            self.artifacts(root,cfg)
            (root/'member_3/results.json').unlink()
            with self.assertRaises(FileNotFoundError):validate_ensemble(root,cfg)

    def test_ensemble_speedup_uses_makespan_and_requires_both_validated(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for mode, seconds in [('baseline',20),('dagger',10)]:
                folder=root/mode/'gpu_ensemble';folder.mkdir(parents=True)
                case=dict(id='default',ranks=4,state='COMPLETED',configuration=self.config(mode),
                          measurement=dict(fastest=1,median=2,ensemble_timed_seconds=seconds,ensemble_dispatch_seconds=seconds*2))
                (folder/'suite.json').write_text(json.dumps(dict(cases=[case])))
            row=comparison_rows(root,('gpu_ensemble',))[0]
            self.assertEqual(row['speedup_ensemble_timed'],2)
            self.assertEqual(row['speedup_median'],1)
            write_comparison(root,root/'comparison',selected=('gpu_ensemble',))
            self.assertIn('Timed makespan',(root/'comparison/comparison.md').read_text())
            self.assertIn('Equal time (1)',(root/'comparison/comparisons/gpu_ensemble.svg').read_text())
            case['state']='FAILED'
            (folder/'suite.json').write_text(json.dumps(dict(cases=[case])))
            self.assertEqual(comparison_rows(root,('gpu_ensemble',))[0]['speedup_ensemble_timed'],'')
