# For each files in the examples directory, define manually the indexes of:
# Start signal: start
# Start forceplate zero phase: start_zero
# End forceplate zero phase: end_zero
# Start trial: start_trial
# End trial: end_trial.

# To find the indexes of these events, use the kinetics toolkit and the TimeSeries.

from os import getcwd, listdir
from DataLoadsol import DataLoadsol
from DataForceplates import DataForceplates
import kineticstoolkit as ktk
import matplotlib.pyplot as plt
ktk.import_extensions()
ktk.change_defaults()

# Define the working directory
curr_path = getcwd()
working_directory = curr_path + "\\examples\\data\\"

# List of txt files in the directory
txt_files = [
    "test_poids.txt",
    "test_pointe_1.txt",
    "test_pointe_3.txt",
    "test_pointe_5.txt",
    "test_poussee_1.txt",
    "test_poussee_2.txt",
    "test_poussee_3.txt",
]

# List of c3d files in the directory
c3d_files = [
    "test_poids.c3d",
    "test_pointe_1.c3d",
    "test_pointe_3.c3d",
    "test_pointe_5.c3d",
    "test_poussee_1.c3d",
    "test_poussee_2.c3d",
    "test_poussee_3.c3d",
]

# Define DataLoadsol objects
poids_ls = DataLoadsol(path=working_directory + txt_files[0], frequency=200)
pointe_1_ls = DataLoadsol(path=working_directory + txt_files[1], frequency=200)
pointe_3_ls = DataLoadsol(path=working_directory + txt_files[2], frequency=200)
pointe_5_ls = DataLoadsol(path=working_directory + txt_files[3], frequency=200)
poussee_1_ls = DataLoadsol(path=working_directory + txt_files[4], frequency=200)
poussee_2_ls = DataLoadsol(path=working_directory + txt_files[5], frequency=200)
poussee_3_ls = DataLoadsol(path=working_directory + txt_files[6], frequency=200)

# Define DataForceplates objects
poids_fp = DataForceplates(path=working_directory + c3d_files[0], frequency=1000)
pointe_1_fp = DataForceplates(path=working_directory + c3d_files[1], frequency=1000)
pointe_3_fp = DataForceplates(path=working_directory + c3d_files[2], frequency=1000)
pointe_5_fp = DataForceplates(path=working_directory + c3d_files[3], frequency=1000)
poussee_1_fp = DataForceplates(path=working_directory + c3d_files[4], frequency=1000)
poussee_2_fp = DataForceplates(path=working_directory + c3d_files[5], frequency=1000)
poussee_3_fp = DataForceplates(path=working_directory + c3d_files[6], frequency=1000)

# Convert txt files into csv files  ## TODO: csv conversion doesn't work correctly
if "test_poids.csv" in listdir(working_directory):
    print("txt files already converted into csv files.")
    pass
else:
    poids_ls.convert_txt_to_csv(working_directory)
    pointe_1_ls.convert_txt_to_csv(working_directory)
    pointe_3_ls.convert_txt_to_csv(working_directory)
    pointe_5_ls.convert_txt_to_csv(working_directory)
    poussee_1_ls.convert_txt_to_csv(working_directory)
    poussee_2_ls.convert_txt_to_csv(working_directory)
    poussee_3_ls.convert_txt_to_csv(working_directory)
    print("txt files converted into csv files.")

## Get variables of interest for finding indexes
# Insoles time
poids_pp_time_ls = poids_ls.get_pre_processed_time()   
pointe_1_pp_time_ls = pointe_1_ls.get_pre_processed_time()
pointe_3_pp_time_ls = pointe_3_ls.get_pre_processed_time()
pointe_5_pp_time_ls = pointe_5_ls.get_pre_processed_time()
poussee_1_pp_time_ls = poussee_1_ls.get_pre_processed_time()
poussee_2_pp_time_ls = poussee_2_ls.get_pre_processed_time()
poussee_3_pp_time_ls = poussee_3_ls.get_pre_processed_time()

# Acceleration of one insole (both are synchronised)
poids_pp_l_acc = poids_ls.get_pre_processed_data(insole_side="LEFT", data_type="ACC")
pointe_1_pp_l_acc = pointe_1_ls.get_pre_processed_data(insole_side="LEFT", data_type="ACC")
pointe_3_pp_l_acc = pointe_3_ls.get_pre_processed_data(insole_side="LEFT", data_type="ACC")
pointe_5_pp_l_acc = pointe_5_ls.get_pre_processed_data(insole_side="LEFT", data_type="ACC")
poussee_1_pp_l_acc = poussee_1_ls.get_pre_processed_data(insole_side="LEFT", data_type="ACC")
poussee_2_pp_l_acc = poussee_2_ls.get_pre_processed_data(insole_side="LEFT", data_type="ACC")
poussee_3_pp_l_acc = poussee_3_ls.get_pre_processed_data(insole_side="LEFT", data_type="ACC")

