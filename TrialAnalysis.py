from os import getcwd, listdir
from Data import Data
from DataLoadsol import DataLoadsol
from DataForceplates import DataForceplates
from scipy import stats
import matplotlib.pyplot as plt
import pandas as pd


class TrialAnalysis:
    def __init__(
        self,
        DataForceplate: DataForceplates,
        DataLoadSol: DataLoadsol,
        sync_time_forceplate: int,
        sync_time_loadsol: int,
    ) -> None:
        self.DataForceplates = DataForceplate
        self.DataLoadsol = DataLoadSol
        self.sync_time_forceplate = sync_time_forceplate
        self.sync_time_loadsol = sync_time_loadsol
        filtering = False

        # Times
        if self.DataLoadsol is not None:
            self.time_ls = self.DataLoadsol.sync_signals(
                time=True, start_sync=self.sync_time_loadsol
            )
            self.time_ls -= self.time_ls[0]
        if self.DataForceplates is not None:
            self.time_fp = self.DataForceplates.sync_signals(
                time=True, start_sync=self.sync_time_forceplate
            )
            self.time_fp -= self.time_fp[0]

        # Loadsol
        if self.DataLoadsol is not None:
            # Left
            self.l_f_heel = self.DataLoadsol.sync_signals(
                dimension_1=True,insole_side="LEFT", data_type="F_HEEL", start_sync=self.sync_time_loadsol
            )
            self.l_f_medial = self.DataLoadsol.sync_signals(
                dimension_1=True,insole_side="LEFT", data_type="F_MEDIAL", start_sync=self.sync_time_loadsol
            )
            self.l_f_lateral = self.DataLoadsol.sync_signals(
                dimension_1=True,insole_side="LEFT", data_type="F_LATERAL", start_sync=self.sync_time_loadsol
            )
            self.l_f_total = self.DataLoadsol.sync_signals(
                dimension_1=True,insole_side="LEFT", data_type="F_TOTAL", start_sync=self.sync_time_loadsol
            )
            if filtering is True:
                self.l_accx = self.DataLoadsol.sync_signals(
                    column=0,insole_side="LEFT", data_type="ACC", start_sync=self.sync_time_loadsol
                )
                self.l_accy = self.DataLoadsol.sync_signals(
                    column=1,insole_side="LEFT", data_type="ACC", start_sync=self.sync_time_loadsol
                )
                self.l_accz = self.DataLoadsol.sync_signals(
                    column=2,insole_side="LEFT", data_type="ACC", start_sync=self.sync_time_loadsol
                )
                self.l_gyrox = self.DataLoadsol.sync_signals(
                    column=0,insole_side="LEFT", data_type="GYRO", start_sync=self.sync_time_loadsol
                )
                self.l_gyroy = self.DataLoadsol.sync_signals(
                    column=1,insole_side="LEFT", data_type="GYRO", start_sync=self.sync_time_loadsol
                )
                self.l_gyroz = self.DataLoadsol.sync_signals(
                    column=2,insole_side="LEFT", data_type="GYRO", start_sync=self.sync_time_loadsol
                )
            else:
                self.l_accx = self.DataLoadsol.sync_signals(
                    insole_side="LEFT", data_type="ACC", start_sync=self.sync_time_loadsol
                )[:,0]
                self.l_accy = self.DataLoadsol.sync_signals(
                    insole_side="LEFT", data_type="ACC", start_sync=self.sync_time_loadsol
                )[:,1]
                self.l_accz = self.DataLoadsol.sync_signals(
                    insole_side="LEFT", data_type="ACC", start_sync=self.sync_time_loadsol
                )[:,2]
                self.l_gyrox = self.DataLoadsol.sync_signals(
                    insole_side="LEFT", data_type="GYRO", start_sync=self.sync_time_loadsol
                )[:,0]
                self.l_gyroy = self.DataLoadsol.sync_signals(
                    insole_side="LEFT", data_type="GYRO", start_sync=self.sync_time_loadsol
                )[:,1]
                self.l_gyroz = self.DataLoadsol.sync_signals(
                    insole_side="LEFT", data_type="GYRO", start_sync=self.sync_time_loadsol
                )[:,2]

            # Right
            self.r_f_heel = self.DataLoadsol.sync_signals(
                dimension_1=True,insole_side="RIGHT", data_type="F_HEEL", start_sync=self.sync_time_loadsol
            )
            self.r_f_medial = self.DataLoadsol.sync_signals(
                dimension_1=True,insole_side="RIGHT", data_type="F_MEDIAL", start_sync=self.sync_time_loadsol
            )
            self.r_f_lateral = self.DataLoadsol.sync_signals(
                dimension_1=True,insole_side="RIGHT",
                data_type="F_LATERAL",
                start_sync=self.sync_time_loadsol,
            )
            self.r_f_total = self.DataLoadsol.sync_signals(
                dimension_1=True,insole_side="RIGHT", data_type="F_TOTAL", start_sync=self.sync_time_loadsol
            )
            if filtering is True:
                self.r_accx = self.DataLoadsol.sync_signals(
                    column=0,insole_side="RIGHT", data_type="ACC", start_sync=self.sync_time_loadsol
                )
                self.r_accy = self.DataLoadsol.sync_signals(
                    column=1,insole_side="RIGHT", data_type="ACC", start_sync=self.sync_time_loadsol
                )
                self.r_accz = self.DataLoadsol.sync_signals(
                    column=2,insole_side="RIGHT", data_type="ACC", start_sync=self.sync_time_loadsol
                )
                self.r_gyrox = self.DataLoadsol.sync_signals(
                    column=0,insole_side="RIGHT", data_type="GYRO", start_sync=self.sync_time_loadsol
                )
                self.r_gyroy = self.DataLoadsol.sync_signals(
                    column=1,insole_side="RIGHT", data_type="GYRO", start_sync=self.sync_time_loadsol
                )
                self.r_gyroz = self.DataLoadsol.sync_signals(
                    column=2,insole_side="RIGHT", data_type="GYRO", start_sync=self.sync_time_loadsol
                )
            else:
                self.r_accx = self.DataLoadsol.sync_signals(
                    insole_side="RIGHT", data_type="ACC", start_sync=self.sync_time_loadsol
                )[:,0]
                self.r_accy = self.DataLoadsol.sync_signals(
                    insole_side="RIGHT", data_type="ACC", start_sync=self.sync_time_loadsol
                )[:,1]
                self.r_accz = self.DataLoadsol.sync_signals(
                    insole_side="RIGHT", data_type="ACC", start_sync=self.sync_time_loadsol
                )[:,2]
                self.r_gyrox = self.DataLoadsol.sync_signals(
                    insole_side="RIGHT", data_type="GYRO", start_sync=self.sync_time_loadsol
                )[:,0]
                self.r_gyroy = self.DataLoadsol.sync_signals(
                    insole_side="RIGHT", data_type="GYRO", start_sync=self.sync_time_loadsol
                )[:,1]
                self.r_gyroz = self.DataLoadsol.sync_signals(
                    insole_side="RIGHT", data_type="GYRO", start_sync=self.sync_time_loadsol
                )[:,2]

        # Forceplates
        if filtering is True:
            if self.DataForceplates is not None:
                self.fp1_x = self.DataForceplates.sync_signals(
                    start_sync=self.sync_time_forceplate, forceplate_number=1, column=0
                )
                self.fp1_y = self.DataForceplates.sync_signals(
                    start_sync=self.sync_time_forceplate, forceplate_number=1, column=1
                )
                self.fp1_z = self.DataForceplates.sync_signals(
                    start_sync=self.sync_time_forceplate, forceplate_number=1, column=2
                )

                self.fp2_x = self.DataForceplates.sync_signals(
                    start_sync=self.sync_time_forceplate, forceplate_number=2, column=0
                )
                self.fp2_y = self.DataForceplates.sync_signals(
                    start_sync=self.sync_time_forceplate, forceplate_number=2, column=1
                )
                self.fp2_z = self.DataForceplates.sync_signals(
                    start_sync=self.sync_time_forceplate, forceplate_number=2, column=2
                )
        else:
            self.fp1_x = self.DataForceplates.sync_signals(
                start_sync=self.sync_time_forceplate, forceplate_number=1
            )[:,0]
            self.fp1_y = self.DataForceplates.sync_signals(
                start_sync=self.sync_time_forceplate, forceplate_number=1
            )[:,1]
            self.fp1_z = self.DataForceplates.sync_signals(
                start_sync=self.sync_time_forceplate, forceplate_number=1,
            )[:,2]

            self.fp2_x = self.DataForceplates.sync_signals(
                start_sync=self.sync_time_forceplate, forceplate_number=2,
            )[:,0]
            self.fp2_y = self.DataForceplates.sync_signals(
                start_sync=self.sync_time_forceplate, forceplate_number=2,
            )[:,1]
            self.fp2_z = self.DataForceplates.sync_signals(
                start_sync=self.sync_time_forceplate, forceplate_number=2,
            )[:,2]

        # Cut signals to the dimension of the smallest one
        min_len = min(len(self.l_f_heel),len(self.fp1_x))

        self.l_f_heel = self.l_f_heel[:min_len]
        self.l_f_medial = self.l_f_medial[:min_len]
        self.l_f_lateral = self.l_f_lateral[:min_len]
        self.l_f_total = self.l_f_total[:min_len]
        self.l_accx = self.l_accx[:min_len]
        self.l_accy = self.l_accy[:min_len]
        self.l_accz = self.l_accz[:min_len]
        self.l_gyrox = self.l_gyrox[:min_len]
        self.l_gyroy = self.l_gyroy[:min_len]
        self.l_gyroz = self.l_gyroz[:min_len]
        self.r_f_heel = self.r_f_heel[:min_len]
        self.r_f_medial = self.r_f_medial[:min_len]
        self.r_f_lateral = self.r_f_lateral[:min_len]
        self.r_f_total = self.r_f_total[:min_len]
        self.r_accx = self.r_accx[:min_len]
        self.r_accy = self.r_accy[:min_len]
        self.r_accz = self.r_accz[:min_len]
        self.r_gyrox = self.r_gyrox[:min_len]
        self.r_gyroy = self.r_gyroy[:min_len]
        self.r_gyroz = self.r_gyroz[:min_len]
        self.fp1_x = self.fp1_x[:min_len]
        self.fp1_y = self.fp1_y[:min_len]
        self.fp1_z = self.fp1_z[:min_len]
        self.fp2_x = self.fp2_x[:min_len]
        self.fp2_y = self.fp2_y[:min_len]
        self.fp2_z = self.fp2_z[:min_len]

        self.time_ls = self.time_ls[:min_len]
        self.time_fp = self.time_fp[:min_len]



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

    def test_sum(self, factor_heel, factor_medial, factor_lateral):
        # Left
        self.l_f_heel_factored = self.l_f_heel * factor_heel
        self.l_f_medial_factored = self.l_f_medial * factor_medial
        self.l_f_lateral_factored = self.l_f_lateral * factor_lateral
        self.l_f_total_factored = (
            self.l_f_heel_factored
            + self.l_f_medial_factored
            + self.l_f_lateral_factored
        )

        # Right
        self.r_f_heel_factored = self.r_f_heel * factor_heel
        self.r_f_medial_factored = self.r_f_medial * factor_medial
        self.r_f_lateral_factored = self.r_f_lateral * factor_lateral
        self.r_f_total_factored = (
            self.r_f_heel_factored
            + self.r_f_medial_factored
            + self.r_f_lateral_factored
        )

        fig1, axs = plt.subplots(2)
        fig1.suptitle("Comparison FP / LS with factors")
        axs[0].set_title("Left insole")
        axs[0].plot(
            self.time_ls, self.l_f_heel_factored, label=f"heel factor: {factor_heel}"
        )
        axs[0].plot(
            self.time_ls,
            self.l_f_medial_factored,
            label=f"medial factor: {factor_medial}",
        )
        axs[0].plot(
            self.time_ls,
            self.l_f_lateral_factored,
            label=f"lateral factor: {factor_lateral}",
        )
        axs[0].plot(self.time_ls, self.l_f_total_factored, label=f"total factor")
        axs[0].plot(self.time_fp, self.fp1_x, "-.", label="Fz")
        axs[0].plot(self.time_fp, self.fp1_y, "-.", label="Fz")
        axs[0].plot(self.time_fp, self.fp1_z, "-.", label="Fz")

        axs[1].set_title("Right insole")
        axs[1].plot(
            self.time_ls, self.r_f_heel_factored, label=f"heel factor: {factor_heel}"
        )
        axs[1].plot(
            self.time_ls,
            self.r_f_medial_factored,
            label=f"medial factor: {factor_medial}",
        )
        axs[1].plot(
            self.time_ls,
            self.r_f_lateral_factored,
            label=f"lateral factor: {factor_lateral}",
        )
        axs[1].plot(self.time_ls, self.r_f_total_factored, label=f"total factor")
        axs[1].plot(self.time_fp, self.fp2_x, "-.", label="Fz")
        axs[1].plot(self.time_fp, self.fp2_y, "-.", label="Fz")
        axs[1].plot(self.time_fp, self.fp2_z, "-.", label="Fz")

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
        axs[0].plot(self.time_ls, self.l_f_heel, label="heel")
        axs[0].plot(self.time_ls, self.l_f_medial, label="medial")
        axs[0].plot(self.time_ls, self.l_f_lateral, label="lateral")
        axs[0].plot(self.time_ls, self.l_f_total, label="total")

        axs[1].set_title("Accelerometer")
        axs[1].plot(self.time_ls, self.l_accx, label="acc x")
        axs[1].plot(self.time_ls, self.l_accy, label="acc y")
        axs[1].plot(self.time_ls, self.l_accz, label="acc z")

        axs[2].set_title("Gyrometer")
        axs[2].plot(self.time_ls, self.l_gyrox, label="gyro x")
        axs[2].plot(self.time_ls, self.l_gyroy, label="gyro y")
        axs[2].plot(self.time_ls, self.l_gyroz, label="gyro z")

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
        axs[0].plot(self.time_ls, self.r_f_heel, label="heel")
        axs[0].plot(self.time_ls, self.r_f_medial, label="medial")
        axs[0].plot(self.time_ls, self.r_f_lateral, label="lateral")
        axs[0].plot(self.time_ls, self.r_f_total, label="total")

        axs[1].set_title("Accelerometer")
        axs[1].plot(self.time_ls, self.r_accx, label="acc x")
        axs[1].plot(self.time_ls, self.r_accy, label="acc y")
        axs[1].plot(self.time_ls, self.r_accz, label="acc z")
        

        axs[2].set_title("Gyrometer")
        axs[2].plot(self.time_ls, self.r_gyrox, label="gyro x")
        axs[2].plot(self.time_ls, self.r_gyroy, label="gyro y")
        axs[2].plot(self.time_ls, self.r_gyroz, label="gyro z")

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


    def plot_ls_forces(self):
        plt.title("Left insole")
        plt.plot(self.time_ls, self.l_f_heel, label="heel")
        plt.plot(self.time_ls, self.l_f_medial, label="medial")
        plt.plot(self.time_ls, self.l_f_lateral, label="lateral")
        plt.plot(self.time_ls, self.l_f_total, label="total")
        plt.legend()
        plt.xlabel("Time (s)")
        plt.ylabel("Force (N)")
        plt.figure()

        plt.title("Right insole")
        plt.plot(self.time_ls, self.r_f_heel, label="heel")
        plt.plot(self.time_ls, self.r_f_medial, label="medial")
        plt.plot(self.time_ls, self.r_f_lateral, label="lateral")
        plt.plot(self.time_ls, self.r_f_total, label="total")

        plt.xlabel("Time (s)")
        plt.ylabel("Force (N)")

        plt.legend()
        plt.show()

    def correlation_ftot_acc(self,direction:str,start_trial:int,end_trial:int):
        match direction:
            case "x":
                corr_coef_l_ftot_accx = stats.pearsonr(self.l_f_total[start_trial:end_trial],self.l_accx[start_trial:end_trial])
                print(f"Pearson correlation coefficient between Ftot and Accx: {corr_coef_l_ftot_accx[0]}")
            case "y":
                corr_coef_l_ftot_accy = stats.pearsonr(self.l_f_total[start_trial:end_trial],self.l_accx[start_trial:end_trial])
                print(f"Pearson correlation coefficient between Ftot and Accy: {corr_coef_l_ftot_accy[0]}")
            case "z":
                corr_coef_l_ftot_accz = stats.pearsonr(self.l_f_total[start_trial:end_trial],self.l_accx[start_trial:end_trial])
                print(f"Pearson correlation coefficient between Ftot and Accz: {corr_coef_l_ftot_accz[0]}")

        
    def export_csv(self,export_directory,file_name):

        # Data to export
        data = {"Time": self.time_ls,
                "F_heel_left": self.l_f_heel,
                "F_medial_left": self.l_f_medial,
                "F_lateral_left": self.l_f_lateral,
                "F_total_left": self.l_f_total,
                "F_acc_x_left": self.l_accx,
                "F_acc_y_left": self.l_accy,
                "F_acc_z_left": self.l_accz,
                "F_gyro_x_left": self.l_gyrox,
                "F_gyro_y_left": self.l_gyroy,
                "F_gyro_z_left": self.l_gyroz,
                "F_heel_right": self.l_f_heel,
                "F_medial_right": self.r_f_medial,
                "F_lateral_right": self.r_f_lateral,
                "F_total_right": self.r_f_total,
                "F_acc_x_right": self.r_accx,
                "F_acc_y_right": self.r_accy,
                "F_acc_z_right": self.r_accz,
                "F_gyro_x_right": self.r_gyrox,
                "F_gyro_y_right": self.r_gyroy,
                "F_gyro_z_right": self.r_gyroz,
                "Fx_left": self.fp1_x,
                "Fy_left": self.fp1_y,
                "Fz_left": self.fp1_z,
                "Fx_right": self.fp2_x,
                "Fy_right": self.fp2_y,
                "Fz_right": self.fp2_z,
                }

        # Create a dataframe containing data to export
        df = pd.DataFrame(data)

        # Export data to a csv file
        df.to_csv(export_directory + file_name + "_processed.csv")

        


        




