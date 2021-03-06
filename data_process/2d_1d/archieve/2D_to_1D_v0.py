__author__ = "Christian Kongsgaard"
__license__ = 'MIT'

# -------------------------------------------------------------------------------------------------------------------- #
# IMPORTS

# Modules
import matplotlib.pyplot as plt
import numpy as np
import os
import datetime
import matplotlib.dates as mdates

# RiBuild Modules
from delphin_6_automation.file_parsing import delphin_parser

# -------------------------------------------------------------------------------------------------------------------- #
# RIBuild


# Functions
def get_points(result: dict, geo: dict):

    points = []
    for index in result['indices']:
        x_ = geo['element_geometry'][index][1]
        y_ = geo['element_geometry'][index][2]
        points.append({'cell': index, 'x': x_, 'y': y_})

    return points


def add_data_to_points(points: list, results: dict, result_name: str):
    for cell_ in results['result'].keys():
        cell_index = int(cell_.split('_')[1])

        for point in points:
            if point['cell'] == cell_index:
                point[result_name] = np.array(results['result'][cell_][8760:])
                break


# Application
colors = {'top': '#FBBA00', 'mid': '#B81A5D', 'bottom': '#79C6C0', '1d_brick': '#000000', '1d_mortar': '#BDCCD4'}
result_folder = r'U:\RIBuild\2D_1D\Results'
projects = ['5ad5da522e2cb21a90397b85', '5ad5dac32e2cb21a90397b86', '5ad5e05d5d9460d762130f93']
files = ['Temperature profile [2].d6o', 'Relative humidity profile [2].d6o',
         'Moisture content profile [2].d6o', 'Moisture content integral [2].d6o']

parsed_dicts = {'brick_1d': {'temp': {}, 'rh': {}, 'm_content': {}, 'moisture': {}, 'geo': {}},
                'mortar_1d': {'temp': {}, 'rh': {}, 'm_content': {}, 'moisture': {}, 'geo': {}},
                '2d': {'temp': {}, 'rh': {}, 'm_content': {}, 'moisture': {}, 'geo': {}}, }

map_projects = {'5ad5da522e2cb21a90397b85': 'brick_1d', '5ad5dac32e2cb21a90397b86': 'mortar_1d',
                '5ad5e05d5d9460d762130f93': '2d'}
for project in projects:
    for mp_key in map_projects.keys():
        if project == mp_key:
            key = map_projects[mp_key]

    folder = result_folder + f'/{project}/results'
    geo_file = [file
                for file in os.listdir(folder)
                if file.endswith('.g6a')][0]

    parsed_dicts[key]['temp'], _ = delphin_parser.d6o_to_dict(folder, files[0])
    parsed_dicts[key]['rh'], _ = delphin_parser.d6o_to_dict(folder, files[1])
    parsed_dicts[key]['m_content'], _ = delphin_parser.d6o_to_dict(folder, files[2])
    parsed_dicts[key]['moisture'], _ = delphin_parser.d6o_to_dict(folder, files[3])
    parsed_dicts[key]['geo'] = delphin_parser.g6a_to_dict(folder, geo_file)

x = np.linspace(0, len(parsed_dicts['brick_1d']['temp']['result']['cell_0'][8760:]),
                len(parsed_dicts['brick_1d']['temp']['result']['cell_0'][8760:]))
x_date = [datetime.datetime(2020, 1, 1) + datetime.timedelta(hours=i)
          for i in range(len(parsed_dicts['brick_1d']['temp']['result']['cell_0'][8760:]))]
x_2d = np.linspace(0, len(parsed_dicts['2d']['temp']['result']['cell_66'][8760:]),
                   len(parsed_dicts['2d']['temp']['result']['cell_66'][8760:]))
x_date_2d = [datetime.datetime(2020, 1, 1) + datetime.timedelta(hours=i)
             for i in range(len(parsed_dicts['2d']['temp']['result']['cell_66'][8760:]))]

# Brick 1D
brick_1d = get_points(parsed_dicts['brick_1d']['temp'], parsed_dicts['brick_1d']['geo'])
brick_1d.sort(key=lambda point: point['x'])
add_data_to_points(brick_1d, parsed_dicts['brick_1d']['temp'], 'temperature')
add_data_to_points(brick_1d, parsed_dicts['brick_1d']['rh'], 'relative_humidity')
add_data_to_points(brick_1d, parsed_dicts['brick_1d']['m_content'], 'moisture_content')
add_data_to_points(brick_1d, parsed_dicts['brick_1d']['moisture'], 'moisture_integral')


