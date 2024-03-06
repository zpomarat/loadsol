from DataLoadsolNew import DataLoadsol
from TrialAnalysisNew import TrialAnalysis
from os import listdir
from matplotlib import pyplot as plt
import numpy as np
from copy import deepcopy


# Synopsis
# Test: progressively standing on tiptoes


# Define working directory
working_directory = "D:\\DEMECO\\tests_pointe_06_03_24\\txt\\"

# Test condition (hl or nl)
CONDITION = "hl"

# List of files in the directory, respecting the condition above
test_files = [
    "pointe_" + CONDITION + "_0_1",
    "pointe_" + CONDITION + "_0_2",
    "pointe_" + CONDITION + "_0_3",
    "pointe_" + CONDITION + "_5_1",
    "pointe_" + CONDITION + "_5_2",
    "pointe_" + CONDITION + "_5_3",
    "pointe_" + CONDITION + "_10_1",
    "pointe_" + CONDITION + "_10_2",
    "pointe_" + CONDITION + "_10_3",
    "pointe_" + CONDITION + "_15_1",
    "pointe_" + CONDITION + "_15_2",
    "pointe_" + CONDITION + "_15_3",
    "pointe_" + CONDITION + "_20_1",
    "pointe_" + CONDITION + "_20_2",
    "pointe_" + CONDITION + "_20_3",
]

# Define trial names
trial_names = []

for name in test_files:
    n = name.split(".")[0]
    if n not in trial_names:
        trial_names.append(n)

# Initialization
overestimation_left = []
overestimation_right = []
bw_test = []
trial_results = {}
mean_results = {}
mean_results = {}

# Define body weights for each trial (in N)
BODYWEIGHTS = [
    558.2,
    558.2,
    558.2,
    607.2,
    607.2,
    607.2,
    656.3,
    656.3,
    656.3,
    705.3,
    705.3,
    705.3,
    754.4,
    754.4,
    754.4,
]

for name, bw in zip(trial_names, BODYWEIGHTS):

    # Create DataLoadsol object
    data = DataLoadsol(path=working_directory + name + ".txt", frequency=200)

    # Convert files into csv files
    data.convert_txt_to_csv(working_directory[:-4] + "csv\\")

    # Create TrialAnalysis object
    trial = TrialAnalysis(
        DataLoadSol=data,
        DataForcePlates=None,
        sync_index_loadsol=None,
        sync_index_forceplates=None,
        final_frequency=200,
        data_state="pre_processed",
        order=None,
        fcut=None,
    )

    # Cut data
    START = 1000
    END = 400

    trial_cut = deepcopy(trial)
    for key in trial_cut.data_loadsol_sync.keys():
        trial_cut.data_loadsol_sync[key] = trial_cut.data_loadsol_sync[key][START:-END]

    # Set time to zero
    trial_cut.data_loadsol_sync["time"] = (
        trial_cut.data_loadsol_sync["time"] - trial_cut.data_loadsol_sync["time"][0]
    )

    # Define initialization parameters
    mean_left, indexes_left, values_left = trial_cut.define_initialization_phase(
        side="left", interv=400, start=0
    )
    mean_right, indexes_right, values_right = trial_cut.define_initialization_phase(
        side="right", interv=400, start=0
    )

    # Define maximal values of total force
    max_left, idx_left = trial_cut.max_total_force(side="left", start=0, end=1)
    max_right, idx_right = trial_cut.max_total_force(side="right", start=0, end=1)

    # Compute the overestimation as the difference between the maximal value and the mean value of force during the initialization phase
    overestimation_left = max_left - mean_left
    overestimation_right = max_right - mean_right

    # Define a list of bodyweight conditions of the test
    if bw not in bw_test:
        bw_test.append(bw)

    # Create a dictionnary containing results of each trial
    trial_results[name] = {
        "force_max_left": max_left,
        "force_max_right": max_right,
        "force_mean_left": mean_left,
        "force_mean_right": mean_right,
        "overestimation_left": overestimation_left,
        "overestimation_right": overestimation_right,
    }

    # plt.figure()
    # plt.plot(trial_cut.data_loadsol_sync["f_total_l"], label="left")
    # plt.plot(trial_cut.data_loadsol_sync["f_total_r"], label="right")
    # plt.plot(indexes_left, values_left, "x", label="left interval")
    # plt.plot(indexes_right, values_right, "o", label="right interval")
    # plt.plot(idx_left, max_left, "s")
    # plt.plot(idx_right, max_right, "s")
    # plt.legend()
    # plt.title(name)

# Create a dictionnary containing the mean results for each weight conditions
for idx, bw in enumerate(bw_test):

    mean_results[bw] = {
        "mean_overestimation_left": np.mean(
            [
                trial_results[trial_names[idx * 3]]["overestimation_left"],
                trial_results[trial_names[idx * 3 + 1]]["overestimation_left"],
                trial_results[trial_names[idx * 3 + 2]]["overestimation_left"],
            ]
        ),
        "mean_overestimation_right": np.mean(
            [
                trial_results[trial_names[idx * 3]]["overestimation_right"],
                trial_results[trial_names[idx * 3 + 1]]["overestimation_right"],
                trial_results[trial_names[idx * 3 + 2]]["overestimation_right"],
            ]
        ),
    }

y_left = [
    mean_results[bw_test[0]]["mean_overestimation_left"],
    mean_results[bw_test[1]]["mean_overestimation_left"],
    mean_results[bw_test[2]]["mean_overestimation_left"],
    mean_results[bw_test[3]]["mean_overestimation_left"],
    mean_results[bw_test[4]]["mean_overestimation_left"],
]
y_right = [
    mean_results[bw_test[0]]["mean_overestimation_right"],
    mean_results[bw_test[1]]["mean_overestimation_right"],
    mean_results[bw_test[2]]["mean_overestimation_right"],
    mean_results[bw_test[3]]["mean_overestimation_right"],
    mean_results[bw_test[4]]["mean_overestimation_left"],
]

plt.figure()
plt.plot(np.array(bw_test), y_left, "-x", label="left")
plt.plot(np.array(bw_test), y_right, "-o", label="right")
plt.legend()
plt.show()
