# For each files in the examples directory, define manually the indexes of:
# Start signal: start
# Start specific movement: start_trial
# End specific movement: end_trial

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
    "roll_test_3.txt",
    "test_pointe_1_05_02.txt",
    "test_pointe_2_05_02.txt",
    "test_pointe_3_05_02.txt",
    "test_pointe_4_05_02.txt",
    "test_pointe_5_05_02.txt",
    "poids_par_zone.txt"
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

roll_test_ls = DataLoadsol(path=working_directory + txt_files[7], frequency=200)
pointe_1_ls_05_02 = DataLoadsol(path=working_directory + txt_files[8], frequency=200)
pointe_2_ls_05_02 = DataLoadsol(path=working_directory + txt_files[9], frequency=200)
pointe_3_ls_05_02 = DataLoadsol(path=working_directory + txt_files[10], frequency=200)
pointe_4_ls_05_02 = DataLoadsol(path=working_directory + txt_files[11], frequency=200)
pointe_5_ls_05_02 = DataLoadsol(path=working_directory + txt_files[12], frequency=200)
poids_par_zone = DataLoadsol(path=working_directory + txt_files[13], frequency=200)


# Define DataForceplates objects
poids_fp = DataForceplates(path=working_directory + c3d_files[0], frequency=1000)
pointe_1_fp = DataForceplates(path=working_directory + c3d_files[1], frequency=1000)
pointe_3_fp = DataForceplates(path=working_directory + c3d_files[2], frequency=1000)
pointe_5_fp = DataForceplates(path=working_directory + c3d_files[3], frequency=1000)
poussee_1_fp = DataForceplates(path=working_directory + c3d_files[4], frequency=1000)
poussee_2_fp = DataForceplates(path=working_directory + c3d_files[5], frequency=1000)
poussee_3_fp = DataForceplates(path=working_directory + c3d_files[6], frequency=1000)

# Convert txt files into csv files
if "rolll_test_3.csv" in listdir(working_directory):
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
    roll_test_ls.convert_txt_to_csv(working_directory)
    pointe_1_ls_05_02.convert_txt_to_csv(working_directory)
    pointe_2_ls_05_02.convert_txt_to_csv(working_directory)
    pointe_3_ls_05_02.convert_txt_to_csv(working_directory)
    pointe_4_ls_05_02.convert_txt_to_csv(working_directory)
    pointe_5_ls_05_02.convert_txt_to_csv(working_directory)
    poids_par_zone.convert_txt_to_csv(working_directory)
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

# Acceleration of the right insole (both are synchronised and the starting is defined by the right foot)
poids_pp_r_acc = poids_ls.get_pre_processed_data(insole_side="RIGHT", data_type="ACC")
pointe_1_pp_r_acc = pointe_1_ls.get_pre_processed_data(insole_side="RIGHT", data_type="ACC")
pointe_3_pp_r_acc = pointe_3_ls.get_pre_processed_data(insole_side="RIGHT", data_type="ACC")
pointe_5_pp_r_acc = pointe_5_ls.get_pre_processed_data(insole_side="RIGHT", data_type="ACC")
poussee_1_pp_r_acc = poussee_1_ls.get_pre_processed_data(insole_side="RIGHT", data_type="ACC")
poussee_2_pp_r_acc = poussee_2_ls.get_pre_processed_data(insole_side="RIGHT", data_type="ACC")
poussee_3_pp_r_acc = poussee_3_ls.get_pre_processed_data(insole_side="RIGHT", data_type="ACC")

