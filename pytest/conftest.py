__author__ = "Christian Kongsgaard"
__license__ = 'MIT'

# -------------------------------------------------------------------------------------------------------------------- #
# IMPORTS

# Modules
import pytest
from mongoengine.connection import get_connection
from collections import OrderedDict
import os
import shutil
import sys
import numpy as np
import time
import pandas as pd

# RiBuild Modules
from delphin_6_automation.database_interactions import mongo_setup
from delphin_6_automation.database_interactions import user_interactions
from delphin_6_automation.database_interactions import material_interactions
from delphin_6_automation.database_interactions import weather_interactions
from delphin_6_automation.database_interactions import general_interactions
from delphin_6_automation.database_interactions import delphin_interactions
from delphin_6_automation.database_interactions import simulation_interactions
from delphin_6_automation.database_interactions import sampling_interactions
from delphin_6_automation.file_parsing import delphin_parser
from delphin_6_automation.file_parsing import weather_parser
from delphin_6_automation.database_interactions.db_templates import delphin_entry
from delphin_6_automation.database_interactions.db_templates import sample_entry
from delphin_6_automation.database_interactions.db_templates import result_raw_entry
from delphin_6_automation.sampling import sampling
from delphin_6_automation.backend import simulation_worker
from delphin_6_automation.sampling import inputs


# -------------------------------------------------------------------------------------------------------------------- #
# RIBuild


@pytest.fixture(scope='session')
def setup_database():
    if sys.platform == 'win32':
        auth_dict = {"ip": "192.38.64.134",
                     "port": 27017,
                     "alias": "local",
                     "name": "test",
                     "ssh": False}
    else:
        auth_dict = {"ip": "127.0.0.1",
                     "port": 27017,
                     "alias": "local",
                     "name": "test",
                     "ssh": False}

    mongo_setup.global_init(auth_dict)

    yield

    db = get_connection('local')
    db.drop_database('test')
    mongo_setup.global_end_ssh(auth_dict)


@pytest.fixture(scope='function')
def empty_database(setup_database):
    db = get_connection('local')
    db.drop_database('test')

    yield


@pytest.fixture()
def test_folder():
    return os.path.dirname(os.path.realpath(__file__)) + '/test_files'


@pytest.fixture()
def delphin_file_path(test_folder):
    delphin_file = test_folder + '/delphin/delphin_project_1d.d6p'

    return delphin_file


@pytest.fixture(params=['1d_exterior_interior_plaster_insulated3layers',
                        '1d_exterior_interior_plaster_insulated2layers',
                        '1d_interior_plaster_insulated2layers',
                        '1d_interior_plaster_insulated3layers'])
def delphin_with_insulation(test_folder, request):
    delphin_file = test_folder + f'/delphin/{request.param}.d6p'

    return delphin_parser.dp6_to_dict(delphin_file)


@pytest.fixture()
def add_single_user(setup_database):
    user_interactions.create_account('User Test', 'test@test.com')

    yield


@pytest.fixture()
def add_two_materials(test_folder, setup_database):
    material_files = ['AltbauziegelDresdenZP_504.m6', 'LimeCementMortarHighCementRatio_717.m6', ]

    for file in material_files:
        material_interactions.upload_material_file(test_folder + '/materials/' + file)

    yield


@pytest.fixture()
def add_five_materials(test_folder, setup_database):
    material_files = ['AltbauziegelDresdenZP_504.m6', 'LimeCementMortarHighCementRatio_717.m6',
                      'GlueMortarForClimateBoard_705.m6', 'CalsithermCalciumsilikatHamstad_571.m6',
                      'KlimaputzMKKQuickmix_125.m6']

    for file in material_files:
        material_interactions.upload_material_file(test_folder + '/materials/' + file)

    yield


@pytest.fixture()
def add_insulation_materials(test_folder, setup_database):
    material_files = ['CalciumSilicateBoard_39.m6', 'PolystyreneBoardExpanded_187.m6',
                      'GlueMortarForClimateBoard_705.m6', 'CarraraMamorSkluptur_559.m6',
                      'KlimaputzMKKQuickmix_125.m6', 'AirGapHorizontal50mm_12.m6']

    for file in material_files:
        material_interactions.upload_material_file(test_folder + '/materials/' + file)

    yield