# Mortar 1D
mortar_1d = get_points(parsed_dicts['mortar_1d']['temp'], parsed_dicts['mortar_1d']['geo'])
mortar_1d.sort(key=lambda point: point['x'])
add_data_to_points(mortar_1d, parsed_dicts['mortar_1d']['temp'], 'temperature')
add_data_to_points(mortar_1d, parsed_dicts['mortar_1d']['rh'], 'relative_humidity')
add_data_to_points(mortar_1d, parsed_dicts['mortar_1d']['m_content'], 'moisture_content')
add_data_to_points(mortar_1d, parsed_dicts['mortar_1d']['moisture'], 'moisture_integral')

# 2D
sim_2d = get_points(parsed_dicts['2d']['temp'], parsed_dicts['2d']['geo'])
sim_2d.sort(key=lambda point: (point['x'], point['y']))
add_data_to_points(sim_2d, parsed_dicts['2d']['temp'], 'temperature')
add_data_to_points(sim_2d, parsed_dicts['2d']['rh'], 'relative_humidity')
add_data_to_points(sim_2d, parsed_dicts['2d']['m_content'], 'moisture_content')
add_data_to_points(sim_2d, parsed_dicts['2d']['moisture'], 'moisture_integral')


# Plots
def plot_locations(quantity):
    # Axes 00
    plt.figure()
    plt.title(f"{quantity}\n1D-Location: {brick_1d[0]['x']:.4f} and 2D-Location: {sim_2d[0]['x']:.4f}")
    plt.plot(x_date, brick_1d[0][quantity], color=colors['1d_brick'], label=f"1D Brick")
    plt.plot(x_date, mortar_1d[0][quantity], color=colors['1d_mortar'], label=f"1D Mortar")
    plt.plot(x_date_2d, sim_2d[0][quantity], color=colors['bottom'], label=f"2D Bottom")
    plt.plot(x_date_2d, sim_2d[1][quantity], color=colors['mid'], label=f"2D Mid")
    plt.plot(x_date_2d, sim_2d[2][quantity], color=colors['top'], label=f"2D Top")
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%B'))
    plt.ylabel(f'{quantity}')

    # Axes 01
    plt.figure()
    plt.title(f"{quantity}\n1D-Location: {brick_1d[1]['x']:.4f} and 2D-Location: {sim_2d[3]['x']:.4f}")
    plt.plot(x_date, brick_1d[1][quantity], color=colors['1d_brick'], label=f"1D Brick")
    plt.plot(x_date, mortar_1d[1][quantity], color=colors['1d_mortar'], label=f"1D Mortar")
    plt.plot(x_date_2d, sim_2d[3][quantity], color=colors['bottom'], label=f"2D Bottom")
    plt.plot(x_date_2d, sim_2d[4][quantity], color=colors['mid'], label=f"2D Mid")
    plt.plot(x_date_2d, sim_2d[5][quantity], color=colors['top'], label=f"2D Top")
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%B'))
    plt.ylabel(f'{quantity}')

    # Axes 10
    plt.figure()
    plt.title(f"{quantity}\n1D-Location: {brick_1d[2]['x']:.4f} and 2D-Location: {sim_2d[6]['x']:.4f}")
    plt.plot(x_date, brick_1d[2][quantity], color=colors['1d_brick'], label=f"1D Brick")
    plt.plot(x_date, mortar_1d[2][quantity], color=colors['1d_mortar'], label=f"1D Mortar")
    plt.plot(x_date_2d, sim_2d[6][quantity], color=colors['bottom'], label=f"2D Bottom")
    plt.plot(x_date_2d, sim_2d[7][quantity], color=colors['mid'], label=f"2D Mid")
    plt.plot(x_date_2d, sim_2d[8][quantity], color=colors['top'], label=f"2D Top")
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%B'))
    plt.ylabel(f'{quantity}')

    # Axes 11
    plt.figure()
    plt.title(f"{quantity}\n1D-Location: {brick_1d[3]['x']:.4f} and 2D-Location: {sim_2d[9]['x']:.4f}")
    plt.plot(x_date, brick_1d[3][quantity], color=colors['1d_brick'], label=f"1D Brick")
    plt.plot(x_date, mortar_1d[3][quantity], color=colors['1d_mortar'], label=f"1D Mortar")
    plt.plot(x_date_2d, sim_2d[9][quantity], color=colors['bottom'], label=f"2D Bottom")
    plt.plot(x_date_2d, sim_2d[10][quantity], color=colors['mid'], label=f"2D Mid")
    plt.plot(x_date_2d, sim_2d[11][quantity], color=colors['top'], label=f"2D Top")
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%B'))
    plt.ylabel(f'{quantity}')

    # Axes 20
    plt.figure()
    plt.title(f"{quantity}\n1D-Location: {brick_1d[4]['x']:.4f} and 2D-Location: {sim_2d[12]['x']:.4f}")
    plt.plot(x_date, brick_1d[4][quantity], color=colors['1d_brick'], label=f"1D Brick")
    plt.plot(x_date, mortar_1d[4][quantity], color=colors['1d_mortar'], label=f"1D Mortar")
    plt.plot(x_date_2d, sim_2d[12][quantity], color=colors['bottom'], label=f"2D Bottom")
    plt.plot(x_date_2d, sim_2d[13][quantity], color=colors['mid'], label=f"2D Mid")
    plt.plot(x_date_2d, sim_2d[14][quantity], color=colors['top'], label=f"2D Top")
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%B'))
    plt.ylabel(f'{quantity}')

    # Axes 21
    plt.figure()
    plt.title(f"{quantity}\n1D-Location: {brick_1d[5]['x']:.4f} and 2D-Location: {sim_2d[15]['x']:.4f}")
    plt.plot(x_date, brick_1d[5][quantity], color=colors['1d_brick'], label=f"1D Brick")
    plt.plot(x_date, mortar_1d[5][quantity], color=colors['1d_mortar'], label=f"1D Mortar")
    plt.plot(x_date_2d, sim_2d[15][quantity], color=colors['bottom'], label=f"2D Bottom")
    plt.plot(x_date_2d, sim_2d[16][quantity], color=colors['mid'], label=f"2D Mid")
    plt.plot(x_date_2d, sim_2d[17][quantity], color=colors['top'], label=f"2D Top")
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%B'))
    plt.ylabel(f'{quantity}')


