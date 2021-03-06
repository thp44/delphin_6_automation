__author__ = "Thomas Perkov"
__license__ = 'MIT'

# -------------------------------------------------------------------------------------------------------------------- #
# IMPORTS

# Modules:
import os
import logging
import sys

# RiBuild Modules:
import delphin_6_automation.database_interactions.mongo_setup as mongo_setup
from delphin_6_automation.database_interactions.auth import auth_dict
from delphin_6_automation.database_interactions import general_interactions
from delphin_6_automation.database_interactions import delphin_interactions
from delphin_6_automation.database_interactions import weather_interactions
from delphin_6_automation.database_interactions.db_templates import delphin_entry as delphin_db
from delphin_6_automation.database_interactions import material_interactions
from delphin_6_automation.file_parsing import delphin_parser
from delphin_6_automation.database_interactions import user_interactions

# -------------------------------------------------------------------------------------------------------------------- #
# DELPHIN PERMUTATION FUNCTIONS

"""
backend user interface:
- Add new simulation(s)
- Monitor the simulation process
- Queue and watch finished simulations
"""


def main():
    print_header()
    config_mongo()
    account = login()
    main_menu(account)


def print_header():
    print('---------------------------------------------------')
    print('|                                                  |')
    print('|           RiBuild EU Research Project            |')
    print('|           for Hygrothermal Simulations           |')
    print('|                                                  |')
    print('|                 WORK IN PROGRESS                 |')
    print('|                 Test Environment                 |')
    print('|                                                  |')
    print('---------------------------------------------------')


def config_mongo():
    mongo_setup.global_init(auth_dict)


def close_connections():
    mongo_setup.global_end_ssh(auth_dict)


def login():
    print('')
    print('------------------- LOGIN -------------------------')

    email = input('What is your email? >').strip().lower()
    account = user_interactions.find_account_by_email(email)

    if not account:
        print(f'Could not find account with email {email}.')
        create = input('Do you which to create a new account? [y/n] >').strip().lower()
        if create == 'y':
            create_account(email)
        else:
            return

    print('Logged in successfully.')
    return account


def create_account(email: str):
    print('')
    print('------------------- REGISTER ----------------------')

    name = input('What is your name? >')

    old_account = user_interactions.find_account_by_email(email)
    if old_account:
        print(f"ERROR: Account with email {email} already exists.")
        return

    return user_interactions.create_account(name, email)


def main_menu(account):
    while True:
        print('')
        print('------------------- MAIN MENU ---------------------')
        print('')
        print("Available actions:")
        print("[a] Add new simulation to queue")
        print("[b] Add new simulation with permutations to queue")
        print("[c] List simulations")
        print("[d] List materials")
        print("[w] List weather")
        print("[t] Test Connection")
        print("[x] Exit")
        print()

        choice = input("> ").strip().lower()

        if choice == 'a':
            [sim_id, *_] = add_to_queue()
            save_ids(sim_id, account)

        elif choice == 'b':
            id_list = add_permutations_to_queue()
            save_ids(id_list, account)

        elif choice == 'c':
            view_simulations(account)

        elif choice == 'd':
            view_material_data()

        elif choice == 'w':
            view_weather_data()

        elif not choice or choice == 'x':
            close_connections()
            print("see ya!")
            sys.exit()


def view_simulations(account):
    while True:
        print('')
        print('------------------ SIMULATIONS --------------------')
        print('')
        print("Available actions:")
        print("[l] List simulations")
        print("[f] Find simulation")
        print("[d] Download simulations")
        print("[a] Add new simulation to queue")
        print("[b] Add new simulation with permutations to queue")
        print("[x] Return to main menu")
        print('')

        choice = input("> ").strip().lower()

        if choice == 'l':
            user_interactions.list_user_simulations(account)

        elif choice == 'f':
            find_simulations()

        elif choice == 'd':
            download_simulation_result()

        elif choice == 'a':
            [sim_id, *_] = add_to_queue()
            save_ids(sim_id, account)

        elif choice == 'b':
            id_list = add_permutations_to_queue()
            save_ids(id_list, account)

        elif choice == 'x':
            return None