@pytest.fixture()
def add_three_years_weather(setup_database, test_folder):
    weather_ids = weather_interactions.upload_weather_to_db(test_folder + '/weather/Aberdeen_3_years.WAC')

    return weather_ids


@pytest.fixture()
def db_one_project(empty_database, delphin_file_path, add_single_user, add_two_materials, add_three_years_weather):
    priority = 'high'
    climate_class = 'a'
    location_name = 'Aberdeen'
    years = [2020, 2021, 2022]

    sim_id = general_interactions.add_to_simulation_queue(delphin_file_path, priority)
    weather_interactions.assign_indoor_climate_to_project(sim_id, climate_class)
    weather_interactions.assign_weather_by_name_and_years(sim_id, location_name, years)
    delphin_interactions.change_entry_simulation_length(sim_id, len(years), 'a')

    return sim_id


@pytest.fixture()
def add_results(db_one_project, tmpdir, test_folder):
    temp_folder = tmpdir.mkdir('upload')
    delphin_doc = delphin_entry.Delphin.objects().first()

    # Upload results
    result_zip = test_folder + '/raw_results/delphin_results.zip'
    shutil.unpack_archive(result_zip, temp_folder)
    os.rename(os.path.join(temp_folder, 'delphin_results'), os.path.join(temp_folder, str(delphin_doc.id)))
    result_id = delphin_interactions.upload_results_to_database(os.path.join(temp_folder, str(delphin_doc.id)))

    return result_id


@pytest.fixture()
def add_sampling_strategy(empty_database, add_three_years_weather, tmpdir, mock_design_options):
    test_dir = tmpdir.mkdir('test')
    strategy = sampling.create_sampling_strategy(test_dir)
    sampling_interactions.upload_sampling_strategy(strategy)


@pytest.fixture()
def add_raw_sample(setup_database):
    sampling_interactions.upload_raw_samples(sampling.sobol(m=2 ** 12, dimension=3), 0)


@pytest.fixture()
def strategy_with_raw_dummy_samples(add_sampling_strategy):
    strategy_entry = sample_entry.Strategy.objects().first()
    raw_id = sampling_interactions.upload_raw_samples(np.random.rand(2 ** 12,
                                                                     len(strategy_entry.strategy[
                                                                             'distributions'].keys())),
                                                      0)

    sampling_interactions.add_raw_samples_to_strategy(strategy_entry, raw_id)


@pytest.fixture()
def dummy_sample():
    return {str(i): {} for i in range(10)}


@pytest.fixture()
def mock_sobol(monkeypatch):
    strategy = sample_entry.Strategy.objects().first()

    def mockreturn(m, dimension, sets):
        return np.random.rand(2 ** 12, len(strategy.strategy['distributions'].keys()))

    monkeypatch.setattr(sampling, 'sobol', mockreturn)


@pytest.fixture()
def mock_material_info(monkeypatch):
    def mockreturn(material_id):
        return OrderedDict((('@name', 'Test Material [000]'),
                            ('@color', '#ff5020a0'),
                            ('@hatchCode', str(13)),
                            ('#text', '${Material Database}/TestMaterial_000.m6')
                            )
                           )

    monkeypatch.setattr(material_interactions, 'get_material_info', mockreturn)


@pytest.fixture()
def add_dummy_sample(setup_database, dummy_sample):
    sample_id = sampling_interactions.upload_samples(dummy_sample, 0)


@pytest.fixture()
def create_samples(add_sampling_strategy, mock_sobol):
    strategy = sample_entry.Strategy.objects().first()

    samples = sampling.create_samples(strategy, 0)

    return samples


