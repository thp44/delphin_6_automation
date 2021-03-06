__author__ = "Christian Kongsgaard"
__license__ = 'MIT'

# -------------------------------------------------------------------------------------------------------------------- #
# IMPORTS

# Modules
import matplotlib.pyplot as plt
import numpy as np

# RiBuild Modules
from delphin_6_automation.database_interactions import mongo_setup
from delphin_6_automation.database_interactions.auth import auth_2d_1d as auth_dict
from delphin_6_automation.backend import result_extraction
from delphin_6_automation.database_interactions.db_templates import delphin_entry

# -------------------------------------------------------------------------------------------------------------------- #
# RIBuild

server = mongo_setup.global_init(auth_dict)

filtered_entries = delphin_entry.Delphin.objects(simulated__exists=True).filter(sample_data__design_option__dim='1D').only('simulation_time')
gt_day = filtered_entries.filter(simulation_time__gt=84000)
gt_250 = filtered_entries.filter(simulation_time__gt=15000)


def get_time(projects):
    time = []
    for p in projects:
        time.append(p.simulation_time)

    return np.array(time)/60


sim_time = get_time(filtered_entries)
months = 5
users = 6

print()
print('STATS')
print(f'\tCount: {len(sim_time)}')
print(f'\tMin: {np.min(sim_time):.02f}')
print(f'\tMean: {np.mean(sim_time):.02f}')
print(f'\tMax: {np.max(sim_time):.02f}')
print('')
print(f'\tQ25: {np.quantile(sim_time, 0.25):.02f}')
print(f'\tMedian: {np.quantile(sim_time, 0.50):.02f}')
print(f'\tQ75: {np.quantile(sim_time, 0.75):.02f}')
print(f'\tQ80: {np.quantile(sim_time, 0.80):.02f}')
print(f'\tQ85: {np.quantile(sim_time, 0.85):.02f}')
print(f'\tQ90: {np.quantile(sim_time, 0.90):.02f}')
print(f'\tQ95: {np.quantile(sim_time, 0.95):.02f}')
print(f'\tSimulations that takes longer than 250min: {gt_250.count()} = '
      f'{gt_250.count()/filtered_entries.count()*100:.02f}%')
print(f'\tSimulations that takes longer than 1400min: {gt_day.count()} = '
      f'{gt_day.count()/filtered_entries.count()*100:.02f}%')
print('')
print('PREDICTIONS')
print('\tAverage:')
print(f'\t- (24h x 60min) / Simulation Time x 60 parallel x ({months} months x 30days): '
      f'{24*60/np.mean(sim_time)*60*months*30:.01f} simulation per user')
print(f'\t- {users} users: {24*60/np.mean(sim_time)*60*months*30*users:.04e} simulations')
print('\n\tMedian:')
print(f'\t- (24h x 60min) / Simulation Time x 60 parallel x ({months} months x 30days): '
      f'{24*60/np.quantile(sim_time, 0.50)*60*months*30:.01f} simulations per user')
print(f'\t- {users} users: {24*60/np.quantile(sim_time, 0.50)*60*months*30*users:.04e} simulations')
print('')

plt.figure(figsize=(10, 10))
plt.hist(sim_time, bins='auto', density=True)
plt.title('1D Simulation Time')
plt.xlabel('Simulation Time in Minutes')
plt.ylabel('Number of Simulations')
plt.xlim(0, 50)
plt.show()

mongo_setup.global_end_ssh(server)
