__author__ = "Christian Kongsgaard"
__license__ = 'MIT'

# -------------------------------------------------------------------------------------------------------------------- #
# IMPORTS

# Modules
import numpy as np
import matplotlib.pyplot as plt
import os

# RiBuild Modules
from delphin_6_automation.file_parsing import delphin_parser
# -------------------------------------------------------------------------------------------------------------------- #
# RIBuild


#folder = r'C:\Users\ocni\PycharmProjects\delphin_6_automation\data_process\validation\test\Hans\5cab2aa229a08e2e20fe4c6e\5cab2aa229a08e2e20fe4c6e\results'
#folder_dif = r'C:\Users\ocni\PycharmProjects\delphin_6_automation\data_process\validation\test\Hans\5cab2aa329a08e2e20fe4c6f\5cab2aa329a08e2e20fe4c6f\results'
folder = r'C:\Users\ocni\PycharmProjects\delphin_6_automation\data_process\validation\test\Hans\5cab2aa229a08e2e20fe4c6e - Dir\5cab2aa229a08e2e20fe4c6e\results'
folder_dif = r'C:\Users\ocni\PycharmProjects\delphin_6_automation\data_process\validation\test\Hans\5cab2aa329a08e2e20fe4c6f - Dir\5cab2aa329a08e2e20fe4c6f\results'

temp_mould = 'temperature mould.d6o'
rh_mould = 'relative humidity mould.d6o'
heat_loss = 'heat loss.d6o'


temp = np.array(delphin_parser.d6o_to_dict(folder, temp_mould)[0])
temp_dif = np.array(delphin_parser.d6o_to_dict(folder_dif, temp_mould)[0])

rh = np.array(delphin_parser.d6o_to_dict(folder, rh_mould)[0])
rh_dif = np.array(delphin_parser.d6o_to_dict(folder_dif, rh_mould)[0])

heat = np.array(delphin_parser.d6o_to_dict(folder, heat_loss)[0])
heat_dif = np.array(delphin_parser.d6o_to_dict(folder_dif, heat_loss)[0])

x = np.arange(0, len(heat))

plt.figure()
plt.title('Temperature - Interface')
plt.plot(x, temp, label='Sun: Dir + Dif')
plt.plot(x, temp_dif, label='Sun: Dif + Dif')
plt.legend()


plt.figure()
plt.title('Relative Humidity - Interface')
plt.plot(x, rh, label='Sun: Dir + Dif')
plt.plot(x, rh_dif, label='Sun: Dif + Dif')
plt.legend()


plt.figure()
plt.title('Heat Loss')
plt.plot(x, heat, label='Sun: Dir + Dif')
plt.plot(x, heat_dif, label='Sun: Dif + Dif')
plt.legend()

plt.figure()
plt.title('Heat Loss - Cumulated')
plt.plot(x, np.cumsum(heat), label='Sun: Dir + Dif')
plt.plot(x, np.cumsum(heat_dif), label='Sun: Dif + Dif')
plt.legend()


plt.show()