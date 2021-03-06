import datetime

__author__ = "Christian Kongsgaard"
__license__ = "MIT"

# -------------------------------------------------------------------------------------------------------------------- #
# IMPORTS

# Modules:
import os
import shutil
import xmltodict
from collections import OrderedDict
import bson
import numpy as np
import typing

# RiBuild Modules:
import delphin_6_automation.database_interactions.db_templates.result_raw_entry as result_db
import delphin_6_automation.database_interactions.db_templates.delphin_entry as delphin_db
import delphin_6_automation.database_interactions.db_templates.material_entry as material_db
from delphin_6_automation.database_interactions.db_templates import sample_entry
from delphin_6_automation.database_interactions.db_templates import result_processed_entry
from delphin_6_automation.delphin_setup import damage_models
from delphin_6_automation.database_interactions import material_interactions
from delphin_6_automation.database_interactions import weather_interactions
import delphin_6_automation.delphin_setup.delphin_permutations as permutations
from delphin_6_automation.file_parsing import delphin_parser
from delphin_6_automation.file_parsing import weather_parser
from delphin_6_automation.logging import ribuild_logger

# Logger
logger = ribuild_logger.ribuild_logger()


# -------------------------------------------------------------------------------------------------------------------- #
# DELPHIN FUNCTIONS AND CLASSES


def upload_delphin_to_database(delphin_file: str, queue_priority: int) -> delphin_db.Delphin.id:
    """
    Uploads a Delphin file to a database.rst.

    :param delphin_file: Path to a Delphin 6 project file
    :param queue_priority: Queue priority for the simulation
    :return: Database entry id
    """

    delphin_dict = delphin_parser.dp6_to_dict(delphin_file)
    entry_id = upload_delphin_dict_to_database(delphin_dict, queue_priority)

    return entry_id


def upload_delphin_dict_to_database(delphin_dict: dict, queue_priority: int) -> delphin_db.Delphin.id:
    """
    Uploads a Delphin file to a database.rst.

    :param delphin_dict: Dict with a Delphin 6 project
    :param queue_priority: Queue priority for the simulation
    :return: Database entry id
    """

    entry = delphin_db.Delphin()
    entry.queue_priority = queue_priority
    delphin_dict = weather_interactions.update_short_wave_condition(delphin_dict)
    entry.dp6_file = delphin_dict
    entry.materials = material_interactions.find_material_ids(material_interactions.list_project_materials(entry))
    entry.dimensions = get_delphin_project_dimension(delphin_dict)
    entry.save()

    logger.debug(f'Uploaded Delphin project with ID: {entry.id} to database')

    return entry.id


def get_delphin_project_dimension(delphin_dict: dict):
    try:
        if len(delphin_dict['DelphinProject']['Discretization']) > 2:
            return 3
        elif len(delphin_dict['DelphinProject']['Discretization']['YSteps']['#text'].split(' ')) > 1:
            return 2
        else:
            return 1

    except KeyError:
        return 1


def download_delphin_entry(delphin_document: delphin_db.Delphin, path: str) -> bool:
    """
    Converts a database.rst entry to Delphin 6 project file.

    :param delphin_document: Database entry id.
    :param path: Path to where the files should be written.
    :return: True
    """

    delphin_dict = dict(delphin_document.dp6_file)
    xmltodict.unparse(delphin_dict, output=open(os.path.join(path,
                                                             f'{str(delphin_document.id)}.d6p'), 'w'), pretty=True)

    logger.debug(f'Downloaded Delphin project with ID: {delphin_document.id} to {path}')

    return True


