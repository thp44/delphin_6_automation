__author__ = "Christian Kongsgaard"
__license__ = 'MIT'

# -------------------------------------------------------------------------------------------------------------------- #
# IMPORTS

# Modules
import mongoengine
from datetime import datetime

# RiBuild Modules
import delphin_6_automation.database_interactions.database_collections as collections

# -------------------------------------------------------------------------------------------------------------------- #
# RIBuild


class Sample(mongoengine.Document):

    # Meta Data
    added_date = mongoengine.DateTimeField(default=datetime.now)

    # References
    samples = mongoengine.DictField(required=True)
    delphin_ids = mongoengine.ListField(field=mongoengine.StringField())
    iteration = mongoengine.IntField(required=True)
    standard_error = mongoengine.ListField(field=mongoengine.FloatField())

    meta = collections.sample_db