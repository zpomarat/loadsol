from DataLoadsolNew import DataLoadsol
from TrialAnalysisNew import TrialAnalysis
from os import listdir
from matplotlib import pyplot as plt
import numpy as np


# working_directory = "D:\\DEMECO\\tests_pointe_01_03_24\\txt\\"
working_directory = "D:\\DEMECO\\tests_pointe_04_03_24\\txt\\"

# List of trial names
files_names = listdir(working_directory)

trial_names = []
for name in files_names:
    n = name.split(".")[0]
    if n not in trial_names:
        trial_names.append(n)

# weight_list = [653.35, 944.7, 562.11, 653.35, 944.7, 562.11, 653.35]
weight_list = [565.1, 565.1, 614.1, 614.1, 663.2, 663.2, 712.2, 712.2, 761.3, 761.3]

surestimation_left = []
surestimation_right = []

for name, weight in zip(trial_names, weight_list):
    file_name = name

    data_ls = DataLoadsol(path=working_directory + file_name + ".txt", frequency=200)

    data_ls.convert_txt_to_csv(working_directory[:-4] + "csv\\")

    Trial = TrialAnalysis(
        DataLoadSol=data_ls,
        DataForcePlates=None,
        sync_index_loadsol=None,
        sync_index_forceplates=None,
        final_frequency=200,
        data_state="filtered",
        order=4,
        fcut=10,
    )

    # Trial.compare_forces_imu()

    mean_left, indexes_left, values_left = Trial.define_initialization_phase(
        side="left", interv=200, start=500
    )
    mean_right, indexes_right, values_right = Trial.define_initialization_phase(
        side="right", interv=200, start=500
    )

    print(f"Mean left: {mean_left}")
    print(f"Mean right: {mean_right}")

    # print(f"Left interval indexes: {indexes_left}")
    # print(f"Left interval values: {values_left}")
    # print(f"Right interval indexes: {indexes_right}")
    # print(f"Right interval values: {values_right}")

    x = np.arange(0,len(Trial.data_loadsol_sync["f_total_l"]),1)
    p_left = np.polyfit(x,Trial.data_loadsol_sync["f_total_l"],10)
    z_left = np.poly1d(p_left)

    x = np.arange(0,len(Trial.data_loadsol_sync["f_total_r"]),1)
    p_right = np.polyfit(x,Trial.data_loadsol_sync["f_total_r"],10)
    z_right = np.poly1d(p_right)

    plt.figure()
    plt.plot(Trial.data_loadsol_sync["f_total_l"], label="left")
    plt.plot(Trial.data_loadsol_sync["f_total_r"], label="right")
    plt.plot(indexes_left, values_left, "x", label="left interval")
    plt.plot(indexes_right, values_right, "o", label="right interval")
    plt.plot(x,z_left(x),label="left")
    plt.plot(x,z_right(x),label="right")
    plt.legend()
    plt.show()

    max_left, idx_left = Trial.max_total_force(side="left", start=500, end=200)
    max_right, idx_right = Trial.max_total_force(side="right", start=500, end=200)

    print(f"Max left: {max_left}")
    print(f"Max right: {max_right}")

    # plt.plot(idx_left, max_left, 's')
    # plt.plot(idx_right, max_right, 's')
    # plt.show()

    # Trial.normalize(factor=weight/2)

    # plt.figure()
    # plt.plot(Trial.weight_normalized_data["f_total_l"], label=file_name)
    # plt.legend()

    # plt.figure()
    # plt.plot(Trial.weight_normalized_data["f_total_r"], label=file_name)
    # plt.legend()

    # plt.show()

    # print("ok")

    # Compute surestimation
    diff_left = max_left - mean_left
    diff_right = max_right - mean_right

    surestimation_left.append(diff_left)
    surestimation_right.append(diff_right)

mean_surestimation_left = [
    np.mean(surestimation_left[0:2]),
    np.mean(surestimation_left[2:4]),
    np.mean(surestimation_left[4:6]),
    np.mean(surestimation_left[6:8]),
    np.mean(surestimation_left[8:10])
]

mean_surestimation_right = [
    np.mean(surestimation_right[0:2]),
    np.mean(surestimation_right[2:4]),
    np.mean(surestimation_right[4:6]),
    np.mean(surestimation_right[6:8]),
    np.mean(surestimation_right[8:10])
]



mean_mean = [np.mean([mean_surestimation_left[0],mean_surestimation_right[0]]),
             np.mean([mean_surestimation_left[1],mean_surestimation_right[1]]),
             np.mean([mean_surestimation_left[2],mean_surestimation_right[2]]),
             np.mean([mean_surestimation_left[3],mean_surestimation_right[3]]),
             np.mean([mean_surestimation_left[4],mean_surestimation_right[4]])]
    

#     diff_left = max_left - mean_left
#     diff_right = max_right - mean_right

#     surestimation_left.append(diff_left)
#     surestimation_right.append(diff_right)

# mean_surestimation_left = [
#     np.mean([surestimation_left[0],surestimation_left[6]]),
#     np.mean([surestimation_left[1],surestimation_left[4]]),
#     np.mean([surestimation_left[2],surestimation_left[5]])
# ]

# mean_surestimation_right = [
#     np.mean([surestimation_right[0],surestimation_right[6]]),
#     np.mean([surestimation_right[1],surestimation_right[4]]),
#     np.mean([surestimation_right[2],surestimation_right[5]])
# ]



# mean_mean = [np.mean([mean_surestimation_left[0],mean_surestimation_right[0]]),
#              np.mean([mean_surestimation_left[1],mean_surestimation_right[1]]),
#              np.mean([mean_surestimation_left[2],mean_surestimation_right[2]])]


# weight_list = [653.35, 944.7, 562.11]
weight_list = [565.1, 614.1, 663.2, 712.2, 761.3]


regress = np.polyfit(weight_list,mean_mean,1)
regress_values = np.poly1d(regress)


plt.plot(weight_list, mean_surestimation_left, "-x", label="left")
plt.plot(weight_list, mean_surestimation_right, "-o", label="right")
plt.plot(weight_list, mean_mean, "-^", label="mean")
plt.plot(weight_list,regress_values(weight_list))
plt.legend()



print(regress_values)

plt.show()