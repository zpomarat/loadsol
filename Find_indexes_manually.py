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

# List of DataLoadsol objects
data_ls_list = [
    "poids_ls",
    "pointe_1_ls",
    "pointe_3_ls",
    "pointe_5_ls",
    "poussee_1_ls",
    "poussee_2_ls",
    "poussee_3_ls",
]

# Define DataForceplates objects
poids_fp = DataForceplates(path=working_directory + c3d_files[0], frequency=1000)
pointe_1_fp = DataForceplates(path=working_directory + c3d_files[1], frequency=1000)
pointe_3_fp = DataForceplates(path=working_directory + c3d_files[2], frequency=1000)
pointe_5_fp = DataForceplates(path=working_directory + c3d_files[3], frequency=1000)
poussee_1_fp = DataForceplates(path=working_directory + c3d_files[4], frequency=1000)
poussee_2_fp = DataForceplates(path=working_directory + c3d_files[5], frequency=1000)
poussee_3_fp = DataForceplates(path=working_directory + c3d_files[6], frequency=1000)

# List of DataLoadsol objects
data_fp_list = [
    "poids_fp",
    "pointe_1_fp",
    "pointe_3_fp",
    "pointe_5_fp",
    "poussee_1_fp",
    "poussee_2_fp",
    "poussee_3_fp",
]

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
# Acceleration of one insole (both are synchronised)
poids_raw_l_acc = poids_ls.get_raw_data(insole_side="LEFT", data_type="ACC")
pointe_1_raw_l_acc = pointe_1_ls.get_raw_data(insole_side="LEFT", data_type="ACC")
pointe_3_raw_l_acc = pointe_3_ls.get_raw_data(insole_side="LEFT", data_type="ACC")
pointe_5_raw_l_acc = pointe_5_ls.get_raw_data(insole_side="LEFT", data_type="ACC")