def upload_results_to_database(path_: str, delete_files: bool = True, result_length=None) -> str:
    """
    Uploads the results from a Delphin simulation.

    :param path_: folder path containing the result files
    :param delete_files: if True the result folder will be deleted. Default is True
    :return: Result entry id
    """

    id_ = os.path.split(path_)[1]
    delphin_entry = delphin_db.Delphin.objects(id=id_).first()
    result_dict = {}
    result_path = os.path.join(path_, 'results')
    geometry_dict = {}

    for result_file in os.listdir(result_path):
        if result_file.endswith('.d6o'):
            result_name = result_file.split('.')[0]
            result_dict[result_name] = {'result': [], 'meta': []}
            (result_dict[result_name]['result'],
             result_dict[result_name]['meta']) = delphin_parser.d6o_to_dict(result_path, result_file, result_length)

        elif result_file.endswith('.g6a'):
            geometry_dict = delphin_parser.g6a_to_dict(result_path, result_file)

    entry = result_db.Result()

    entry.delphin = delphin_entry

    entry.geometry_file = geometry_dict
    entry.results.put(bson.BSON.encode(result_dict))

    try:
        last_meta: dict = result_dict[list(result_dict.keys())[0]]['meta']
        entry.simulation_started = last_meta['created']
        entry.geometry_file_hash = last_meta['geo_file_hash']
    except IndexError:
        pass

    entry.save()

    logger.debug(f'Uploaded raw results with ID: {entry.id}')

    # Add results reference to Delphin entry
    delphin_entry.update(set__results_raw=entry)

    logger.debug(f'Added raw result with ID: {entry.id} to Delphin project with ID: {delphin_entry.id}')

    if delete_files:
        shutil.rmtree(path_, ignore_errors=True)
        logger.debug(f'Deleted {path_}')

    return entry.id


def download_result_files(result_obj: result_db.Result, download_path: str) -> bool:
    """
    Writes out all the result files from a result database entry.

    :param result_obj: Raw result entry
    :param download_path: Where to write the files
    :return: True
    """

    result_dict: dict = bson.BSON.decode(result_obj.results.read())
    result_path = download_path + '/results'

    if not os.path.exists(result_path):
        os.mkdir(result_path)
    else:
        shutil.rmtree(result_path)
        os.mkdir(result_path)

    delphin_parser.dict_to_g6a(dict(result_obj.geometry_file), result_path)

    for result_name in result_dict.keys():
        delphin_parser.dict_to_d6o(result_dict[result_name], os.path.join(result_path, result_name),
                                   result_obj.simulation_started, result_obj.geometry_file['name'],
                                   result_obj.geometry_file_hash)

    logger.debug(f'Downloaded raw results with ID: {result_obj.id}')

    return True


def permutate_entry_layer_width(original_id, layer_material, widths, queue_priority):
    delphin_document = delphin_db.Delphin.objects(id=original_id).first()
    delphin_dict = dict(delphin_document.dp6_file)
    modified_ids = []

    for width in widths:
        modified_dict = permutations.change_layer_width(delphin_dict, layer_material, width)
        modified_ids.append(str(upload_delphin_dict_to_database(modified_dict, queue_priority)))

    return modified_ids


def permutate_entry_layer_material(original_id, original_material, new_materials, queue_priority):
    delphin_document = delphin_db.Delphin.objects(id=original_id).first()
    delphin_dict = dict(delphin_document.dp6_file)
    modified_ids = []

    for new_material in new_materials:

        if isinstance(new_material, str):
            material = material_db.Material.objects(material_name=new_material).first()

            material_dict = OrderedDict((('@name', f'{material.material_name} [{material.material_id}]'),
                                         ('@color', str(material.material_data['IDENTIFICATION-COLOUR'])),
                                         ('@hatchCode', str(material.material_data['IDENTIFICATION-HATCHING'])),
                                         ('#text', '${Material Database}/' +
                                          str(material.material_data['INFO-FILE'].split('/')[-1]))
                                         )
                                        )
            modified_dict = permutations.change_layer_material(delphin_dict, original_material, material_dict)
            modified_ids.append(upload_delphin_dict_to_database(modified_dict, queue_priority))

        elif isinstance(new_material, int):
            material = material_db.Material.objects(material_id=new_material).first()

            material_dict = OrderedDict((('@name', f'{material.material_name} [{material.material_id}]'),
                                         ('@color', str(material.material_data['IDENTIFICATION-COLOUR'])),
                                         ('@hatchCode', str(material.material_data['IDENTIFICATION-HATCHING'])),
                                         ('#text', '${Material Database}/' +
                                          str(material.material_data['INFO-FILE'].split('/')[-1]))
                                         )
                                        )
            modified_dict = permutations.change_layer_material(delphin_dict, original_material, material_dict)
            modified_ids.append(upload_delphin_dict_to_database(modified_dict, queue_priority))

    return modified_ids


