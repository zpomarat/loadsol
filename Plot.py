# For each file in the examples directory, synchronise insoles and forceplates data and plot:

from os import getcwd, listdir
from Data import Data
from DataLoadsol import DataLoadsol
from DataForceplates import DataForceplates
import matplotlib.pyplot as plt

## Define the working directory
curr_path = getcwd()
working_directory = curr_path + "\\examples\\data\\"

## List of txt files in the directory
txt_files = [
    "test_poids.txt",
    "test_pointe_1.txt",
    "test_pointe_3.txt",
    "test_pointe_5.txt",
    "test_poussee_1.txt",
    "test_poussee_2.txt",
    "test_poussee_3.txt",
]

## List of c3d files in the directory
c3d_files = [
    "test_poids.c3d",
    "test_pointe_1.c3d",
    "test_pointe_3.c3d",
    "test_pointe_5.c3d",
    "test_poussee_1.c3d",
    "test_poussee_2.c3d",
    "test_poussee_3.c3d",
]

## Define DataLoadsol objects
poids_ls = DataLoadsol(path=working_directory + txt_files[0], frequency=200)
pointe_1_ls = DataLoadsol(path=working_directory + txt_files[1], frequency=200)
pointe_3_ls = DataLoadsol(path=working_directory + txt_files[2], frequency=200)
pointe_5_ls = DataLoadsol(path=working_directory + txt_files[3], frequency=200)
poussee_1_ls = DataLoadsol(path=working_directory + txt_files[4], frequency=200)
poussee_2_ls = DataLoadsol(path=working_directory + txt_files[5], frequency=200)
poussee_3_ls = DataLoadsol(path=working_directory + txt_files[6], frequency=200)

## Define DataForceplates objects
poids_fp = DataForceplates(path=working_directory + c3d_files[0], frequency=1000)
pointe_1_fp = DataForceplates(path=working_directory + c3d_files[1], frequency=1000)
pointe_3_fp = DataForceplates(path=working_directory + c3d_files[2], frequency=1000)
pointe_5_fp = DataForceplates(path=working_directory + c3d_files[3], frequency=1000)
poussee_1_fp = DataForceplates(path=working_directory + c3d_files[4], frequency=1000)
poussee_2_fp = DataForceplates(path=working_directory + c3d_files[5], frequency=1000)
poussee_3_fp = DataForceplates(path=working_directory + c3d_files[6], frequency=1000)

## Convert txt files into csv files
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

## Get variables of interest
# Insoles time
poids_time_ls = poids_ls.get_filled_time()   
pointe_1_time_ls = pointe_1_ls.get_filled_time()
pointe_3_time_ls = pointe_3_ls.get_filled_time()
pointe_5_time_ls = pointe_5_ls.get_filled_time()
poussee_1_time_ls = poussee_1_ls.get_filled_time()
poussee_2_time_ls = poussee_2_ls.get_filled_time()
poussee_3_time_ls = poussee_3_ls.get_filled_time()

# Acceleration of the left insole
poids_l_acc = poids_ls.get_filled_data(insole_side="LEFT", data_type="ACC")
pointe_1_l_acc = pointe_1_ls.get_filled_data(insole_side="LEFT", data_type="ACC")
pointe_3_l_acc = pointe_3_ls.get_filled_data(insole_side="LEFT", data_type="ACC")
pointe_5_l_acc = pointe_5_ls.get_filled_data(insole_side="LEFT", data_type="ACC")
poussee_1_l_acc = poussee_1_ls.get_filled_data(insole_side="LEFT", data_type="ACC")
poussee_2_l_acc = poussee_2_ls.get_filled_data(insole_side="LEFT", data_type="ACC")
poussee_3_l_acc = poussee_3_ls.get_filled_data(insole_side="LEFT", data_type="ACC")