# Total force of the right insole (both are synchronised and the starting is defined by the right foot)
poids_pp_r_f = poids_ls.get_pre_processed_data(insole_side="RIGHT", data_type="F_TOTAL")
pointe_1_pp_r_f = pointe_1_ls.get_pre_processed_data(insole_side="RIGHT", data_type="F_TOTAL")
pointe_3_pp_r_f = pointe_3_ls.get_pre_processed_data(insole_side="RIGHT", data_type="F_TOTAL")
pointe_5_pp_r_f = pointe_5_ls.get_pre_processed_data(insole_side="RIGHT", data_type="F_TOTAL")
poussee_1_pp_r_f = poussee_1_ls.get_pre_processed_data(insole_side="RIGHT", data_type="F_TOTAL")
poussee_2_pp_r_f = poussee_2_ls.get_pre_processed_data(insole_side="RIGHT", data_type="F_TOTAL")
poussee_3_pp_r_f = poussee_3_ls.get_pre_processed_data(insole_side="RIGHT", data_type="F_TOTAL")

# Forceceplate force in z direction for the forceplates 1 and 2
poids_pp_fp4 = poids_fp.get_pre_processed_data(forceplate_number=4)
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

poids_ls_ts.data = {'acc':poids_pp_r_acc}
poids_ls_ts.data = {'f':poids_pp_r_f}
poids_fp_ts.data = {'f':poids_pp_fp4}
pointe_1_ls_ts.data = {'acc':pointe_1_pp_r_acc}
pointe_1_ls_ts.data = {'f':pointe_1_pp_r_f}
pointe_1_fp_ts.data = {'f':pointe_1_pp_fp2}
pointe_3_ls_ts.data = {'acc':pointe_3_pp_r_acc}
pointe_3_ls_ts.data = {'f':pointe_3_pp_r_f}
pointe_3_fp_ts.data = {'f':pointe_3_pp_fp2}
pointe_5_ls_ts.data = {'acc':pointe_5_pp_r_acc}
pointe_5_ls_ts.data = {'f':pointe_5_pp_r_f}
pointe_5_fp_ts.data = {'f':pointe_5_pp_fp2}
poussee_1_ls_ts.data = {'acc':poussee_1_pp_r_acc}
poussee_1_ls_ts.data = {'f':poussee_1_pp_r_f}
poussee_1_fp_ts.data = {'f':poussee_1_pp_fp2}
poussee_2_ls_ts.data = {'acc':poussee_2_pp_r_acc}
poussee_2_ls_ts.data = {'f':poussee_2_pp_r_f}
poussee_2_fp_ts.data = {'f':poussee_2_pp_fp2}
poussee_3_ls_ts.data = {'acc':poussee_3_pp_r_acc}
poussee_3_ls_ts.data = {'f':poussee_3_pp_r_f}
poussee_3_fp_ts.data = {'f':poussee_3_pp_fp2}

# Create events manually
poids_ls_ts = poids_ls_ts.ui_edit_events()
# poids_fp_ts = poids_fp_ts.ui_edit_events()
pointe_1_ls_ts = pointe_1_ls_ts.ui_edit_events()
# pointe_1_fp_ts = pointe_1_fp_ts.ui_edit_events()
pointe_3_ls_ts = pointe_3_ls_ts.ui_edit_events()
# pointe_3_fp_ts = pointe_3_fp_ts.ui_edit_events()
pointe_5_ls_ts = pointe_5_ls_ts.ui_edit_events()
# pointe_5_fp_ts = pointe_5_fp_ts.ui_edit_events()
poussee_1_ls_ts = poussee_1_ls_ts.ui_edit_events()
# poussee_1_fp_ts = poussee_1_fp_ts.ui_edit_events()
poussee_2_ls_ts = poussee_2_ls_ts.ui_edit_events()
# poussee_2_fp_ts = poussee_2_fp_ts.ui_edit_events()
poussee_3_ls_ts = poussee_3_ls_ts.ui_edit_events()
# poussee_3_fp_ts = poussee_3_fp_ts.ui_edit_events()