def get_simulation_status(id_):
    delphin_document = delphin_db.Delphin.objects(id=id_).first()

    if delphin_document.simulating:
        status = "Is currently being simulated."
    elif delphin_document.simulated:
        status = f"Was simulated on {delphin_document.simulated}"
    else:
        status = 'Is waiting to be simulated'

    print('')
    print(f'Simulation with ID: {id_}\n'
          f'\tAdded: {delphin_document.added_date}\n'
          f'\t{status}')

    if status == f"Was simulated on {delphin_document.simulated}":
        print('')
        download = input("Do you wish to download the results? y/n >")

        if download == 'y':
            print(f'Simulation result will be saved on the Desktop as in the folder: {id_}')
            user_desktop = os.path.join(os.environ["HOMEPATH"], "Desktop")
            general_interactions.download_raw_result(delphin_document.results_raw.id, user_desktop + f'/{id_}')


def find_simulations():
    print('')
    print("The simulations will be identified by their database ID")

    database_ids = input("What is the database ID?\n"
                         "If more than 1 simulation is wished, then the IDs have to be separated with a comma. >")
    database_ids = [id_.strip()
                    for id_ in database_ids.split(',')]
    for id_ in database_ids:
        get_simulation_status(id_)


def view_material_data():
    while True:
        print('')
        print('------------------- MATERIALS ---------------------')
        print('')
        print("Available actions:")
        print("[l] List materials")
        print("[m] Add Delphin material to the database")
        print("[d] Download material")
        print("[x] Return to main menu")
        print('')

        choice = input("> ").strip().lower()

        if choice == 'l':
            print('Looking up the weather stations may take some time. Please wait.')
            print('The RIBuild Database currently contains the following materials:\n')
            materials = general_interactions.list_materials()
            general_interactions.print_material_dict(materials)

        elif choice == 'm':
            add_delphin_material_to_db()

        elif choice == 'd':
            download_delphin_material()

        elif choice == 'x':
            return None


def test_connection():
    print('if materials are printing the sh#t is running:\n')
    materials = general_interactions.list_materials()
    general_interactions.print_material_dict(materials)


def view_weather_data():
    while True:
        print('')
        print('------------------ WEATHER DATA -------------------')
        print('')
        print("[l] List weather stations")
        print("[x] Return to main menu")
        print('')

        choice = input("> ").strip().lower()

        if choice == 'l':
            print('Looking up the weather stations may take some time. Please wait.')
            print('The RIBuild Database currently contains the following weather stations:\n')
            weather_stations = general_interactions.list_weather_stations()
            general_interactions.print_weather_stations_dict(weather_stations)

        elif choice == 'x':
            return None


def add_to_queue():
    delphin_file = ' '
    while not os.path.isfile(delphin_file):
        delphin_file = str(input("File path for the Delphin file >"))
        if not os.path.isfile(delphin_file):
            print('Could not find file. Please try again')

    priority = str(input("Simulation Priority - high, medium or low >"))
    climate_class = str(input('What climate class should be assigned? A or B can be chosen. >'))

    if check_delphin_file(delphin_file):
        sim_id = general_interactions.add_to_simulation_queue(delphin_file, priority)
        weather_interactions.assign_indoor_climate_to_project(sim_id, climate_class)
        location_name, years = add_weather_to_simulation(sim_id)

        change_year = input('Do you wish to change the simulation length to match the weather input? [Y/n] >')
        if change_year != 'n':
            delphin_interactions.change_entry_simulation_length(sim_id, len(years), 'a')
            print(f'Simulation length changed to {len(years)} a')

        print('Simulation ID:', sim_id,
              '\nTo retrieve the results of a simulation the simulation ID is needed.')

        return sim_id, general_interactions.queue_priorities(priority), location_name, years, climate_class

    else:
        return None


def add_permutations_to_queue():
    print('First upload the original file. Afterwards permutations can be chosen.')

    id_list = []
    original_id, priority, location_name, years, climate_class = add_to_queue()
    id_list.append(original_id)
    modified_ids, choice = list_permutation_options(original_id, priority)

    if choice != 'c':
        for id_ in modified_ids:
            weather_interactions.assign_weather_by_name_and_years(id_, location_name, years)
            weather_interactions.assign_indoor_climate_to_project(id_, climate_class)

    id_list.extend(modified_ids)

    return id_list


