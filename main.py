import json
import os
import numpy as np
import matplotlib.pyplot as plt

given_current = []
current_set = []

with open('raw/given_current.json', 'r') as file:
    raw = file.readlines()
    count = 0
    for line in raw:
        count += 1
        given_current.append(json.loads(line))
    file.close()

with open('raw/current_set.json', 'r') as file:
    raw = file.readlines()
    count = 0
    for line in raw:
        count += 1
        current_set.append(json.loads(line))
    file.close()

given_current_arr = []
current_set_arr = []

# access hierarchy: given_current[i]['variabledata'][j]['x']
for i in range(len(given_current)):
    for j in range(len(given_current[i]['variabledata'])):
        given_current_arr.append([given_current[i]['variabledata'][j]['x'], given_current[i]['variabledata'][j]['y']])

for i in range(len(current_set)):
    for j in range(len(current_set[i]['variabledata'])):
        current_set_arr.append([current_set[i]['variabledata'][j]['x'], current_set[i]['variabledata'][j]['y']])

given_current_arr = np.array(given_current_arr)
current_set_arr = np.array(current_set_arr)

# np.savetxt("data/given_current.csv", given_current_arr.astype(int), fmt='%i', delimiter=',')
# np.savetxt("data/current_set.csv", current_set_arr.astype(int), fmt='%i', delimiter=',')

given_current_arr = given_current_arr[given_current_arr[:, 0].argsort()]
current_set_arr = current_set_arr[current_set_arr[:, 0].argsort()]

np.savetxt("data/given_current_sorted.csv", given_current_arr.astype(int), fmt='%i', delimiter=',')
np.savetxt("data/current_set_sorted.csv", current_set_arr.astype(int), fmt='%i', delimiter=',')

init_timestamp = np.array([min(given_current_arr[0][0], current_set_arr[0][0]), 0])
given_current_arr = given_current_arr - init_timestamp
current_set_arr = current_set_arr - init_timestamp

np.savetxt("data/given_current_aligned.csv", given_current_arr.astype(int), fmt='%i', delimiter=',')
np.savetxt("data/current_set_aligned.csv", current_set_arr.astype(int), fmt='%i', delimiter=',')

plt.figure()
plt.scatter(given_current_arr[:, 0], given_current_arr[:, 1])
plt.show()
plt.savefig('plot/given_current.png', dpi=400)

# plt.scatter(current_set_arr[:, 0], current_set_arr[:, 1])
# plt.show()