# Get events
# print(f"Start poids_ls: {poids_ls_ts.get_index_before_event('start')}")
# print(f"Start poids_fp: {poids_fp_ts.get_index_before_event('start')}")
# print(f"Start pointe_1_ls: {pointe_1_ls_ts.get_index_before_event('start')}")
# print(f"Start pointe_1_fp: {pointe_1_fp_ts.get_index_before_event('start')}")
# print(f"Start pointe_3_ls: {pointe_3_ls_ts.get_index_before_event('start')}")
# print(f"Start pointe_3_fp: {pointe_3_fp_ts.get_index_before_event('start')}")
# print(f"Start pointe_5_ls: {pointe_5_ls_ts.get_index_before_event('start')}")
# print(f"Start pointe_5_fp: {pointe_5_fp_ts.get_index_before_event('start')}")
# print(f"Start poussee_1_ls: {poussee_1_ls_ts.get_index_before_event('start')}")
# print(f"Start poussee_1_fp: {poussee_1_fp_ts.get_index_before_event('start')}")
# print(f"Start poussee_2_ls: {poussee_2_ls_ts.get_index_before_event('start')}")
# print(f"Start poussee_2_fp: {poussee_2_fp_ts.get_index_before_event('start')}")
# print(f"Start poussee_3_ls: {poussee_3_ls_ts.get_index_before_event('start')}")
# print(f"Start poussee_3_fp: {poussee_3_fp_ts.get_index_before_event('start')}")

print(f"Start trial poids_ls: {poids_ls_ts.get_index_before_event('start_trial')}")
print(f"Start trial pointe_1_ls: {pointe_1_ls_ts.get_index_before_event('start_trial')}")
print(f"Start trial pointe_3_ls: {pointe_3_ls_ts.get_index_before_event('start_trial')}")
print(f"Start trial pointe_5_ls: {pointe_5_ls_ts.get_index_before_event('start_trial')}")
print(f"Start trial poussee_1_ls: {poussee_1_ls_ts.get_index_before_event('start_trial')}")
print(f"Start trial poussee_2_ls: {poussee_2_ls_ts.get_index_before_event('start_trial')}")
print(f"Start trial poussee_3_ls: {poussee_3_ls_ts.get_index_before_event('start_trial')}")

print(f"End trial poids_ls: {poids_ls_ts.get_index_before_event('end_trial')}")
print(f"End trial pointe_1_ls: {pointe_1_ls_ts.get_index_before_event('end_trial')}")
print(f"End trial pointe_3_ls: {pointe_3_ls_ts.get_index_before_event('end_trial')}")
print(f"End trial pointe_5_ls: {pointe_5_ls_ts.get_index_before_event('end_trial')}")
print(f"End trial poussee_1_ls: {poussee_1_ls_ts.get_index_before_event('end_trial')}")
print(f"End trial poussee_2_ls: {poussee_2_ls_ts.get_index_before_event('end_trial')}")
print(f"End trial poussee_3_ls: {poussee_3_ls_ts.get_index_before_event('end_trial')}")


## Results:
# Start poids_ls: 10
# Start poids_fp: 3847
# Start pointe_1_ls: 3488
# Start pointe_1_fp: 16743
# Start pointe_3_ls: 3465
# Start pointe_3_fp: 16825
# Start pointe_5_ls: 3412
# Start pointe_5_fp: 16598
# Start poussee_1_ls: 3009
# Start poussee_1_fp: 13718
# Start poussee_2_ls: 3165
# Start poussee_2_fp: 15384
# Start poussee_3_ls: 3644
# Start poussee_3_fp: 17745

# Start trial poids_ls: 756
# End trial poids_ls: 1040
# Start trial pointe_1_ls: 5211
# End trial pointe_1_ls: 12245
# Start trial pointe_3_ls: 4557
# End trial pointe_3_ls: 18475
# Start trial pointe_5_ls: 4719
# End trial pointe_5_ls: 10541
# Start trial poussee_1_ls: 4284
# End trial poussee_1_ls: 10314
# Start trial poussee_2_ls: 4172
# End trial poussee_2_ls: 11746
# Start trial poussee_3_ls: 5159
# End trial poussee_3_ls: 11441