def save_ids(simulation_id, account):
    if not simulation_id:
        return

    else:
        if isinstance(simulation_id, list):
            for id_ in simulation_id:
                user_interactions.add_simulation_to_user(account, delphin_db.Delphin.objects(id=id_).first())
        else:
            user_interactions.add_simulation_to_user(account, delphin_db.Delphin.objects(id=simulation_id).first())

        save = str(input('Save Simulation ID to text file? (y/n)'))
        if save == 'y':
            print('Simulation will be saved on the Desktop as simulation_id.txt ')
            user_desktop = os.path.join(os.environ["HOMEPATH"], "Desktop")
            id_file = open(user_desktop + '/simulation_id.txt', 'w')

            if not isinstance(simulation_id, list):
                id_file.write(str(simulation_id))

            else:
                for id_ in simulation_id:
                    id_file.write(str(id_) + '\n')

            id_file.close()

        else:
            print('Simulation ID was not saved.')
            return


def check_delphin_file(delphin_file):
    delphin_dict = delphin_parser.dp6_to_dict(delphin_file)

    if delphin_interactions.check_delphin_file(delphin_dict):
        delphin_logger = logging.getLogger("delphin_6_automation.database_interactions.delphin_interactions")
        log_file = delphin_logger.handlers[0].baseFilename

        print('\n------------------- ERROR -------------------------')
        print('Uploaded Delphin Project does not comply with the guidelines for the simulation system.')
        print(f'An error log has been created and can be found here:\n{log_file}\n')

        return False

    else:
        return True


def add_weather_to_simulation(simulation_id):
    location_name = str(input("What weather station should be used? >"))
    years = input("Which years should be used?.\n"
                  "If more than 1 year is wished, then the values have to be separated with a comma. >")
    years = [int(year.strip())
             for year in years.split(',')]
    weather_interactions.assign_weather_by_name_and_years(simulation_id, location_name, years)

    return location_name, years


def list_permutation_options(original_id, priority):
    print('-------------- PERMUTATION OPTIONS ----------------')
    print('')
    print("Available options:")
    print("[a] Change layer width")
    print("[b] Change layer material")
    print("[c] Change weather")
    print("[d] Change wall orientation")
    print("[e] Change boundary coefficient")
    print("[f] Change simulation length")
    print("[x] Exit")
    print()

    choice = input("> ").strip().lower()

    if choice == 'a':
        ids = layer_width_permutation(original_id, priority)

    elif choice == 'b':
        ids = layer_material_permutation(original_id, priority)

    elif choice == 'c':
        ids = weather_permutation(original_id, priority)

    elif choice == 'd':
        ids = wall_permutation(original_id, priority)

    elif choice == 'e':
        ids = boundary_permutation(original_id, priority)

    elif choice == 'f':
        ids = simulation_length_permutation(original_id, priority)

    else:
        ids = ''

    return ids, choice


def layer_width_permutation(simulation_id, priority):
    print('')
    print("The layer will be identified by the name of the material in the layer.")

    layer_material = input("What is the name of the material? >")
    widths = input("Input wished layer widths in meter.\n"
                   "If more than 1 width is wished, then the values have to be separated with a comma. >")
    widths = [float(width.strip())
              for width in widths.split(',')]

    print('')
    print(f'Following values given: {widths}')
    print('')

    ids = delphin_interactions.permutate_entry_layer_width(simulation_id, layer_material, widths, priority)

    return ids


def layer_material_permutation(original_id, priority):
    print('')
    print("The layer will be identified by the name of the material in the layer.")

    layer_material = input("What is the name of the original material you want to change? >")
    material_list = input("Input wished layer materials.\n"
                          "If more than 1 material is wished, then the values have to be separated with a comma. >")
    materials = []
    for material in material_list.split(','):
        try:
            materials.append(int(material.strip()))
            print('Material identified by ID')
        except ValueError:
            materials.append(material.strip())
            print('Material identified by Material Name')

    print('')
    print(f'Following values given: {materials}')
    print('')

    ids = delphin_interactions.permutate_entry_layer_material(original_id, layer_material, materials, priority)

    return ids


def weather_permutation(original_id, priority):
    print('')

    weather_stations = {'years': [], 'stations': []}

    stations = input("Input wished weather stations.\n"
                     "If more than 1 weather station with the same years is wished, "
                     "then the weather station have to be separated with a comma. >")

    for station in stations.split(','):
        weather_stations['stations'].append(station.strip())

    year_list = input(f"Input wished years for the following weather stations: {stations}.\n"
                      f"If more than 1 year is wished, then the years have to be separated with a comma. >")

    year_list = [[int(year.strip())
                  for year in years.strip().split(' ')]
                 for years in year_list.split(',')]

    weather_stations['years'] = year_list

    print('')
    print(f'Following values given: {weather_stations}')
    print('')

    return delphin_interactions.permutate_entry_weather(original_id, weather_stations, priority)