#plot_locations(quantity='temperature')
#plt.show()
#plot_locations(quantity='relative_humidity')
#plt.show()
#plot_locations(quantity='moisture_content')
#plt.show()

# Moisture Integral
plt.figure()
plt.title('Moisture Integral')
plt.plot(x_date, brick_1d[0]['moisture_integral'], color=colors['1d_brick'], label=f"1D Brick")
plt.plot(x_date, mortar_1d[0]['moisture_integral'], color=colors['1d_mortar'], label=f"1D Mortar")
plt.plot(x_date_2d, sim_2d[0]['moisture_integral']*7.351860020585208, color=colors['bottom'], label=f"2D")
plt.legend()
plt.gcf().autofmt_xdate()
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%B'))
plt.ylabel('kg')


def abs_diff(x1, x2):
    return x2 - x1


def rel_diff(x1, x2):
    return (abs(x2 - x1))/abs(x2) * 100


brick_abs = abs_diff(brick_1d[0]['moisture_integral'][:len(sim_2d[0]['moisture_integral'])],
                     sim_2d[0]['moisture_integral']*7.351860020585208)
mortar_abs = abs_diff(mortar_1d[0]['moisture_integral'][:len(sim_2d[0]['moisture_integral'])],
                      sim_2d[0]['moisture_integral']*7.351860020585208)
brick_rel = rel_diff(brick_1d[0]['moisture_integral'][:len(sim_2d[0]['moisture_integral'])],
                     sim_2d[0]['moisture_integral']*7.351860020585208)
mortar_rel = rel_diff(mortar_1d[0]['moisture_integral'][:len(sim_2d[0]['moisture_integral'])],
                      sim_2d[0]['moisture_integral']*7.351860020585208)

# Moisture Integral
plt.figure()
plt.title('Moisture Integral - Absolute Difference')
plt.plot(x_date_2d, brick_abs, color=colors['1d_brick'], label=f"1D Brick")
plt.plot(x_date_2d, mortar_abs, color=colors['1d_mortar'], label=f"1D Mortar")
plt.legend()
plt.gcf().autofmt_xdate()
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%B'))
plt.ylabel('kg')

plt.figure()
plt.title('Moisture Integral - Relative Difference')
plt.plot(x_date_2d, brick_rel, color=colors['1d_brick'], label=f"1D Brick")
plt.plot(x_date_2d, mortar_rel, color=colors['1d_mortar'], label=f"1D Mortar")
plt.legend()
plt.gcf().autofmt_xdate()
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%B'))
plt.ylabel('%')

print('Relative Difference:')
print()
print(f"25th PERCENTILE:\tBrick: {np.percentile(brick_rel, 25):.03f}\tMortar: {np.percentile(mortar_rel, 25):.03f}")
print(f"MEAN:\t\t\t\tBrick: {np.mean(brick_rel):.03f}\tMortar: {np.mean(mortar_rel):.03f}")
print(f"MEDIAN:\t\t\t\tBrick: {np.median(brick_rel):.03f}\tMortar: {np.median(mortar_rel):.03f}")
print(f"75th PERCENTILE:\tBrick: {np.percentile(brick_rel, 75):.03f}\tMortar: {np.percentile(mortar_rel, 75):.03f}")
print(f"STANDARD DEVIATION:\tBrick: {np.std(brick_rel):.03f}\tMortar: {np.std(mortar_rel):.03f}")

plt.show()