@pytest.fixture()
def add_delphin_for_errors(empty_database, delphin_file_path, add_two_materials, add_three_years_weather,
                           add_results, test_folder, tmpdir):
    priority = 'high'
    climate_class = 'a'
    location_name = 'Aberdeen'
    years = [2020, 2021, 2022]
    design_list = ['1d_interior_plaster', '1d_interior_plaster',
                   '1d_exterior_interior_plaster', '1d_exterior_interior_plaster']
    result_doc = result_raw_entry.Result.objects().first()
    folder = tmpdir.mkdir('test')
    weather_folder = folder.mkdir('weather')
    result_zip = test_folder + '/raw_results/delphin_results1.zip'
    shutil.unpack_archive(result_zip, folder)
    shutil.copy(f'{test_folder}/weather/temperature.ccd', f'{weather_folder}/temperature.ccd')
    shutil.copy(f'{test_folder}/weather/indoor_temperature.ccd', f'{weather_folder}/indoor_temperature.ccd')
    result_folder = os.path.join(folder, 'delphin_id')

    for sequence_index in range(10):
        for design in design_list:
            sim_id = general_interactions.add_to_simulation_queue(delphin_file_path, priority)
            weather_interactions.assign_indoor_climate_to_project(sim_id, climate_class)
            weather_interactions.assign_weather_by_name_and_years(sim_id, location_name, years)
            delphin_interactions.change_entry_simulation_length(sim_id, len(years), 'a')
            delphin_interactions.add_sampling_dict(sim_id, {'design_option': design,
                                                            'sequence': sequence_index})
            delphin_doc = delphin_entry.Delphin.objects(id=sim_id).first()
            delphin_interactions.upload_processed_results(result_folder, delphin_doc.id, result_doc.id)


@pytest.fixture()
def add_strategy_for_errors(setup_database, add_three_years_weather):
    strategy = {'design': ['1d_interior_plaster', '1d_exterior_interior_plaster'],
                'settings': {'sequence': 10, 'standard error threshold': 0.1}}
    sampling_interactions.upload_sampling_strategy(strategy)


@pytest.fixture()
def mock_submit_job(monkeypatch):
    def mockreturn(submit_file, sim_id):
        return None

    monkeypatch.setattr(simulation_worker, 'submit_job', mockreturn)


@pytest.fixture()
def mock_sleep(monkeypatch):
    def mockreturn(secs):
        return None

    monkeypatch.setattr(time, 'sleep', mockreturn)


@pytest.fixture()
def mock_hpc_worker(monkeypatch):
    def mockreturn(id_, folder=None):
        print('hpc called')
        exit()
        return None

    monkeypatch.setattr(simulation_worker, 'hpc_worker', mockreturn)


@pytest.fixture()
def mock_find_next_sim_in_queue(monkeypatch):
    def mockreturn():
        return 'test_id'

    monkeypatch.setattr(simulation_interactions, 'find_next_sim_in_queue', mockreturn)


@pytest.fixture()
def mock_hpc_worker_exception(monkeypatch):
    def mockreturn(id_, thread_name, folder=None):
        raise FileNotFoundError

    monkeypatch.setattr(simulation_worker, 'hpc_worker', mockreturn)


@pytest.fixture()
def mock_sleep_exception(monkeypatch):
    def mockreturn(secs):
        exit()
        return None

    monkeypatch.setattr(time, 'sleep', mockreturn)


@pytest.fixture()
def add_sample_for_errors(add_strategy_for_errors, dummy_sample):
    mean = {str(i): {'1d_interior_plaster': {'mould': 0.5,
                                             'algae': 0.5,
                                             'heat_loss': 0.5}} for i in range(10)}

    strategy_doc = sample_entry.Strategy.objects().first()
    sample_id = sampling_interactions.upload_samples(dummy_sample, 0)
    sampling_interactions.upload_sample_mean(sample_id, mean)
    sampling_interactions.add_sample_to_strategy(strategy_doc.id, sample_id)


@pytest.fixture()
def dummy_systems():
    multi_index = pd.MultiIndex(levels=[[0, 1], ['insulation_00', 'insulation_01',
                                                 'insulation_02', 'finish_00', 'detail_00']],
                                labels=[[0, 0, 0, 0, 0, 1, 1, 1], [0, 1, 2, 3, 4, 0, 1, 3]],
                                names=['ID', 'Dimension'], )
    frame = pd.DataFrame(index=multi_index, data={'ID': [39, 39, 39, 125, 705, 187, 187, 559],
                                                  'Dimension': [25, 50, 100, 10, 5, 25, 35, 12]})

    return frame


@pytest.fixture()
def delphin_reference_folder(test_folder, tmpdir):
    folder = tmpdir.mkdir('test')
    folder.mkdir('design')
    folder.mkdir('delphin')
    delphin_folder = os.path.join(test_folder, 'delphin')

    for file in os.listdir(delphin_folder):
        new_file = os.path.join(folder, 'delphin', file)
        shutil.copyfile(os.path.join(delphin_folder, file), new_file)

    return folder


