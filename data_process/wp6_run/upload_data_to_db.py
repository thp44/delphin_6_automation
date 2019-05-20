__author__ = "Christian Kongsgaard"
__license__ = 'MIT'

# -------------------------------------------------------------------------------------------------------------------- #
# IMPORTS

# Modules
import os
import json

# RiBuild Modules
from delphin_6_automation.database_interactions import mongo_setup
from delphin_6_automation.database_interactions.auth import auth_dict
from delphin_6_automation.database_interactions import weather_interactions
from delphin_6_automation.database_interactions import delphin_interactions
from delphin_6_automation.database_interactions import material_interactions
from delphin_6_automation.database_interactions import sampling_interactions
from delphin_6_automation.database_interactions.db_templates import sample_entry
from delphin_6_automation.sampling import sampling

# -------------------------------------------------------------------------------------------------------------------- #
# RIBuild

server = mongo_setup.global_init(auth_dict)


def upload_materials(folder):

    print('Uploading Materials')

    for file in os.listdir(folder):
        material_interactions.upload_material_file(f'{folder}/{file}')


def upload_weather(folder):
    weather_file = r'C:\Users\ocni\PycharmProjects\delphin_6_automation\data_process\wp6_run\inputs\weather_stations.txt'

    with open(weather_file, 'r') as file:
        weather_stations = [name.strip() for name in file.readlines()]

    print('Uploading Weather\n')
    for station in weather_stations:
        print(f'\t{station}')
        weather_interactions.upload_weather_to_db(os.path.join(folder, station))


def create_strategy(folder):
    sampling.create_sampling_strategy(folder, folder)


def upload_strategy(folder):
    strategy = os.path.join(folder, 'sampling_strategy.json')

    with open(strategy) as file:
        data = json.load(file)

    sampling_interactions.upload_sampling_strategy(data)


def upload_designs(folder):
    strategy = sample_entry.Strategy.objects().first()

    for file in os.listdir(folder):
        delphin_interactions.upload_design_file(os.path.join(folder, file), strategy.id)


#upload_weather(r'U:\RIBuild\Weather Data')
#upload_materials(r'C:\Program Files\IBK\Delphin 6.0\resources\DB_materials')
create_strategy(r'C:\Users\ocni\PycharmProjects\delphin_6_automation\data_process\wp6_run\inputs')
#upload_strategy(r'C:\Users\ocni\PycharmProjects\delphin_6_automation\data_process\wp6_run\inputs')
#upload_designs(r'C:\Users\ocni\PycharmProjects\delphin_6_automation\data_process\wp6_run\inputs\design')

mongo_setup.global_end_ssh(server)
