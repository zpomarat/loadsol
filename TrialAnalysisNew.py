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
        data_state = "raw",
        order = 4,
        fcut = 20
    ):
        self.data_loadsol = deepcopy(DataLoadSol)
        self.data_forceplates = deepcopy(DataForcePlates)
        self.data_loadsol_sync = None
        self.data_forceplates_sync = None

        ## Synchronise manually signals
        # Initialise synchronised data
        if data_state is "raw":
            if DataLoadSol is not None:
                self.data_loadsol.downsample(final_frequency)
            if DataForcePlates is not None:
                self.data_forceplates.downsample(final_frequency)

            self.data_loadsol_sync = deepcopy(self.data_loadsol.downsampled_data)
            self.data_forceplates_sync = deepcopy(self.data_forceplates.downsampled_data)

        elif data_state is "filtered":
            if DataLoadSol is not None:
                self.data_loadsol.filter(fs = final_frequency, order = order, fcut = fcut)
            if DataForcePlates is not None:
                self.data_forceplates.filter(fs = final_frequency, order = order, fcut = fcut)

            self.data_loadsol_sync = deepcopy(self.data_loadsol.filtered_data)
            self.data_forceplates_sync = deepcopy(self.data_forceplates.filtered_data)

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

    def compare_loadsol_forceplates(self):
        fig1, axs = plt.subplots(2)
        fig1.suptitle("Comparison FP / LS")
        axs[0].set_title("Left insole")
        axs[0].plot(self.time_ls, self.l_f_heel, label="heel")
        axs[0].plot(self.time_ls, self.l_f_medial, label="medial")
        axs[0].plot(self.time_ls, self.l_f_lateral, label="lateral")
        axs[0].plot(self.time_ls, self.l_f_total, label="total")
        axs[0].plot(self.time_fp, self.fp1_x, "-.", label="Fx")
        axs[0].plot(self.time_fp, self.fp1_y, "-.", label="Fy")
        axs[0].plot(self.time_fp, self.fp1_z, "-.", label="Fz")

        axs[1].set_title("Right insole")
        axs[1].plot(self.time_ls, self.r_f_heel, label="heel")
        axs[1].plot(self.time_ls, self.r_f_medial, label="medial")
        axs[1].plot(self.time_ls, self.r_f_lateral, label="lateral")
        axs[1].plot(self.time_ls, self.r_f_total, label="total")
        axs[1].plot(self.time_fp, self.fp2_x, "-.", label="Fx")
        axs[1].plot(self.time_fp, self.fp2_y, "-.", label="Fy")
        axs[1].plot(self.time_fp, self.fp2_z, "-.", label="Fz")

        axs[0].set_xlabel("Time (s)")
        axs[0].set_ylabel("Force (N)")
        axs[1].set_xlabel("Time (s)")
        axs[1].set_ylabel("Force (N)")

        axs[0].legend()
        axs[1].legend()
        fig1.subplots_adjust(hspace=0.3)
        plt.show()


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
            DataLoadSol=data_ls, DataForcePlates=data_fp, final_frequency=200, sync_index_loadsol=idx_ls, sync_index_forceplates=int(idx_fp/5), data_state = "filtered"
        )

        Trial.export_csv(export_directory=curr_path + "\\tests_09_02_24\\results\\filtered\\",file_name=file_name)

    #     # Initialise data (synchronised + downsampled signals)
    #     plt.plot(Trial.data_loadsol_sync["time"],Trial.data_loadsol_sync['f_total_l'],"-o",label="f total left")
    #     plt.plot(Trial.data_forceplates_sync["time"],Trial.data_forceplates_sync["fz1"],"-x",label="fz1")
    #     plt.xlabel("Time (s)")
    #     plt.ylabel("Force (N)")
    #     plt.legend()
    #     plt.title("Synchronised and resampled data (" + name + ")")
    #     plt.figure()
    # plt.show()

