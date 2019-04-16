__author__ = "Christian Kongsgaard"
__license__ = 'MIT'

# -------------------------------------------------------------------------------------------------------------------- #
# IMPORTS

# Modules
import os
import sys
import json

source_folder = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, source_folder)

# RiBuild Modules
from delphin_6_automation.logging.ribuild_logger import ribuild_logger
from delphin_6_automation.database_interactions import mongo_setup
from delphin_6_automation.backend import simulation_worker

# -------------------------------------------------------------------------------------------------------------------- #
# RIBuild


if __name__ == "__main__":

    logger = ribuild_logger()
    # Setup connection
    from delphin_6_automation.database_interactions.auth import validation as auth_dict

    server = mongo_setup.global_init(auth_dict)

    try:

        folder = r'C:\Users\ocni\PycharmProjects\delphin_6_automation\data_process\validation\test\data'

        simulation_worker.docker_worker('local', folder)

    except Exception as err:
        logger.exception('Error in main')

    finally:
        mongo_setup.global_end_ssh(server)