# Acceleration of the right insole
poids_r_acc = poids_ls.get_filled_data(insole_side="RIGHT", data_type="ACC")
pointe_1_r_acc = pointe_1_ls.get_filled_data(insole_side="RIGHT", data_type="ACC")
pointe_3_r_acc = pointe_3_ls.get_filled_data(insole_side="RIGHT", data_type="ACC")
pointe_5_r_acc = pointe_5_ls.get_filled_data(insole_side="RIGHT", data_type="ACC")
poussee_1_r_acc = poussee_1_ls.get_filled_data(insole_side="RIGHT", data_type="ACC")
poussee_2_r_acc = poussee_2_ls.get_filled_data(insole_side="RIGHT", data_type="ACC")
poussee_3_r_acc = poussee_3_ls.get_filled_data(insole_side="RIGHT", data_type="ACC")

# Angular velocity of the left insole
poids_l_gyro = poids_ls.get_filled_data(insole_side="LEFT", data_type="GYRO")
pointe_1_l_gyro = pointe_1_ls.get_filled_data(insole_side="LEFT", data_type="GYRO")
pointe_3_l_gyro = pointe_3_ls.get_filled_data(insole_side="LEFT", data_type="GYRO")
pointe_5_l_gyro = pointe_5_ls.get_filled_data(insole_side="LEFT", data_type="GYRO")
poussee_1_l_gyro = poussee_1_ls.get_filled_data(insole_side="LEFT", data_type="GYRO")
poussee_2_l_gyro = poussee_2_ls.get_filled_data(insole_side="LEFT", data_type="GYRO")
poussee_3_l_gyro = poussee_3_ls.get_filled_data(insole_side="LEFT", data_type="GYRO")

# Angular of the right insole
poids_r_gyro = poids_ls.get_filled_data(insole_side="RIGHT", data_type="GYRO")
pointe_1_r_gyro = pointe_1_ls.get_filled_data(insole_side="RIGHT", data_type="GYRO")
pointe_3_r_gyro = pointe_3_ls.get_filled_data(insole_side="RIGHT", data_type="GYRO")
pointe_5_r_gyro = pointe_5_ls.get_filled_data(insole_side="RIGHT", data_type="GYRO")
poussee_1_r_gyro = poussee_1_ls.get_filled_data(insole_side="RIGHT", data_type="GYRO")
poussee_2_r_gyro = poussee_2_ls.get_filled_data(insole_side="RIGHT", data_type="GYRO")
poussee_3_r_gyro = poussee_3_ls.get_filled_data(insole_side="RIGHT", data_type="GYRO")

# Heel force on the left insole
poids_l_fheel = poids_ls.get_filled_data(insole_side="LEFT",data_type="F_HEEL")
pointe_1_l_fheel = pointe_1_ls.get_filled_data(insole_side="LEFT",data_type="F_HEEL")
pointe_3_l_fheel = pointe_3_ls.get_filled_data(insole_side="LEFT",data_type="F_HEEL")
pointe_5_l_fheel = pointe_5_ls.get_filled_data(insole_side="LEFT",data_type="F_HEEL")
poussee_1_l_fheel = poussee_1_ls.get_filled_data(insole_side="LEFT",data_type="F_HEEL")
poussee_2_l_fheel = poussee_2_ls.get_filled_data(insole_side="LEFT",data_type="F_HEEL")
poussee_3_l_fheel = poussee_3_ls.get_filled_data(insole_side="LEFT",data_type="F_HEEL")

# Heel force on the right insole
poids_r_fheel = poids_ls.get_filled_data(insole_side="RIGHT",data_type="F_HEEL")
pointe_1_r_fheel = pointe_1_ls.get_filled_data(insole_side="RIGHT",data_type="F_HEEL")
pointe_3_r_fheel = pointe_3_ls.get_filled_data(insole_side="RIGHT",data_type="F_HEEL")
pointe_5_r_fheel = pointe_5_ls.get_filled_data(insole_side="RIGHT",data_type="F_HEEL")
poussee_1_r_fheel = poussee_1_ls.get_filled_data(insole_side="RIGHT",data_type="F_HEEL")
poussee_2_r_fheel = poussee_2_ls.get_filled_data(insole_side="RIGHT",data_type="F_HEEL")
poussee_3_r_fheel = poussee_3_ls.get_filled_data(insole_side="RIGHT",data_type="F_HEEL")

