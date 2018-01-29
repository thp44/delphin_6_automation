__author__ = "Christian Kongsgaard"
__license__ = "MIT"
__version__ = "0.0.1"

# -------------------------------------------------------------------------------------------------------------------- #
# IMPORTS

# Modules:
import mongoengine
from datetime import datetime

# RiBuild Modules:
import delphin_6_automation.nosql.database_collections as collections

# -------------------------------------------------------------------------------------------------------------------- #
# MATERIAL CLASS


class Material(mongoengine.Document):



    added_date = mongoengine.DateTimeField(default=datetime.now)
    material_data = mongoengine.DictField(required=True)

    meta = collections.material_db