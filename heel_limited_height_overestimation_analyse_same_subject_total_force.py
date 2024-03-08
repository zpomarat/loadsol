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
CONDITION = "nl"

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
overestimation = []
bw_test = []
trial_results = {}
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

    # Define the signal of totla force of both feet
    data = trial_cut.data_loadsol_sync["f_total_l"] + trial_cut.data_loadsol_sync["f_total_r"]

    # Define initialization parameters
    mean, std, indexes, values = trial_cut.define_initialization_phase(
        side="total", interv=400, start=0, data = data
    )


    # print(name)
    # print(f"Mean left: {mean_left}")
    # print(f"Standard deviation left: {std_left}")
    # print(f"Mean right: {mean_right}")
    # print(f"Standard deviation right: {std_right}")

    # Define maximal values of total force
    max, idx = trial_cut.max_total_force(side="total", start=0, end=1, data = data)


    # Compute the overestimation as the difference between the maximal value and the mean value of force during the initialization phase
    overestimation = max - mean

    # Compute the overestimatoin rate
    overestimation_rate = (overestimation / mean)*100

    # Define a list of bodyweight conditions of the test
    if bw not in bw_test:
        bw_test.append(bw)    

    # Create a dictionnary containing results of each trial
    trial_results[name] = {
        "force_max": max,
        "force_mean": mean,
        "overestimation": overestimation,
        "overestimation_rate": overestimation_rate
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

# For this example, delete the condition 705.3
bw_test.remove(705.3)

# Create a dictionnary containing the mean results for each weight conditions
for idx, bw in enumerate(bw_test):

    if CONDITION == "hl":
        match bw:
            case 607.2:
                mean_results[bw] = {
                    "mean_overestimation": np.mean(
                        [
                            trial_results[trial_names[idx * 3 + 1]]["overestimation"]
                        ]
                    ),
                    "std_overestimation": np.std(
                        [
                            trial_results[trial_names[idx * 3 + 1]]["overestimation"]
                        ]
                    ),
                    "mean_overestimation_rate": np.mean(
                        [
                            trial_results[trial_names[idx * 3 + 1]]["overestimation_rate"]
                        ]
                    ),
                    "std_overestimation_rate": np.std(
                        [
                            trial_results[trial_names[idx * 3 + 1]]["overestimation_rate"]
                        ]
                    )
                }
          
            case 754.4:
                mean_results[bw] = {
                    "mean_overestimation": np.mean(
                        [
                            trial_results[trial_names[idx * 3 + 1]]["overestimation"],
                            trial_results[trial_names[idx * 3 + 2]]["overestimation"]
                        ]
                    ),
                    "std_overestimation": np.std(
                        [
                            trial_results[trial_names[idx * 3 + 1]]["overestimation"],
                            trial_results[trial_names[idx * 3 + 2]]["overestimation"]
                        ]
                    ),
                    "mean_overestimation_rate": np.mean(
                        [
                            trial_results[trial_names[idx * 3 + 1]]["overestimation_rate"],
                            trial_results[trial_names[idx * 3 + 2]]["overestimation_rate"]
                        ]
                    ),
                    "std_overestimation_rate": np.std(
                        [
                            trial_results[trial_names[idx * 3 + 1]]["overestimation_rate"],
                            trial_results[trial_names[idx * 3 + 2]]["overestimation_rate"]
                        ]
                    )
                }
                
            case _:
                mean_results[bw] = {
                    "mean_overestimation": np.mean(
                        [
                            trial_results[trial_names[idx * 3]]["overestimation"],
                            trial_results[trial_names[idx * 3 + 1]]["overestimation"],
                            trial_results[trial_names[idx * 3 + 2]]["overestimation"]
                        ]
                    ),
                    "std_overestimation": np.std(
                        [
                            trial_results[trial_names[idx * 3]]["overestimation"],
                            trial_results[trial_names[idx * 3 + 1]]["overestimation"],
                            trial_results[trial_names[idx * 3 + 2]]["overestimation"]
                        ]
                    ),
                    "mean_overestimation_rate": np.mean(
                        [
                            trial_results[trial_names[idx * 3]]["overestimation_rate"],
                            trial_results[trial_names[idx * 3 + 1]]["overestimation_rate"],
                            trial_results[trial_names[idx * 3 + 2]]["overestimation_rate"]
                        ]
                    ),
                    "std_overestimation_rate": np.std(
                        [
                            trial_results[trial_names[idx * 3]]["overestimation_rate"],
                            trial_results[trial_names[idx * 3 + 1]]["overestimation_rate"],
                            trial_results[trial_names[idx * 3 + 2]]["overestimation_rate"]
                        ]
                    )
                }


    elif CONDITION == "nl":
        match bw:
            case 558.2:
                mean_results[bw] = {
                    "mean_overestimation": np.mean(
                        [
                            trial_results[trial_names[idx * 3]]["overestimation"]
                        ]
                    ),
                    "std_overestimation": np.std(
                        [
                            trial_results[trial_names[idx * 3]]["overestimation"]
                        ]
                    ),
                    "mean_overestimation_rate": np.mean(
                        [
                            trial_results[trial_names[idx * 3]]["overestimation_rate"]
                        ]
                    ),
                    "std_overestimation_rate": np.std(
                        [
                            trial_results[trial_names[idx * 3]]["overestimation_rate"]
                        ]
                    )
                }
            
            case 607.2:
                mean_results[bw] = {
                    "mean_overestimation": np.mean(
                        [
                            trial_results[trial_names[idx * 3 + 1]]["overestimation"],
                            trial_results[trial_names[idx * 3 + 2]]["overestimation"]
                        ]
                    ),
                    "std_overestimation": np.std(
                        [
                            trial_results[trial_names[idx * 3 + 1]]["overestimation"],
                            trial_results[trial_names[idx * 3 + 2]]["overestimation"]
                        ]
                    ),
                    "mean_overestimation_rate": np.mean(
                        [
                            trial_results[trial_names[idx * 3 + 1]]["overestimation_rate"],
                            trial_results[trial_names[idx * 3 + 2]]["overestimation_rate"]
                        ]
                    ),
                    "std_overestimation_rate": np.std(
                        [
                            trial_results[trial_names[idx * 3 + 1]]["overestimation_rate"],
                            trial_results[trial_names[idx * 3 + 2]]["overestimation_rate"]
                        ]
                    )
                }

            case 656.3:
                mean_results[bw] = {
                    "mean_overestimation": np.mean(
                        [
                            trial_results[trial_names[idx * 3]]["overestimation"],
                            trial_results[trial_names[idx * 3 + 2]]["overestimation"]
                        ]
                    ),
                    "std_overestimation": np.std(
                        [
                            trial_results[trial_names[idx * 3]]["overestimation"],
                            trial_results[trial_names[idx * 3 + 2]]["overestimation"]
                        ]
                    ),
                    "mean_overestimation_rate": np.mean(
                        [
                            trial_results[trial_names[idx * 3]]["overestimation_rate"],
                            trial_results[trial_names[idx * 3 + 2]]["overestimation_rate"]
                        ]
                    ),
                    "std_overestimation_rate": np.std(
                        [
                            trial_results[trial_names[idx * 3]]["overestimation_rate"],
                            trial_results[trial_names[idx * 3 + 2]]["overestimation_rate"]
                        ]
                    )
                }

            case _:
                mean_results[bw] = {
                    "mean_overestimation": np.mean(
                        [
                            trial_results[trial_names[idx * 3]]["overestimation"],
                            trial_results[trial_names[idx * 3 + 1]]["overestimation"],
                            trial_results[trial_names[idx * 3 + 2]]["overestimation"],
                        ]
                    ),
                    "std_overestimation": np.std(
                        [
                            trial_results[trial_names[idx * 3]]["overestimation"],
                            trial_results[trial_names[idx * 3 + 1]]["overestimation"],
                            trial_results[trial_names[idx * 3 + 2]]["overestimation"],
                        ]
                    ),
                    "mean_overestimation_rate": np.mean(
                        [
                            trial_results[trial_names[idx * 3]]["overestimation_rate"],
                            trial_results[trial_names[idx * 3 + 1]]["overestimation_rate"],
                            trial_results[trial_names[idx * 3 + 2]]["overestimation_rate"],
                        ]
                    ),
                    "std_overestimation_rate": np.std(
                        [
                            trial_results[trial_names[idx * 3]]["overestimation_rate"],
                            trial_results[trial_names[idx * 3 + 1]]["overestimation_rate"],
                            trial_results[trial_names[idx * 3 + 2]]["overestimation_rate"],
                        ]
                    )
                }
                

# Initialize lists of results data
mean_over = []
std_over = []
mean_over_rate = []
std_over_rate = []


for i in range(len(bw_test)):
    mean_over.append(mean_results[bw_test[i]]["mean_overestimation"])
    std_over.append(mean_results[bw_test[i]]["std_overestimation"])
    mean_over_rate.append(mean_results[bw_test[i]]["mean_overestimation_rate"])
    std_over_rate.append(mean_results[bw_test[i]]["std_overestimation_rate"])


plt.figure()
plt.title("Overestimation of the total force")
plt.xlabel("Body weight")
plt.ylabel("Overestimation of force (N)")
plt.plot(np.array(bw_test), mean_over, "-x", color='blue', label="left")
plt.errorbar(np.array(bw_test), mean_over, std_over, color='blue')
plt.legend()

plt.figure()
plt.title("Overestimation rate of the total force")
plt.xlabel("Body weight")
plt.ylabel("Overestimation rate of force (% of the force in the reference phase)")
plt.plot(np.array(bw_test), mean_over_rate, "-x", color='blue', label="left")
plt.errorbar(np.array(bw_test), mean_over_rate, std_over_rate, color='blue')
plt.legend()

# Compute regression function
regress_force = np.polyfit(bw_test,mean_over,1)
regress_values_force = np.poly1d(regress_force)

regress_rate = np.polyfit(bw_test,mean_over_rate,1)
regress_values_rate = np.poly1d(regress_rate)

plt.figure()
plt.title("Overestimation of the total force")
plt.xlabel("Body weight")
plt.ylabel("Overestimation of force (N)")
plt.plot(np.array(bw_test), mean_over, "-x", color='blue', label="left")
plt.errorbar(np.array(bw_test), mean_over, std_over, color='blue')
plt.plot(bw_test,regress_values_force(bw_test))
plt.legend()

plt.figure()
plt.title("Overestimation rate of the total force")
plt.xlabel("Body weight")
plt.ylabel("Overestimation rate of force (% of the force in the reference phase)")
plt.plot(np.array(bw_test), mean_over_rate, "-x", color='blue', label="left")
plt.errorbar(np.array(bw_test), mean_over_rate, std_over_rate, color='blue')
plt.plot(bw_test,regress_values_rate(bw_test))
plt.legend()
plt.show()

print(f"Regress force left: {regress_force}")
print(f"Regress rate left: {regress_rate}")
