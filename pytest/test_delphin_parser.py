__author__ = "Christian Kongsgaard"
__license__ = 'MIT'

# -------------------------------------------------------------------------------------------------------------------- #
# IMPORTS

# Modules
import shutil
import os

# RiBuild Modules
from delphin_6_automation.file_parsing import delphin_parser

# -------------------------------------------------------------------------------------------------------------------- #
# RIBuild


def test_cvode_stats(test_folder, tmpdir):
    temp_folder = tmpdir.mkdir('test')
    result_zip = test_folder + '/raw_results/delphin_results.zip'
    shutil.unpack_archive(result_zip, temp_folder)
    integrator_dict = delphin_parser.cvode_stats_to_dict(os.path.join(temp_folder,
                                                                      'delphin_results/log'))

    assert isinstance(integrator_dict, dict)


def test_d6o_to_dict(result_files, request):

    for file in os.listdir(result_files):
        if file.endswith('.d6o'):
            if '4' not in request.node.name:
                result, meta = delphin_parser.d6o_to_dict(result_files, file)
                assert isinstance(result, list)
                assert isinstance(meta, dict)
            else:
                result, meta = delphin_parser.d6o_to_dict(result_files, file, 7*8760)
                assert isinstance(result, list)
                assert len(result) == 7 * 8760
                assert isinstance(meta, dict)