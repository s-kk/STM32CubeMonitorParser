import json
import os
import numpy as np
import sys

data_raw = []

with open(sys.argv[1], 'r') as file:
    raw = file.readlines()
    count = 0
    for line in raw:
        count += 1
        data_raw.append(json.loads(line))
    file.close()

variable_list = []
total_timestamp = []

for i in range(len(data_raw)):
    variable_list.append(data_raw[i]['variablename'])
    for j in range(len(data_raw[i]['variabledata'])):
        total_timestamp.append(data_raw[i]['variabledata'][j]['x'])
variable_list = sorted(set(variable_list))
init_timestamp = np.array([min(total_timestamp), 0])

print('Please select from the variable list:')
for i in range(len(variable_list)):
    print("{}:\t{}".format(i, variable_list[i]))
target_variable = int(input())

filtered_variable = []
target_variable_list = []
for i in range(len(data_raw)):
    if data_raw[i]['variablename'] == variable_list[target_variable]:
        filtered_variable.append(data_raw[i])

# access hierarchy: arr[i]['variabledata'][j]['x']
for i in range(len(filtered_variable)):
    for j in range(len(filtered_variable[i]['variabledata'])):
        target_variable_list.append([filtered_variable[i]['variabledata'][j]['x'],
                                     filtered_variable[i]['variabledata'][j]['y']])

target_variable_array = np.array(target_variable_list, dtype=float)

if input('Would you like to align the timestamp? (y/n) ') == 'y':
    # neutralize timestamp
    print('Aligning...')
    target_variable_array = target_variable_array - init_timestamp

if input('Would you like to export the data sorted by timestamp? (y/n) ') == 'y':
    # sort data
    print('Sorting...')
    target_variable_array = target_variable_array[target_variable_array[:, 0].argsort()]
    save_path = os.path.join("data", variable_list[target_variable] + '_sorted.csv')
    np.savetxt(save_path, target_variable_array.astype(float), fmt=['%i', '%.17f'], delimiter=',')
    print('Success!')
else:
    save_path = os.path.join("data", variable_list[target_variable] + '.csv')
    np.savetxt(save_path, target_variable_array.astype(float), fmt=['%i', '%.16f'], delimiter=',')
    print('Success!')
