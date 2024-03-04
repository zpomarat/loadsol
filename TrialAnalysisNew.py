from os import getcwd, listdir
from copy import deepcopy
from DataLoadsolNew import DataLoadsol
from DataForceplatesNew import DataForceplates
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


class TrialAnalysis:
    def __init__(
        self,
        DataLoadSol: DataLoadsol,
        DataForcePlates: DataForceplates,
        sync_index_loadsol: int,
        sync_index_forceplates: int,
        final_frequency: int,
        data_state = "pre_processed",
        order = 4,
        fcut = 20
    ):
        self.data_loadsol = deepcopy(DataLoadSol)
        self.data_forceplates = deepcopy(DataForcePlates)
        self.data_loadsol_sync = None
        self.data_forceplates_sync = None
        self.data_state = data_state

        ## Synchronise manually signals
        # Initialise synchronised data
        if data_state == "pre_processed":
            if DataLoadSol is not None:
                self.data_loadsol.downsample(final_frequency)
                self.data_loadsol_sync = deepcopy(self.data_loadsol.downsampled_data)
            if DataForcePlates is not None:
                self.data_forceplates.downsample(final_frequency)
                self.data_forceplates_sync = deepcopy(self.data_forceplates.downsampled_data)
            
        elif data_state == "filtered":
            if DataLoadSol is not None:
                self.data_loadsol.filter(fs = final_frequency, order = order, fcut = fcut)
                self.data_loadsol_sync = deepcopy(self.data_loadsol.filtered_data)
            if DataForcePlates is not None:
                self.data_forceplates.filter(fs = final_frequency, order = order, fcut = fcut)
                self.data_forceplates_sync = deepcopy(self.data_forceplates.filtered_data)
            
        # Start signals at the start index
        if DataLoadSol is not None and DataForcePlates is not None:
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

        axs[0].plot(self.data_loadsol_sync["time"], self.data_loadsol_sync["f_heel_l"], label="heel")
        axs[0].plot(self.data_loadsol_sync["time"], self.data_loadsol_sync["f_medial_l"], label="medial")
        axs[0].plot(self.data_loadsol_sync["time"], self.data_loadsol_sync["f_lateral_l"], label="lateral")
        axs[0].plot(self.data_loadsol_sync["time"], self.data_loadsol_sync["f_total_l"], label="total")
        axs[0].plot(self.data_forceplates_sync["time"], self.data_forceplates_sync["fx1"], "-.", label="Fx")
        axs[0].plot(self.data_forceplates_sync["time"], self.data_forceplates_sync["fy1"], "-.", label="Fy")
        axs[0].plot(self.data_forceplates_sync["time"], self.data_forceplates_sync["fz1"], "-.", label="Fz")

        axs[1].set_title("Right insole")
        axs[1].plot(self.data_loadsol_sync["time"], self.data_loadsol_sync["f_heel_r"], label="heel")
        axs[1].plot(self.data_loadsol_sync["time"], self.data_loadsol_sync["f_medial_r"], label="medial")
        axs[1].plot(self.data_loadsol_sync["time"], self.data_loadsol_sync["f_lateral_r"], label="lateral")
        axs[1].plot(self.data_loadsol_sync["time"], self.data_loadsol_sync["f_total_r"], label="total")
        axs[1].plot(self.data_forceplates_sync["time"], self.data_forceplates_sync["fx2"], "-.", label="Fx")
        axs[1].plot(self.data_forceplates_sync["time"], self.data_forceplates_sync["fy2"], "-.", label="Fy")
        axs[1].plot(self.data_forceplates_sync["time"], self.data_forceplates_sync["fz2"], "-.", label="Fz")

        axs[0].set_xlabel("Time (s)")
        axs[0].set_ylabel("Force (N)")
        axs[1].set_xlabel("Time (s)")
        axs[1].set_ylabel("Force (N)")

        axs[0].legend()
        axs[1].legend()
        fig1.subplots_adjust(hspace=0.3)
        plt.show()

    def compare_forces_imu(self):
        fig1, axs = plt.subplots(3)
        fig1.suptitle("Comparison LS forces / IMU left insole")
        axs[0].set_title("Forces")
        if self.data_state == "pre_processed":
            axs[0].plot(self.data_loadsol.downsampled_data["time"], self.data_loadsol.downsampled_data["f_heel_l"], label="heel")
            axs[0].plot(self.data_loadsol.downsampled_data["time"], self.data_loadsol.downsampled_data["f_medial_l"], label="medial")
            axs[0].plot(self.data_loadsol.downsampled_data["time"], self.data_loadsol.downsampled_data["f_lateral_l"], label="lateral")
            axs[0].plot(self.data_loadsol.downsampled_data["time"], self.data_loadsol.downsampled_data["f_total_l"], label="total")
        elif self.data_state == "filtered":
            axs[0].plot(self.data_loadsol.filtered_data["time"], self.data_loadsol.filtered_data["f_heel_l"], label="heel")
            axs[0].plot(self.data_loadsol.filtered_data["time"], self.data_loadsol.filtered_data["f_medial_l"], label="medial")
            axs[0].plot(self.data_loadsol.filtered_data["time"], self.data_loadsol.filtered_data["f_lateral_l"], label="lateral")
            axs[0].plot(self.data_loadsol.filtered_data["time"], self.data_loadsol.filtered_data["f_total_l"], label="total")

        axs[1].set_title("Accelerometer")
        if self.data_state == "pre_processed":
            axs[1].plot(self.data_loadsol.downsampled_data["time"], self.data_loadsol.downsampled_data["acc_x_l"], label="acc x")
            axs[1].plot(self.data_loadsol.downsampled_data["time"], self.data_loadsol.downsampled_data["acc_y_l"], label="acc y")
            axs[1].plot(self.data_loadsol.downsampled_data["time"], self.data_loadsol.downsampled_data["acc_z_l"], label="acc z")
        elif self.data_state == "filtered":
            axs[1].plot(self.data_loadsol.filtered_data["time"], self.data_loadsol.filtered_data["acc_x_l"], label="acc x")
            axs[1].plot(self.data_loadsol.filtered_data["time"], self.data_loadsol.filtered_data["acc_y_l"], label="acc y")
            axs[1].plot(self.data_loadsol.filtered_data["time"], self.data_loadsol.filtered_data["acc_z_l"], label="acc z")

        axs[2].set_title("Gyrometer")
        if self.data_state == "pre_processed":
            axs[2].plot(self.data_loadsol.downsampled_data["time"], self.data_loadsol.downsampled_data["gyro_x_l"], label="gyro x")
            axs[2].plot(self.data_loadsol.downsampled_data["time"], self.data_loadsol.downsampled_data["gyro_y_l"], label="gyro y")
            axs[2].plot(self.data_loadsol.downsampled_data["time"], self.data_loadsol.downsampled_data["gyro_z_l"], label="gyro z")
        elif self.data_state == "filtered":
            axs[2].plot(self.data_loadsol.filtered_data["time"], self.data_loadsol.filtered_data["gyro_x_l"], label="gyro x")
            axs[2].plot(self.data_loadsol.filtered_data["time"], self.data_loadsol.filtered_data["gyro_y_l"], label="gyro y")
            axs[2].plot(self.data_loadsol.filtered_data["time"], self.data_loadsol.filtered_data["gyro_z_l"], label="gyro z")

        axs[0].set_xlabel("Time (s)")
        axs[0].set_ylabel("Force (N)")
        axs[1].set_xlabel("Time (s)")
        axs[1].set_ylabel("Acceleration (g)")
        axs[2].set_xlabel("Time (s)")
        axs[2].set_ylabel("Angular velocity (rad/s)")

        axs[0].legend()
        axs[1].legend()
        axs[2].legend()
        fig1.subplots_adjust(hspace=0.3)

        fig2, axs = plt.subplots(3)
        fig2.suptitle("Comparison LS forces / IMU right insole")
        axs[0].set_title("Forces")
        if self.data_state == "pre_processed":
            axs[0].plot(self.data_loadsol.downsampled_data["time"], self.data_loadsol.downsampled_data["f_heel_r"], label="heel")
            axs[0].plot(self.data_loadsol.downsampled_data["time"], self.data_loadsol.downsampled_data["f_medial_r"], label="medial")
            axs[0].plot(self.data_loadsol.downsampled_data["time"], self.data_loadsol.downsampled_data["f_lateral_r"], label="lateral")
            axs[0].plot(self.data_loadsol.downsampled_data["time"], self.data_loadsol.downsampled_data["f_total_r"], label="total")
        elif self.data_state == "filtered":
            axs[0].plot(self.data_loadsol.filtered_data["time"], self.data_loadsol.filtered_data["f_heel_r"], label="heel")
            axs[0].plot(self.data_loadsol.filtered_data["time"], self.data_loadsol.filtered_data["f_medial_r"], label="medial")
            axs[0].plot(self.data_loadsol.filtered_data["time"], self.data_loadsol.filtered_data["f_lateral_r"], label="lateral")
            axs[0].plot(self.data_loadsol.filtered_data["time"], self.data_loadsol.filtered_data["f_total_r"], label="total")

        axs[1].set_title("Accelerometer")
        if self.data_state == "pre_processed":
            axs[1].plot(self.data_loadsol.downsampled_data["time"], self.data_loadsol.downsampled_data["acc_x_r"], label="acc x")
            axs[1].plot(self.data_loadsol.downsampled_data["time"], self.data_loadsol.downsampled_data["acc_y_r"], label="acc y")
            axs[1].plot(self.data_loadsol.downsampled_data["time"], self.data_loadsol.downsampled_data["acc_z_r"], label="acc z")
        elif self.data_state == "filtered":
            axs[1].plot(self.data_loadsol.filtered_data["time"], self.data_loadsol.filtered_data["acc_x_r"], label="acc x")
            axs[1].plot(self.data_loadsol.filtered_data["time"], self.data_loadsol.filtered_data["acc_y_r"], label="acc y")
            axs[1].plot(self.data_loadsol.filtered_data["time"], self.data_loadsol.filtered_data["acc_z_r"], label="acc z")

        axs[2].set_title("Gyrometer")
        if self.data_state == "pre_processed":
            axs[2].plot(self.data_loadsol.downsampled_data["time"], self.data_loadsol.downsampled_data["gyro_x_"], label="gyro x")
            axs[2].plot(self.data_loadsol.downsampled_data["time"], self.data_loadsol.downsampled_data["gyro_y_"], label="gyro y")
            axs[2].plot(self.data_loadsol.downsampled_data["time"], self.data_loadsol.downsampled_data["gyro_z_"], label="gyro z")
        elif self.data_state == "filtered":
            axs[2].plot(self.data_loadsol.filtered_data["time"], self.data_loadsol.filtered_data["gyro_x_"], label="gyro x")
            axs[2].plot(self.data_loadsol.filtered_data["time"], self.data_loadsol.filtered_data["gyro_y_"], label="gyro y")
            axs[2].plot(self.data_loadsol.filtered_data["time"], self.data_loadsol.filtered_data["gyro_z_"], label="gyro z")

        axs[0].set_xlabel("Time (s)")
        axs[0].set_ylabel("Force (N)")
        axs[1].set_xlabel("Time (s)")
        axs[1].set_ylabel("Acceleration (g)")
        axs[2].set_xlabel("Time (s)")
        axs[2].set_ylabel("Angular velocity (rad/s)")

        axs[0].legend()
        axs[1].legend()
        axs[2].legend()
        fig2.subplots_adjust(hspace=0.3)
        plt.show()

    def plot(self,time:np.ndarray, data:np.ndarray, data_type:str, legend:str):
        plt.plot(time,data,label=legend)
        plt.xlabel("Time (s)")
        if data_type == "force":
            plt.ylabel("Force (N)")
        elif data_type == "accelerometer":
            plt.ylabel("Acceleration (g)")
        elif data_type == "gyroscope":
            plt.ylabel("Angular velocity (rad/s)")
        plt.legend()



if __name__ == "__main__":
    curr_path = getcwd()
    working_directory = curr_path + "\\tests_09_02_24\\data\\txt\\"

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

        # Trial.compare_loadsol_forceplates()
        # Trial.compare_forces_imu()

        Trial.plot(time=Trial.data_loadsol_sync["time"],data=Trial.data_loadsol_sync["f_total_l"],data_type="force",legend="f total left")
        Trial.plot(time=Trial.data_forceplates_sync["time"],data=Trial.data_forceplates_sync["fy1"],data_type="force",legend="fy")
        plt.title("Comparison Fy and ftot (loadsol) for the left foot.")
        plt.show()

    #     # Initialise data (synchronised + downsampled signals)
    #     plt.plot(Trial.data_loadsol_sync["time"],Trial.data_loadsol_sync['f_total_l'],"-o",label="f total left")
    #     plt.plot(Trial.data_forceplates_sync["time"],Trial.data_forceplates_sync["fz1"],"-x",label="fz1")
    #     plt.xlabel("Time (s)")
    #     plt.ylabel("Force (N)")
    #     plt.legend()
    #     plt.title("Synchronised and resampled data (" + name + ")")
    #     plt.figure()
    # plt.show()