def wall_permutation(original_id, priority):
    print('')

    orientation_list = input("Input wished orientations.\n"
                             "If more than 1 orientation is wished, "
                             "then the values have to be separated with a comma. >")
    orientation_list = [int(orientation.strip())
                        for orientation in orientation_list.split(',')]

    print('')
    print(f'Following values given: {orientation_list}')
    print('')

    return delphin_interactions.permutate_entry_orientation(original_id, orientation_list, priority)


def boundary_permutation(original_id, priority):
    print('')

    boundary_condition = input("Input wished boundary condition to change. >")
    coefficient_name = input("Input wished climate coefficient to change. >")
    coefficient_list = input("Input wished boundary coefficients.\n"
                             "If more than 1 coefficient is wished, "
                             "then the values have to be separated with a comma. >")
    coefficient_list = [float(coefficient.strip())
                        for coefficient in coefficient_list.split(',')]

    print('')
    print(f'Following values given: {coefficient_list}')
    print('')

    return delphin_interactions.permutate_entry_boundary_coefficient(original_id, boundary_condition, coefficient_name,
                                                                     coefficient_list, priority)


def list_latest_added_simulations():
    documents = delphin_db.Delphin.objects.order_by("added_date")

    for document in documents:
        print(f"ID: {document.id} - Added: {document.added_date} - With priority: {document.queue_priority}")


def add_delphin_material_to_db():
    user_input = input("Please type the path a .m6 file or a folder with multiple files: ")
    id_ = material_interactions.upload_material_file(user_input)
    print(f'\nMaterial was upload with ID: {id_}')


def download_delphin_material():
    # TODO - download_delphin_material
    print('Not implemented')
    return


def download_simulation_result():
    print('')
    choice = input('Do you wish to download a [s]ingle result or [m]ultiple? >')

    if choice == 's':
        download_single_result()
    elif choice == 'm':
        download_result_from_file()
    else:
        return


def download_result_from_file():
    print('')
    file_path = str(input('Path to text file with simulation IDs >'))
    download_path = str(input('The path to which the results should be downloaded? >'))

    file = open(file_path, 'r')
    lines = file.readlines()
    file.close()

    for line in lines:
        sim_id = line.strip()

        if not general_interactions.does_simulation_exists(sim_id):
            print(f'Simulation ID: {sim_id} can not be found in database. Skipping to next ID.')
            pass
        elif general_interactions.is_simulation_finished(sim_id):
            print(f'Downloading: {sim_id}')
            delphin_document = delphin_db.Delphin.objects(id=sim_id).first()
            result_id = delphin_document.results_raw.id
            general_interactions.download_raw_result(result_id, download_path)
            delphin_interactions.download_delphin_entry(delphin_document, f'{download_path}/{result_id}')
        else:
            print(f'Simulation with ID: {sim_id} is not done yet. Skipping to next ID.')
            pass

    print(f'Wanted files are now downloaded to: {download_path}')
    return


def download_single_result():
    print('')

    sim_id = str(input('Simulation ID to retrieve? >'))
    if general_interactions.is_simulation_finished(sim_id):
        print('Simulation is ready to download.')
        download_path = str(input('Download Path? >'))
        delphin_document = delphin_db.Delphin.objects(id=sim_id).first()
        result_id = delphin_document.results_raw.id
        general_interactions.download_raw_result(result_id, download_path)
        delphin_interactions.download_delphin_entry(delphin_document, download_path)
    else:
        print('Simulation is not done yet. Please return later')
        return


def simulation_length_permutation(original_id, priority):
    print('')

    length_list = input("Input wished simulation lengths.\n"
                        "If more than 1 length is wished, then the values have to be separated with a comma. >")
    unit_list = input("Input wished simulation unit.\n"
                      "If more than 1 unit is wished, then the values have to be separated with a comma. >")

    length_list = [int(length.strip())
                   for length in length_list.split(',')]

    unit_list = [unit.strip()
                 for unit in unit_list.split(',')]

    print('')
    print(f'Following simulation values given:\nLengths: {length_list}\nUnits: {unit_list}')
    print('')

    return delphin_interactions.permutate_entry_simulation_length(original_id, length_list, unit_list, priority)
