__author__ = "Christian Kongsgaard"
__license__ = 'MIT'

# -------------------------------------------------------------------------------------------------------------------- #
# IMPORTS

# Modules
import os
import time
import sys

# Insert Python Path
source_folder = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, source_folder)

# RiBuild Modules
from delphin_6_automation.logging.ribuild_logger import ribuild_logger
from delphin_6_automation.database_interactions import simulation_interactions

# Logger
logger = ribuild_logger(__name__)

# -------------------------------------------------------------------------------------------------------------------- #
# RIBuild


if __name__ == "__main__":
    logger = ribuild_logger()

    auth_path = '/run/secrets'
    #auth_path = r'C:\Users\ocni\PycharmProjects\delphin_6_automation\test\checks'
    # Setup connection

    try:
        for file in os.listdir(auth_path):
            if file.startswith('hpc_'):
                simulation_interactions.check_simulations(file)

    except Exception as err:
        logger.exception('Error in main')

    finally:
        time.sleep(300)