def permutate_entry_orientation(original_id, orientation_list, queue_priority):
    delphin_document = delphin_db.Delphin.objects(id=original_id).first()
    delphin_dict = dict(delphin_document.dp6_file)
    modified_ids = []

    for orientation in orientation_list:
        modified_dict = permutations.change_orientation(delphin_dict, orientation)
        modified_ids.append(str(upload_delphin_dict_to_database(modified_dict, queue_priority)))

    return modified_ids


def permutate_entry_weather(original_id, weather_stations, queue_priority):
    delphin_document = delphin_db.Delphin.objects(id=original_id).first()
    delphin_dict = dict(delphin_document.dp6_file)
    modified_ids = []

    for station in weather_stations['stations']:
        print(station)
        print(weather_stations['years'])
        for index in range(len(weather_stations['years'])):
            print(weather_stations['years'][index])
            modified_id = str(upload_delphin_dict_to_database(delphin_dict, queue_priority))
            weather_interactions.assign_weather_by_name_and_years(
                modified_id, station, weather_stations['years'][index])
            modified_ids.append(modified_id)

    return modified_ids


def permutate_entry_boundary_coefficient(original_id, boundary_condition, coefficient_name,
                                         coefficient_list, queue_priority):
    delphin_document = delphin_db.Delphin.objects(id=original_id).first()
    delphin_dict = dict(delphin_document.dp6_file)
    modified_ids = []

    for coefficient in coefficient_list:
        modified_dict = permutations.change_boundary_coefficient(delphin_dict, boundary_condition,
                                                                 coefficient_name, coefficient)
        modified_ids.append(str(upload_delphin_dict_to_database(modified_dict, queue_priority)))

    return modified_ids


def permutate_entry_simulation_length(original_id, length_list, unit_list, queue_priority):
    delphin_document = delphin_db.Delphin.objects(id=original_id).first()
    delphin_dict = dict(delphin_document.dp6_file)
    modified_ids = []

    for unit in unit_list:
        for length in length_list:
            modified_dict = permutations.change_simulation_length(delphin_dict, length, unit)
            modified_ids.append(str(upload_delphin_dict_to_database(modified_dict, queue_priority)))

    return modified_ids


def change_entry_simulation_length(sim_id, length, unit):
    """Change the simulation length of a Delphin project"""

    delphin_document = delphin_db.Delphin.objects(id=sim_id).first()
    delphin_dict = dict(delphin_document.dp6_file)
    permutations.change_simulation_length(delphin_dict, length, unit)

    delphin_document.update(set__dp6_file=delphin_dict)

    logger.debug(f'Changed simulation length to {length} {unit} for Delphin project with ID: {sim_id}')

    return delphin_document.id


