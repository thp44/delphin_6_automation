__author__ = "Christian Kongsgaard"
__license__ = 'MIT'

# -------------------------------------------------------------------------------------------------------------------- #
# IMPORTS

# Modules
import pytest
import datetime
import os
import time
import shutil

# RiBuild Modules
from delphin_6_automation.backend import simulation_worker
from delphin_6_automation.database_interactions.db_templates import delphin_entry

# -------------------------------------------------------------------------------------------------------------------- #
# RIBuild


@pytest.mark.parametrize('restart',
                         [False, True])
def test_create_submit_file(tmpdir, db_one_project, restart):

    folder = tmpdir.mkdir('test')
    delphin_id = delphin_entry.Delphin.objects().first().id

    expected_submit_file = ["#!/bin/bash\n", "#BSUB -J DelphinJob\n", "#BSUB -o DelphinJob_%J.out\n",
                            "#BSUB -e DelphinJob_%J.err\n", "#BSUB -q hpc\n", "#BSUB -W 120\n",
                            '#BSUB -R "rusage[mem=14MB] span[hosts=1]"\n', "#BSUB -n 2\n", "#BSUB -N\n",
                            '\n', "export OMP_NUM_THREADS=$LSB_DJOB_NUMPROC\n", '\n',
                            f"~/Delphin-6.0/bin/DelphinSolver {delphin_id}.d6p\n", '\n']

    expected_restart = f"~/Delphin-6.0/bin/DelphinSolver --restart {delphin_id}.d6p\n"

    submit_file = simulation_worker.create_submit_file(delphin_id, folder, 120, restart)

    assert submit_file
    assert submit_file == f'submit_{delphin_id}.sh'
    assert os.path.exists(os.path.join(folder, submit_file))

    with open(os.path.join(folder, submit_file), 'r') as file:
        submit_data = file.readlines()

    if not restart:
        assert submit_data == expected_submit_file

    else:
        expected_submit_file[-2] = expected_restart
        assert submit_data == expected_submit_file


def test_hpc_worker(tmpdir, db_one_project, mock_submit_job, monkeypatch, test_folder):
    folder = tmpdir.mkdir('test')
    delphin_doc = delphin_entry.Delphin.objects().first()

    def mockreturn(sim_id, estimated_run_time, simulation_folder):
        result_zip = test_folder + '/raw_results/delphin_results1.zip'
        delphin_folder = os.path.join(folder, str(delphin_doc.id))
        shutil.unpack_archive(result_zip, delphin_folder)
        os.rename(os.path.join(delphin_folder, 'delphin_id'), os.path.join(delphin_folder, str(delphin_doc.id)))

        time.sleep(2)
        return None

    monkeypatch.setattr(simulation_worker, 'wait_until_finished', mockreturn)

    simulation_worker.hpc_worker(str(delphin_doc.id), folder)

    delphin_doc.reload()

    assert not os.path.exists(os.path.join(folder, str(delphin_doc.id)))
    assert delphin_doc.results_raw
    assert delphin_doc.result_processed
    assert delphin_doc.simulated
    assert delphin_doc.simulation_time


def test_simulation_worker(mock_hpc_worker, mock_find_next_sim_in_queue, capsys):

    with pytest.raises(SystemExit) as exc_info:
        simulation_worker.simulation_worker('hpc')

    out, err = capsys.readouterr()
    assert out.split('\n')[0] == 'hpc called'
    assert 'None' in str(exc_info.value)


def test_simulation_worker_exception(db_one_project, mock_hpc_worker_exception, mock_sleep_exception,
                                     tmpdir, mock_copytree):

    with pytest.raises(SystemExit) as exc_info:
        simulation_worker.simulation_worker('hpc', tmpdir)

    delphin_doc = delphin_entry.Delphin.objects().first()
    assert 'None' in str(exc_info.value)
    assert not delphin_doc.simulating


def test_simulation_worker_failed_simulation(mock_hpc_worker_failed_simulation, mock_sleep_exception):

    with pytest.raises(SystemExit) as exc_info:
        simulation_worker.simulation_worker('hpc', mock_hpc_worker_failed_simulation)

    delphin_doc = delphin_entry.Delphin.objects().first()
    original_folder = os.path.join(mock_hpc_worker_failed_simulation, str(delphin_doc.id))
    failed_folder = os.path.join(mock_hpc_worker_failed_simulation, 'failed', str(delphin_doc.id))

    assert os.listdir(original_folder) == os.listdir(failed_folder)


def test_exceeding_time_limit(mock_hpc_worker_time_limit, test_folder):
    folder, sim_id = mock_hpc_worker_time_limit

    simulation_worker.hpc_worker(str(sim_id), folder)

    delphin_doc = delphin_entry.Delphin.objects(id=sim_id).first()

    assert delphin_doc
    assert delphin_doc.exceeded_time_limit


def test_consecutive_errors(mock_wait_consecutive_errors, tmpdir):
    return_code = simulation_worker.wait_until_finished('Test_ID', 5, tmpdir)

    assert return_code == 'consecutive errors'


def test_parse_hpc_log(test_folder):
    with open(os.path.join(test_folder, 'logs', 'hpc_logs.txt')) as file:
        data = file.read()

    line = simulation_worker.parse_hpc_log(data)
    assert line == 'Job <2947325> is submitted to queue <hpc>.'