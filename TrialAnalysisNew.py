from os import getcwd, listdir
from copy import deepcopy
from DataLoadsolNew import DataLoadsol
from DataForceplatesNew import DataForceplates
import matplotlib.pyplot as plt
import pandas as pd


class TrialAnalysis:
    def __init__(
        self,
        DataLoadSol: DataLoadsol,
        DataForcePlates: DataForceplates,
        sync_index_loadsol: int,
        sync_index_forceplates: int,
        final_frequency: int,
    ):
        self.data_loadsol = deepcopy(DataLoadSol)
        self.data_forceplates = deepcopy(DataForcePlates)
        self.data_loadsol_sync = None
        self.data_forceplates_sync = None

        ## Synchronise manually signals
        # Initialise synchronised data
        if DataLoadSol is not None:
            self.data_loadsol.downsample(final_frequency)
        if DataForcePlates is not None:
            self.data_forceplates.downsample(final_frequency)

        self.data_loadsol_sync = deepcopy(self.data_loadsol.downsampled_data)
        self.data_forceplates_sync = deepcopy(self.data_forceplates.downsampled_data)

        # Start signals at the start index
        for key_ls in self.data_loadsol_sync.keys():
            self.data_loadsol_sync[key_ls] = self.data_loadsol_sync[key_ls][
                sync_index_loadsol:
            ]

        for key_fp in self.data_forceplates_sync.keys():
            self.data_forceplates_sync[key_fp] = self.data_forceplates_sync[key_fp][
                sync_index_forceplates:
            ]
       
        # Cut signals to the dimension of the smallest one
        min_len = min(len(self.data_loadsol_sync["time"]), len(self.data_forceplates_sync["time"]))

        for key_ls in self.data_loadsol_sync.keys():
            self.data_loadsol_sync[key_ls] = self.data_loadsol_sync[key_ls][:min_len]

        for key_fp in self.data_forceplates_sync.keys():
            self.data_forceplates_sync[key_fp] = self.data_forceplates_sync[key_fp][:min_len]

        # Start time to zero
        self.data_loadsol_sync["time"] -= self.data_loadsol_sync["time"][0]
        self.data_forceplates_sync["time"] -= self.data_forceplates_sync["time"][0]

    def export_csv(self,export_directory:str, file_name:str):

        # Data to export
        data = {
            "Time": self.data_loadsol_sync["time"],
            "F_heel_left": self.data_loadsol_sync["f_heel_l"],
            "F_medial_left": self.data_loadsol_sync["f_medial_l"],
            "F_lateral_left": self.data_loadsol_sync["f_lateral_l"],
            "F_total_left": self.data_loadsol_sync["f_total_l"],
            "F_acc_x_left": self.data_loadsol_sync["acc_x_l"],
            "F_acc_y_left": self.data_loadsol_sync["acc_y_l"],
            "F_acc_z_left": self.data_loadsol_sync["acc_z_l"],
            "F_gyro_x_left": self.data_loadsol_sync["gyro_x_l"],
            "F_gyro_y_left": self.data_loadsol_sync["gyro_y_l"],
            "F_gyro_z_left": self.data_loadsol_sync["gyro_z_l"],
            "F_heel_right": self.data_loadsol_sync["f_heel_r"],
            "F_medial_right": self.data_loadsol_sync["f_medial_r"],
            "F_lateral_right": self.data_loadsol_sync["f_lateral_r"],
            "F_total_right": self.data_loadsol_sync["f_total_r"],
            "F_acc_x_right": self.data_loadsol_sync["acc_x_r"],
            "F_acc_y_right": self.data_loadsol_sync["acc_y_r"],
            "F_acc_z_right": self.data_loadsol_sync["acc_z_r"],
            "F_gyro_x_right": self.data_loadsol_sync["gyro_x_r"],
            "F_gyro_y_right": self.data_loadsol_sync["gyro_y_r"],
            "F_gyro_z_right": self.data_loadsol_sync["gyro_z_r"],
            "Fx_left": self.data_forceplates_sync["fx1"],
            "Fy_left": self.data_forceplates_sync["fy1"],
            "Fz_left": self.data_forceplates_sync["fz1"],
            "Fx_right": self.data_forceplates_sync["fx2"],
            "Fy_right": self.data_forceplates_sync["fy2"],
            "Fz_right": self.data_forceplates_sync["fz2"],
        }

        # Create a dataframe containing data to export
        df = pd.DataFrame(data)

        # Export data to a csv file
        df.to_csv(export_directory + file_name + "_processed.csv")


if __name__ == "__main__":
    curr_path = getcwd()
    working_directory = curr_path + "\\tests_09_02_24\\data\\"

    # List of trial names
    files_names = listdir(working_directory)
    
    trial_names = []
    for name in files_names:
        n = name.split(".")[0]
        if n not in trial_names:
            trial_names.append(n)

    # List of indexes of synchronisation
    index_ls = [2345,1676,3717,1685,1883,1481,5623,10115,3858,4304,4079,5096]
    index_fp = [12092,9759,11027,9634,10285,8747,45720,52187,20371,23160,21143,27272]

    for name, idx_ls, idx_fp in zip(trial_names, index_ls, index_fp):
        file_name = name

        data_ls = DataLoadsol(
            path=working_directory + file_name + ".txt", frequency=200
        )

        data_fp = DataForceplates(
            path=working_directory + file_name + ".c3d", frequency=1000
        )

        Trial = TrialAnalysis(
            DataLoadSol=data_ls, DataForcePlates=data_fp, final_frequency=200, sync_index_loadsol=idx_ls, sync_index_forceplates=int(idx_fp/5)
        )

        Trial.export_csv(export_directory=curr_path + "\\tests_09_02_24\\results\\",file_name=file_name)

    #     # Initialise data (synchronised + downsampled signals)
    #     plt.plot(Trial.data_loadsol_sync["time"],Trial.data_loadsol_sync['f_total_l'],"-o",label="f total left")
    #     plt.plot(Trial.data_forceplates_sync["time"],Trial.data_forceplates_sync["fz1"],"-x",label="fz1")
    #     plt.xlabel("Time (s)")
    #     plt.ylabel("Force (N)")
    #     plt.legend()
    #     plt.title("Synchronised and resampled data (" + name + ")")
    #     plt.figure()
    # plt.show()