def check_delphin_file(delphin_dict: dict):
    """
    Checks if a Delphin project file is valid for simulation.

    :return:
    """

    error = False

    # 1D or 2D?
    if len(delphin_dict['DelphinProject']['Discretization']) > 2:
        logger.warning('Delphin Project File is 3 dimensional. Permutations are not guaranteed to work!')
    elif len(delphin_dict['DelphinProject']['Discretization']) > 1:
        logger.warning('Delphin Project File is 2 dimensional. Permutations are not guaranteed to work!')
    else:
        logger.info('Delphin Project File is 1 dimensional.')

    # Is materials correct?
    material_error = False

    for material in delphin_dict['DelphinProject']['Materials']['MaterialReference']:
        material_id = material['@name'][-5:]
        if not material_id.startswith('[') and material_id.endswith(']'):
            logger.error(f'Material name should end with: [XXX], where XXX is the Delphin Material ID. '
                         f'Material ended with: {material_id}')
            material_error = True

        try:
            material_int = int(material_id[1:-1])
        except ValueError:
            logger.error(f'Material name should end with: [XXX], where XXX is the Delphin Material ID. '
                         f'Delphin Material ID {material_id} was not an integer, but a: {type(material_id[1:-1])}')
            material_error = True

    if not material_error:
        logger.info('Material check passed')
    else:
        error = True
        logger.error('Material check did not pass')

    # Is interface correct?
    interface_error = False

    interfaces = delphin_dict['DelphinProject']['Conditions']['Interfaces']['Interface']

    if not isinstance(interfaces, list):
        logger.error(f'Only {interfaces["@name"]} assigned. Both an interior and exterior surface should be assigned.')
        interface_error = True

    else:
        for interface in interfaces:
            if interface['@name'].lower() == 'indoor surface' or interface['@name'].lower() == 'interior surface':

                if interface['@type'] != 'Detailed':
                    logger.error(
                        f'Interior interface should be: Detailed. Interface type given was: {interface["@type"]}')
                    interface_error = True

                interior_boundaries = ['IndoorHeatConduction', 'IndoorVaporDiffusion']
                for bc_ref in interface['BCReference']:
                    try:
                        index = interior_boundaries.index(bc_ref.split(':')[-1])
                        interior_boundaries.pop(index)
                    except ValueError:
                        logger.error(f'Boundary condition not part of: {interior_boundaries}. '
                                     f'Boundary condition given was: {bc_ref.split(":")[-1]}')
                        interface_error = True

            elif interface['@name'].lower() == 'outdoor surface' or interface['@name'].lower() == 'exterior surface':

                if interface['@type'] != 'Detailed':
                    logger.error(
                        f'Exterior interface should be: Detailed. Interface type given was: {interface["@type"]}')
                    interface_error = True

                exterior_boundaries = ['OutdoorHeatConduction', 'OutdoorVaporDiffusion', 'OutdoorShortWaveRadiation',
                                       'OutdoorLongWaveRadiation', 'OutdoorWindDrivenRain']
                for bc_ref in interface['BCReference']:
                    try:
                        index = exterior_boundaries.index(bc_ref.split(':')[-1])
                        exterior_boundaries.pop(index)
                    except ValueError:
                        logger.error(f'Boundary condition not part of: {exterior_boundaries}. '
                                     f'Boundary condition given was: {bc_ref.split(":")[-1]}')
                        interface_error = True

            else:
                logger.error(f'Could not recognize interface name.\n'
                             f'Interior surface should be named: indoor surface or interior surface.\n'
                             f'Exterior surface should be named: outdoor surface or exterior surface.\n'
                             f'Named given was: {interface["@name"].lower()}')
                interface_error = True

    if not interface_error:
        logger.info('Interface check passed')
    else:
        error = True
        logger.error('Interface check did not pass')

    # Is climate conditions correct?
    climate_error = False

    for climate_condition in delphin_dict['DelphinProject']['Conditions']['ClimateConditions']['ClimateCondition']:
        if climate_condition['@kind'] != 'TabulatedData':
            logger.error(f'Climate condition kind should be TabulatedData. '
                         f'Given kind was: {climate_condition["@kind"]}')
            climate_error = True

        if climate_condition['IBK:Flag'][1]['#text'] != 'false':
            logger.error(f'Climate condition should not use ExtendData. '
                         f'Given value was: {climate_condition[2]["#text"]}')
            climate_error = True

    if not climate_error:
        logger.info('Climate condition check passed')
    else:
        error = True
        logger.error('Climate condition check did not pass')

    # Is boundary conditions correct?
    boundary_error = False

    for boundary_condition in delphin_dict['DelphinProject']['Conditions']['BoundaryConditions']['BoundaryCondition']:
        if boundary_condition['@type'] == 'HeatConduction':
            if boundary_condition['@kind'] != 'Exchange':
                logger.error(f'Heat conduction should be of the boundary condition kind: Exchange. '
                             f'Given kind was: {boundary_condition["@kind"]}')
                boundary_error = True

        elif boundary_condition['@type'] == 'VaporDiffusion':
            if boundary_condition['@kind'] != 'Exchange':
                logger.error(f'Vapor diffusion should be of the boundary condition kind: Exchange. '
                             f'Given kind was: {boundary_condition["@kind"]}')
                boundary_error = True

        elif boundary_condition['@type'] == 'WindDrivenRain':
            if boundary_condition['@kind'] != 'ImposedFlux':
                logger.error(f'Wind driven rain should be of the boundary condition kind: ImposedFlux. '
                             f'Given kind was: {boundary_condition["@kind"]}')
                boundary_error = True

        elif boundary_condition['@type'] == 'ShortWaveRadiation':
            if boundary_condition['@kind'] != 'ImposedFlux':
                logger.error(f'Short wave radiation should be of the boundary condition kind: ImposedFlux. '
                             f'Given kind was: {boundary_condition["@kind"]}')
                boundary_error = True

        elif boundary_condition['@type'] == 'LongWaveRadiation':
            if boundary_condition['@kind'] != 'LongWaveComponents':
                logger.error(f'Long wave radiation should be of the boundary condition kind: LongWaveComponents. '
                             f'Given kind was: {boundary_condition["@kind"]}')
                boundary_error = True

    if not boundary_error:
        logger.info('Boundary condition check passed')
    else:
        error = True
        logger.error('Boundary condition check did not pass')

    # Is outputs correct?
    # TODO - To be determined

    return error