# Medial force on the left insole
poids_l_fmedial = poids_ls.get_filled_data(insole_side="LEFT",data_type="F_MEDIAL")
pointe_1_l_fmedial = pointe_1_ls.get_filled_data(insole_side="LEFT",data_type="F_MEDIAL")
pointe_3_l_fmedial = pointe_3_ls.get_filled_data(insole_side="LEFT",data_type="F_MEDIAL")
pointe_5_l_fmedial = pointe_5_ls.get_filled_data(insole_side="LEFT",data_type="F_MEDIAL")
poussee_1_l_fmedial = poussee_1_ls.get_filled_data(insole_side="LEFT",data_type="F_MEDIAL")
poussee_2_l_fmedial = poussee_2_ls.get_filled_data(insole_side="LEFT",data_type="F_MEDIAL")
poussee_3_l_fmedial = poussee_3_ls.get_filled_data(insole_side="LEFT",data_type="F_MEDIAL")

# Medial force on the right insole
poids_r_fmedial = poids_ls.get_filled_data(insole_side="RIGHT",data_type="F_MEDIAL")
pointe_1_r_fmedial = pointe_1_ls.get_filled_data(insole_side="RIGHT",data_type="F_MEDIAL")
pointe_3_r_fmedial = pointe_3_ls.get_filled_data(insole_side="RIGHT",data_type="F_MEDIAL")
pointe_5_r_fmedial = pointe_5_ls.get_filled_data(insole_side="RIGHT",data_type="F_MEDIAL")
poussee_1_r_fmedial = poussee_1_ls.get_filled_data(insole_side="RIGHT",data_type="F_MEDIAL")
poussee_2_r_fmedial = poussee_2_ls.get_filled_data(insole_side="RIGHT",data_type="F_MEDIAL")
poussee_3_r_fmedial = poussee_3_ls.get_filled_data(insole_side="RIGHT",data_type="F_MEDIAL")

# Lateral force on the left insole
poids_l_flateral = poids_ls.get_filled_data(insole_side="LEFT",data_type="F_LATERAL")
pointe_1_l_flateral = pointe_1_ls.get_filled_data(insole_side="LEFT",data_type="F_LATERAL")
pointe_3_l_flateral = pointe_3_ls.get_filled_data(insole_side="LEFT",data_type="F_LATERAL")
pointe_5_l_flateral = pointe_5_ls.get_filled_data(insole_side="LEFT",data_type="F_LATERAL")
poussee_1_l_flateral = poussee_1_ls.get_filled_data(insole_side="LEFT",data_type="F_LATERAL")
poussee_2_l_flateral = poussee_2_ls.get_filled_data(insole_side="LEFT",data_type="F_LATERAL")
poussee_3_l_flateral = poussee_3_ls.get_filled_data(insole_side="LEFT",data_type="F_LATERAL")

# Lateral force on the right insole
poids_r_flateral = poids_ls.get_filled_data(insole_side="RIGHT",data_type="F_LATERAL")
pointe_1_r_flateral = pointe_1_ls.get_filled_data(insole_side="RIGHT",data_type="F_LATERAL")
pointe_3_r_flateral = pointe_3_ls.get_filled_data(insole_side="RIGHT",data_type="F_LATERAL")
pointe_5_r_flateral = pointe_5_ls.get_filled_data(insole_side="RIGHT",data_type="F_LATERAL")
poussee_1_r_flateral = poussee_1_ls.get_filled_data(insole_side="RIGHT",data_type="F_LATERAL")
poussee_2_r_flateral = poussee_2_ls.get_filled_data(insole_side="RIGHT",data_type="F_LATERAL")
poussee_3_r_flateral = poussee_3_ls.get_filled_data(insole_side="RIGHT",data_type="F_LATERAL")

# Total force on the left insole
poids_l_ftotal = poids_ls.get_filled_data(insole_side="LEFT",data_type="F_TOTAL")
pointe_1_l_ftotal = pointe_1_ls.get_filled_data(insole_side="LEFT",data_type="F_TOTAL")
pointe_3_l_ftotal = pointe_3_ls.get_filled_data(insole_side="LEFT",data_type="F_TOTAL")
pointe_5_l_ftotal = pointe_5_ls.get_filled_data(insole_side="LEFT",data_type="F_TOTAL")
poussee_1_l_ftotal = poussee_1_ls.get_filled_data(insole_side="LEFT",data_type="F_TOTAL")
poussee_2_l_ftotal = poussee_2_ls.get_filled_data(insole_side="LEFT",data_type="F_TOTAL")
poussee_3_l_ftotal = poussee_3_ls.get_filled_data(insole_side="LEFT",data_type="F_TOTAL")

