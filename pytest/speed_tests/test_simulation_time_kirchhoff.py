__author__ = "Christian Kongsgaard"
__license__ = 'MIT'

# -------------------------------------------------------------------------------------------------------------------- #
# IMPORTS

# Modules
import pytest
import platform
import os
import datetime

# RiBuild Modules
from delphin_6_automation.database_interactions import delphin_interactions
from delphin_6_automation.database_interactions import general_interactions
from delphin_6_automation.backend import simulation_worker

# -------------------------------------------------------------------------------------------------------------------- #
# RIBuild

#
# Result: Simulation without Kirchhoff is significatly faster
#


@pytest.mark.skipif(platform.system() == 'Linux', reason='Test should only run locally')
@pytest.mark.parametrize('change_to', [True, False])
def test_speed_vs_cores(mock_driving_rain, mock_wait_until_finished, db_one_project, change_to):

    db_one_project = str(db_one_project)
    folder = 'H:/ribuild'
    simulation_folder = os.path.join(folder, db_one_project)
    os.mkdir(simulation_folder)
    delphin_interactions.change_entry_simulation_length(db_one_project, 1, 'a')
    delphin_interactions.change_entry_kirchhoff_potential(db_one_project, change_to)
    general_interactions.download_full_project_from_database(db_one_project, simulation_folder)
    submit_file, estimated_time = simulation_worker.create_submit_file(db_one_project, simulation_folder)
    simulation_worker.submit_job(submit_file, db_one_project)

    time_0 = datetime.datetime.now()
    simulation_worker.wait_until_finished(db_one_project, estimated_time, simulation_folder)
    delta_time = datetime.datetime.now() - time_0

    with open(os.path.join(folder, 'time.txt'), 'a') as out:
        out.write(f'Kirchhoff: {change_to} - Simulation Time: {str(delta_time.total_seconds())} \n')