def upload_processed_results(folder: str, delphin_id: str, raw_result_id: str,
                             simulation_interrupted: bool=False) -> result_db.Result.id:
    """Process simulation results and upload them to the database"""

    # Paths
    folder = os.path.join(folder, 'results')
    weather_path = os.path.join(os.path.dirname(os.path.dirname(folder)), 'weather')

    # Parse
    exterior_temperature = weather_parser.ccd_to_list(os.path.join(weather_path, 'temperature.ccd'))
    interior_temperature = weather_parser.ccd_to_list(os.path.join(weather_path, 'indoor_temperature.ccd'))

    if simulation_interrupted:
        output_length = None
    else:
        output_length = len(exterior_temperature)

    temperature_mould = delphin_parser.d6o_to_dict(folder, 'temperature mould.d6o',
                                                   output_length)[0]

    relative_humidity_mould = delphin_parser.d6o_to_dict(folder, 'relative humidity mould.d6o',
                                                         output_length)[0]

    temperature_algae = delphin_parser.d6o_to_dict(folder, 'temperature algae.d6o',
                                                   output_length)[0]

    relative_humidity_algae = delphin_parser.d6o_to_dict(folder, 'relative humidity algae.d6o',
                                                         output_length)[0]

    heat_loss = delphin_parser.d6o_to_dict(folder, 'heat loss.d6o',
                                           output_length)[0]

    logger.debug(f'Collected simulation result data for Delphin project with ID: {delphin_id}')

    # Upload
    result_entry = result_processed_entry.ProcessedResult()
    raw_result_doc = result_db.Result.objects(id=raw_result_id).first()
    delphin_doc = delphin_db.Delphin.objects(id=delphin_id).first()

    result_entry.delphin = delphin_doc
    result_entry.results_raw = raw_result_doc

    if len(relative_humidity_mould) < len(temperature_mould):
        temperature_mould = temperature_mould[:len(relative_humidity_mould)]
    elif len(temperature_mould) < len(relative_humidity_mould):
        relative_humidity_mould = relative_humidity_mould[:len(temperature_mould)]

    mould = damage_models.mould_index(relative_humidity_mould, temperature_mould,
                                      draw_back=1, sensitivity_class=3, surface_quality=0)

    result_entry.mould.put(np.asarray(mould).tobytes())
    result_entry.heat_loss.put(np.array(heat_loss).tobytes())
    #result_entry.algae.put(np.array(damage_models.algae(relative_humidity_algae, temperature_algae)).tobytes())
    result_entry.u_value = damage_models.u_value(heat_loss,
                                                 exterior_temperature[:len(heat_loss)],
                                                 interior_temperature[:len(heat_loss)])

    result_entry.thresholds = {'mould': max(mould),
                               'heat_loss': sum(heat_loss)}

    result_entry.save()
    logger.debug(f'Uploaded processed result with ID: {result_entry.id}')

    # Cross reference
    delphin_doc.update(set__result_processed=result_entry)
    raw_result_doc.update(set__result_processed=result_entry)

    logger.debug(f'Added processed result entry to Delphin project with ID: {delphin_id}')
    logger.debug(f'Added processed result entry to raw result entry with ID: {raw_result_id}')

    return result_entry.id