@pytest.fixture()
def delphin_design_folder(test_folder, tmpdir):
    if not os.path.exists(os.path.join(tmpdir, 'test')):
        folder = tmpdir.mkdir('test')
        folder.mkdir('design')
        folder.mkdir('delphin')
    else:
        folder = os.path.join(tmpdir, 'test')
        os.mkdir(os.path.join(folder, 'design'))
        os.mkdir(os.path.join(folder, 'delphin'))

    delphin_folder = os.path.join(test_folder, 'delphin')

    for index, file in enumerate(os.listdir(delphin_folder)):
        names = ['1d_exterior.d6p', '1d_interior.d6p',
                 '1d_exterior_CalciumSilicateBoard_39_125_705_25.d6p',
                 '1d_exterior_CalciumSilicateBoard_39_125_705_50.d6p',
                 '1d_exterior_CalciumSilicateBoard_39_125_705_100.d6p',
                 '1d_exterior_PolystyreneBoardExpanded_187_559_25.d6p',
                 '1d_exterior_PolystyreneBoardExpanded_187_559_35.d6p',
                 '1d_interior_CalciumSilicateBoard_39_125_705_25.d6p',
                 '1d_interior_CalciumSilicateBoard_39_125_705_50.d6p',
                 '1d_interior_CalciumSilicateBoard_39_125_705_100.d6p',
                 '1d_interior_PolystyreneBoardExpanded_187_559_25.d6p',
                 '1d_interior_PolystyreneBoardExpanded_187_559_35.d6p']
        new_file = os.path.join(folder, 'design', names[index])
        shutil.copyfile(os.path.join(delphin_folder, file), new_file)

    return os.path.join(folder, 'design')


@pytest.fixture()
def mock_insulation_systems(monkeypatch, dummy_systems, delphin_reference_folder, test_folder):
    def mock_return(rows_to_read=None, excel_file=None, folder=None):
        return dummy_systems

    monkeypatch.setattr(inputs, 'insulation_systems', mock_return)

    from_file = os.path.join(test_folder, 'input_sets', 'InsulationSystems.xlsx')
    to_file = os.path.join(delphin_reference_folder, 'InsulationSystems.xlsx')
    shutil.copyfile(from_file, to_file)


@pytest.fixture()
def input_sets():
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test_files', 'input_sets')


@pytest.fixture()
def mock_design_options(monkeypatch):
    def mock_return(folder=None):

        return ['1d_exterior', '1d_interior',
                '1d_exterior_CalciumSilicateBoard_39_125_705_25',
                '1d_exterior_CalciumSilicateBoard_39_125_705_50',
                '1d_exterior_CalciumSilicateBoard_39_125_705_100',
                '1d_exterior_PolystyreneBoardExpanded_187_559_25',
                '1d_exterior_PolystyreneBoardExpanded_187_559_35', ]

    monkeypatch.setattr(inputs, 'design_options', mock_return)


@pytest.fixture(params=[1, 2])
def uvalue_data(test_folder, request):
    folder = os.path.join(test_folder, 'damage_models', f'u_value_{request.param}')

    indoor_temp = weather_parser.ccd_to_list(os.path.join(folder, 'indoor_temperature.ccd'))
    outdoor_temp = weather_parser.ccd_to_list(os.path.join(folder, 'temperature.ccd'))
    heat_loss = delphin_parser.d6o_to_dict(folder, 'heat loss.d6o', len(outdoor_temp))[0]

    return heat_loss, outdoor_temp, indoor_temp


@pytest.fixture(params=[1, 2, 3, 4])
def result_files(tmpdir, test_folder, request):
    temp_folder = tmpdir.mkdir('test')

    result_zip = test_folder + f'/raw_results/delphin_results{request.param}.zip'
    shutil.unpack_archive(result_zip, temp_folder)

    for file in os.listdir(os.path.join(temp_folder, 'delphin_id', 'results')):
        os.rename(os.path.join(temp_folder, 'delphin_id', 'results', file), os.path.join(temp_folder, file))

    return temp_folder


@pytest.fixture()
def design_options(mock_insulation_systems, add_insulation_materials, delphin_reference_folder):
    return inputs.design_options(delphin_reference_folder)


@pytest.fixture()
def mock_copytree(monkeypatch):
    def mockreturn(src, dst):
        return None

    monkeypatch.setattr(shutil, 'copytree', mockreturn)