# Total force on the right insole
poids_r_ftotal = poids_ls.get_filled_data(insole_side="RIGHT",data_type="F_TOTAL")
pointe_1_r_ftotal = pointe_1_ls.get_filled_data(insole_side="RIGHT",data_type="F_TOTAL")
pointe_3_r_ftotal = pointe_3_ls.get_filled_data(insole_side="RIGHT",data_type="F_TOTAL")
pointe_5_r_ftotal = pointe_5_ls.get_filled_data(insole_side="RIGHT",data_type="F_TOTAL")
poussee_1_r_ftotal = poussee_1_ls.get_filled_data(insole_side="RIGHT",data_type="F_TOTAL")
poussee_2_r_ftotal = poussee_2_ls.get_filled_data(insole_side="RIGHT",data_type="F_TOTAL")
poussee_3_r_ftotal = poussee_3_ls.get_filled_data(insole_side="RIGHT",data_type="F_TOTAL")

# Forceplates time
poids_time_fp_ds = poids_fp.downsample(final_frequency=200,time=poids_fp.get_filled_time())
pointe_1_time_fp = pointe_1_fp.downsample(final_frequency=200,time=pointe_1_fp.get_filled_time())
pointe_3_time_fp = pointe_3_fp.downsample(final_frequency=200,time=pointe_3_fp.get_filled_time())
pointe_5_time_fp = pointe_5_fp.downsample(final_frequency=200,time=pointe_5_fp.get_filled_time())
poussee_1_time_fp = poussee_1_fp.downsample(final_frequency=200,time=poussee_1_fp.get_filled_time())
poussee_2_time_fp = poussee_2_fp.downsample(final_frequency=200,time=poussee_2_fp.get_filled_time())
poussee_3_time_fp = poussee_3_fp.downsample(final_frequency=200,time=poussee_3_fp.get_filled_time())

# Forces on the forceplate number 1 (left foot)
poids_fp1 = poids_fp.downsample(final_frequency=200,forceplate_number=1)
pointe_1_fp1 = pointe_1_fp.downsample(final_frequency=200,forceplate_number=1)
pointe_3_fp1 = pointe_3_fp.downsample(final_frequency=200,forceplate_number=1)
pointe_5_fp1 = pointe_5_fp.downsample(final_frequency=200,forceplate_number=1)
poussee_1_fp1 = poussee_1_fp.downsample(final_frequency=200,forceplate_number=1)
poussee_2_fp1 = poussee_2_fp.downsample(final_frequency=200,forceplate_number=1)
poussee_3_fp1 = poussee_3_fp.downsample(final_frequency=200,forceplate_number=1)

# Forces on the forceplate number 2 (right foot)
poids_fp2 = poids_fp.downsample(final_frequency=200,forceplate_number=2)
pointe_1_fp2 = pointe_1_fp.downsample(final_frequency=200,forceplate_number=2)
pointe_3_fp2 = pointe_3_fp.downsample(final_frequency=200,forceplate_number=2)
pointe_5_fp2 = pointe_5_fp.downsample(final_frequency=200,forceplate_number=2)
poussee_1_fp2 = poussee_1_fp.downsample(final_frequency=200,forceplate_number=2)
poussee_2_fp2 = poussee_2_fp.downsample(final_frequency=200,forceplate_number=2)
poussee_3_fp2 = poussee_3_fp.downsample(final_frequency=200,forceplate_number=2)

plt.plot(pointe_1_time_ls,pointe_1_l_fheel,label='heel')
plt.plot(pointe_1_time_ls,pointe_1_l_fmedial,label='medial')
plt.plot(pointe_1_time_ls,pointe_1_l_flateral,label='lateral')
plt.plot(pointe_1_time_ls,pointe_1_l_ftotal,label='total')
plt.legend()
plt.show()
