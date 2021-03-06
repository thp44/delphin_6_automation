__author__ = "Christian Kongsgaard"
__license__ = 'MIT'

# -------------------------------------------------------------------------------------------------------------------- #
# IMPORTS

# Modules
import pytest
import numpy as np

# RiBuild Modules
from delphin_6_automation.delphin_setup import weather_modeling
from delphin_6_automation.file_parsing import weather_parser

# -------------------------------------------------------------------------------------------------------------------- #
# TEST WEATHER MODELS


@pytest.mark.skip('Catch ration model is not implemented correctly')
def test_rain_model_1(test_folder):

    rain = weather_parser.ccd_to_list(test_folder + '/weather/vertical_rain.ccd')
    wind_speed = weather_parser.ccd_to_list(test_folder + '/weather/wind_speed.ccd')
    wind_direction = weather_parser.ccd_to_list(test_folder + '/weather/wind_direction.ccd')
    wall_location = {'height': 5.0, 'width': 5.0}
    wdr = weather_modeling.driving_rain(rain, wind_direction, wind_speed, wall_location, 90, 0)

    assert rain == wdr


def test_rain_model_2(test_folder):

    rain = weather_parser.ccd_to_list(test_folder + '/weather/vertical_rain.ccd')
    wind_speed = weather_parser.ccd_to_list(test_folder + '/weather/wind_speed.ccd')
    wind_direction = weather_parser.ccd_to_list(test_folder + '/weather/wind_direction.ccd')
    wall_location = {'height': 5.0, 'width': 5.0}
    wdr = weather_modeling.driving_rain(rain, wind_direction, wind_speed, wall_location, 90, 0, 1)

    assert rain == wdr


def test_solar_radiation(test_folder):

    # TODO - Create some assertments
    diff_rad = np.array(weather_parser.ccd_to_list(test_folder + '/weather/diffuse_radiation.ccd'))
    dir_rad = np.array(weather_parser.ccd_to_list(test_folder + '/weather/direct_radiation.ccd'))
    radiation = diff_rad + dir_rad
    short_wave = weather_modeling.short_wave_radiation(radiation, -2.083, 57.167, 0, 230)