def add_sampling_dict(delphin_id: str, sample_data: dict) -> str:
    """Adds a sample metadata dict to a Delphin project in the database."""

    entry = delphin_db.Delphin.objects(id=delphin_id).first()
    entry.update(set__sample_data=sample_data)

    logger.debug(f'Added sample metadata to Delphin project with ID: {delphin_id}')

    return entry.id


def change_entry_kirchhoff_potential(sim_id, set_to):
    """Change the Kirchhoff potential of a Delphin project"""

    delphin_document = delphin_db.Delphin.objects(id=sim_id).first()
    delphin_dict = dict(delphin_document.dp6_file)
    permutations.change_kirchhoff_potential(delphin_dict, set_to)

    delphin_document.update(set__dp6_file=delphin_dict)

    logger.debug(f'Changed Kirchhoff potential to {set_to} for Delphin project with ID: {sim_id}')

    return delphin_document.id


def change_entry_solver_relative_tolerance(sim_id, rel_tol):
    """Change the solver relative tolerance of a Delphin project"""

    delphin_document = delphin_db.Delphin.objects(id=sim_id).first()
    delphin_dict = dict(delphin_document.dp6_file)
    permutations.change_solver_relative_tolerance(delphin_dict, rel_tol)

    delphin_document.update(set__dp6_file=delphin_dict)

    logger.debug(f'Changed the solver relative tolerance to {rel_tol} for Delphin project with ID: {sim_id}')

    return delphin_document.id


def set_exceeding_time_limit(sim_id: delphin_db.Delphin.id) -> str:

    entry = delphin_db.Delphin.objects(id=sim_id).first()
    entry.update(set__exceeded_time_limit=True)
    logger.debug(f'Simulation with ID: {sim_id} got flagged as exceeding simulation time limit.')

    return entry.id


def upload_restart_data(folder: str, delphin_id: str) -> str:

    restart_folder = os.path.join(folder, delphin_id, 'var')

    restart_dict = delphin_parser.restart_data(restart_folder)

    delphin_doc = delphin_db.Delphin.objects(id=delphin_id).first()
    delphin_doc.update(set__restart_data=restart_dict)

    return delphin_doc.id


def download_restart_data(delphin_doc: delphin_db.Delphin, folder: str) -> None:

    restart_dict = delphin_doc.restart_data

    var_folder = os.path.join(folder, 'var')

    if not os.path.exists(folder):
        os.mkdir(folder)

    os.mkdir(var_folder)
    delphin_parser.restart_data_to_file(var_folder, restart_dict)

    return None


def set_critical_error(sim_id: delphin_db.Delphin.id) -> str:

    entry = delphin_db.Delphin.objects(id=sim_id).first()

    entry.update(set__critical_error=True)
    logger.debug(f'Simulation with ID: {sim_id} got flagged with critical errors.')

    return entry.id


def upload_design_file(path: str, strategy_id: typing.Optional[str], update_outputs: bool = True,
                       measured_indoor_climate: bool = False) -> bson.ObjectId:

    """
    Uploads a Delphin file to a database.rst.

    :param path: Path to a Delphin 6 project file
    :param strategy_id: Strategy ID
    :return: Database entry id
    """

    delphin_dict = delphin_parser.dp6_to_dict(path)

    entry = delphin_db.Design()

    if strategy_id:
        strategy_doc = sample_entry.Strategy.objects(id=strategy_id).first()
        entry.strategy = strategy_doc

    entry.d6p_file = delphin_dict
    entry.design_name = os.path.split(path)[1].split('.')[0]
    entry.update_outputs = update_outputs
    entry.measured_indoor_climate = measured_indoor_climate
    entry.save()

    logger.debug(f'Uploaded Design project with ID: {entry.id} to database')

    return entry.id


def get_design_by_name(name: str) -> delphin_db.Design:

    design_doc = delphin_db.Design.objects(design_name=name).first()

    return design_doc