# Forceceplate force in z direction for the forceplates 1 and 2
poids_pp_fp2 = poids_fp.get_pre_processed_data(forceplate_number=2)
pointe_1_pp_fp2 = pointe_1_fp.get_pre_processed_data(forceplate_number=2)
pointe_3_pp_fp2 = pointe_3_fp.get_pre_processed_data(forceplate_number=2)
pointe_5_pp_fp2 = pointe_5_fp.get_pre_processed_data(forceplate_number=2)
poussee_1_pp_fp2 = poussee_1_fp.get_pre_processed_data(forceplate_number=2)
poussee_2_pp_fp2 = poussee_2_fp.get_pre_processed_data(forceplate_number=2)
poussee_3_pp_fp2 = poussee_3_fp.get_pre_processed_data(forceplate_number=2)

# Forceplates time
poids_pp_time_fp = poids_fp.get_pre_processed_time()   
pointe_1_pp_time_fp = pointe_1_fp.get_pre_processed_time()
pointe_3_pp_time_fp = pointe_3_fp.get_pre_processed_time()
pointe_5_pp_time_fp = pointe_5_fp.get_pre_processed_time()
poussee_1_pp_time_fp = poussee_1_fp.get_pre_processed_time()
poussee_2_pp_time_fp = poussee_2_fp.get_pre_processed_time()
poussee_3_pp_time_fp = poussee_3_fp.get_pre_processed_time()

## Create TimeSeries
poids_ls_ts = ktk.TimeSeries()
poids_fp_ts = ktk.TimeSeries()
pointe_1_ls_ts = ktk.TimeSeries()
pointe_1_fp_ts = ktk.TimeSeries()
pointe_3_ls_ts = ktk.TimeSeries()
pointe_3_fp_ts = ktk.TimeSeries()
pointe_5_ls_ts = ktk.TimeSeries()
pointe_5_fp_ts = ktk.TimeSeries()
poussee_1_ls_ts = ktk.TimeSeries()
poussee_1_fp_ts = ktk.TimeSeries()
poussee_2_ls_ts = ktk.TimeSeries()
poussee_2_fp_ts = ktk.TimeSeries()
poussee_3_ls_ts = ktk.TimeSeries()
poussee_3_fp_ts = ktk.TimeSeries()

## Add data to the TimeSeries
poids_ls_ts.time = poids_pp_time_ls
poids_fp_ts.time = poids_pp_time_fp
pointe_1_ls_ts.time = pointe_1_pp_time_ls
pointe_1_fp_ts.time = pointe_1_pp_time_fp
pointe_3_ls_ts.time = pointe_3_pp_time_ls
pointe_3_fp_ts.time = pointe_3_pp_time_fp
pointe_5_ls_ts.time = pointe_5_pp_time_ls
pointe_5_fp_ts.time = pointe_5_pp_time_fp
poussee_1_ls_ts.time = poussee_1_pp_time_ls
poussee_1_fp_ts.time = poussee_1_pp_time_fp
poussee_2_ls_ts.time = poussee_2_pp_time_ls
poussee_2_fp_ts.time = poussee_2_pp_time_fp
poussee_3_ls_ts.time = poussee_3_pp_time_ls
poussee_3_fp_ts.time = poussee_3_pp_time_fp

poids_ls_ts.data = poids_pp_l_acc
poids_fp_ts.data = poids_pp_time_fp
pointe_1_ls_ts.data = pointe_1_pp_l_acc
pointe_1_fp_ts.data = pointe_1_pp_fp2
pointe_3_ls_ts.data = pointe_3_pp_l_acc
pointe_3_fp_ts.data = pointe_3_pp_fp2
pointe_5_ls_ts.data = pointe_5_pp_l_acc
pointe_5_fp_ts.data = pointe_5_pp_fp2
poussee_1_ls_ts.data = poussee_1_pp_l_acc
poussee_1_fp_ts.data = poussee_1_pp_fp2
poussee_2_ls_ts.data = poussee_2_pp_l_acc
poussee_2_fp_ts.data = poussee_2_pp_fp2
poussee_3_ls_ts.data = poussee_3_pp_l_acc
poussee_3_fp_ts.data = poussee_3_pp_fp2



# for val in [poids_raw_l_acc,pointe_1_raw_l_acc,pointe_3_raw_l_acc, pointe_5_raw_l_acc]:
#     plt.plot(val)
# plt.show()