if __name__ == "__main__":
    curr_path = getcwd()
    working_directory = curr_path + "\\examples\\data\\"

    file_name = "test_poussee_1"
    poussee_1_ls = DataLoadsol(
        path=working_directory + file_name + ".txt", frequency=200
    )

    poussee_1_fp = DataForceplates(
        path=working_directory + file_name + ".c3d", frequency=1000
    )

    # Trial = TrialAnalysis(
    #     poids_fp,
    #     poids_ls,
    #     sync_time_loadsol=10,
    #     sync_time_forceplate=int(3847 / 5),
    # )

    # Trial = TrialAnalysis(
    #     pointe_1_fp,
    #     pointe_1_ls,
    #     sync_time_loadsol=3847,
    #     sync_time_forceplate=int(16743 / 5),
    # )

    # Trial = TrialAnalysis(
    #     pointe_3_fp,
    #     pointe_3_ls,
    #     sync_time_loadsol=3465,
    #     sync_time_forceplate=int(16825 / 5),
    # )

    # Trial = TrialAnalysis(
    #     pointe_5_fp,
    #     pointe_5_ls,
    #     sync_time_loadsol=3412,
    #     sync_time_forceplate=int(16598 / 5),
    # )

    Trial = TrialAnalysis(
        poussee_1_fp,
        poussee_1_ls,
        sync_time_loadsol=3009,
        sync_time_forceplate=int(13718 / 5),
    )

    # Trial = TrialAnalysis(
    #     poussee_2_fp,
    #     poussee_2_ls,
    #     sync_time_loadsol=3165,
    #     sync_time_forceplate=int(15384 / 5),
    # )

    # Trial = TrialAnalysis(
    #     poussee_3_fp,
    #     poussee_3_ls,
    #     sync_time_loadsol=3644,
    #     sync_time_forceplate=int(17745 / 5),
    # )

    # Trial2 = TrialAnalysis(
    #     poussee_3_fp,
    #     poussee_3_ls,
    #     sync_time_loadsol=3684,
    #     sync_time_forceplate=int(17785 / 5),
    # )

    # Trial = TrialAnalysis(
    #     DataForceplate=None,
    #     DataLoadSol=pointe_3_05_02_ls,
    #     sync_time_loadsol=0,
    #     sync_time_forceplate=0,
    # )

    # Trial.compare_loadsol_forceplates()
    # Trial.plot_ls_forces()
    # Trial.test_sum(1,2/3,2/3)
    # Trial.compare_forces_imu()
    # Trial2.compare_forces_imu()
    # Trial.correlation_ftot_acc(direction="x",start_trial=756,end_trial=1040)
    # Trial.correlation_ftot_acc(direction="y",start_trial=756,end_trial=1040)
    # Trial.correlation_ftot_acc(direction="z",start_trial=756,end_trial=1040)

    Trial.export_csv(curr_path + "\\examples\\results\\",file_name)
 
