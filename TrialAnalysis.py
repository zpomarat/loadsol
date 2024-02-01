from os import getcwd, listdir
from Data import Data
from DataLoadsol import DataLoadsol
from DataForceplates import DataForceplates
import matplotlib.pyplot as plt


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

        # Times
        self.time_ls = self.DataLoadsol.sync_signals(
            time=True, start_sync=self.sync_time_loadsol
        )
        self.time_ls -= self.time_ls[0]

        self.time_fp = self.DataForceplates.sync_signals(
            time=True, start_sync=self.sync_time_forceplate
        )
        self.time_fp -= self.time_fp[0]

        # Loadsol
        # Left
        self.l_f_heel = self.DataLoadsol.sync_signals(
            insole_side="LEFT", data_type="F_HEEL", start_sync=self.sync_time_loadsol
        )
        self.l_f_medial = self.DataLoadsol.sync_signals(
            insole_side="LEFT", data_type="F_MEDIAL", start_sync=self.sync_time_loadsol
        )
        self.l_f_lateral = self.DataLoadsol.sync_signals(
            insole_side="LEFT", data_type="F_LATERAL", start_sync=self.sync_time_loadsol
        )
        self.l_f_total = self.DataLoadsol.sync_signals(
            insole_side="LEFT", data_type="F_TOTAL", start_sync=self.sync_time_loadsol
        )

        # Right
        self.r_f_heel = self.DataLoadsol.sync_signals(
            insole_side="RIGHT", data_type="F_HEEL", start_sync=self.sync_time_loadsol
        )
        self.r_f_medial = self.DataLoadsol.sync_signals(
            insole_side="RIGHT", data_type="F_MEDIAL", start_sync=self.sync_time_loadsol
        )
        self.r_f_lateral = self.DataLoadsol.sync_signals(
            insole_side="RIGHT",
            data_type="F_LATERAL",
            start_sync=self.sync_time_loadsol,
        )
        self.r_f_total = self.DataLoadsol.sync_signals(
            insole_side="RIGHT", data_type="F_TOTAL", start_sync=self.sync_time_loadsol
        )

        # Forceplates
        self.fp1_z = self.DataForceplates.sync_signals(
            start_sync=self.sync_time_forceplate, forceplate_number=1, column=2
        )
        self.fp2_z = self.DataForceplates.sync_signals(
            start_sync=self.sync_time_forceplate, forceplate_number=2, column=2
        )

    def compare_loadsol_forceplates(self):
        fig1, axs = plt.subplots(2)
        fig1.suptitle("Comparison FP / LS")
        axs[0].set_title("Left insole")
        axs[0].plot(self.time_ls, self.l_f_heel, label="heel")
        axs[0].plot(self.time_ls, self.l_f_medial, label="medial")
        axs[0].plot(self.time_ls, self.l_f_lateral, label="lateral")
        axs[0].plot(self.time_ls, self.l_f_total, label="total")
        axs[0].plot(self.time_fp, self.fp1_z, label="Fz")

        axs[1].set_title("Right insole")
        axs[1].plot(self.time_ls, self.r_f_heel, label="heel")
        axs[1].plot(self.time_ls, self.r_f_medial, label="medial")
        axs[1].plot(self.time_ls, self.r_f_lateral, label="lateral")
        axs[1].plot(self.time_ls, self.r_f_total, label="total")
        axs[1].plot(self.time_fp, self.fp2_z, label="Fz")

        axs[0].set_xlabel("Time (s)")
        axs[0].set_ylabel("Force (N)")
        axs[1].set_xlabel("Time (s)")
        axs[1].set_ylabel("Force (N)")

        axs[0].legend()
        axs[1].legend()
        fig1.subplots_adjust(hspace=0.3)
        plt.show()

    def test_sum(self, factor_heel, factor_medial, factor_lateral):
        self.l_f_heel_factored = self.l_f_heel * factor_heel
        self.l_f_medial_factored = self.l_f_medial * factor_medial
        self.l_f_lateral_factored = self.l_f_lateral * factor_lateral

        # Right
        self.r_f_heel_factored = self.r_f_heel * factor_heel
        self.r_f_medial_factored = self.r_f_medial * factor_medial
        self.r_f_lateral_factored = self.r_f_lateral * factor_lateral

        fig1, axs = plt.subplots(2)
        fig1.suptitle("Comparison FP / LS with factors")
        axs[0].set_title("Left insole")
        axs[0].plot(self.time_ls, self.l_f_heel_factored, label=f"heel factor: {factor_heel}")
        axs[0].plot(self.time_ls, self.l_f_medial_factored, label=f"medial factor: {factor_medial}")
        axs[0].plot(self.time_ls, self.l_f_lateral_factored, label=f"lateral factor: {factor_lateral}")
        axs[0].plot(self.time_fp, self.fp1_z, label="Fz")

        axs[1].set_title("Right insole")
        axs[1].plot(self.time_ls, self.r_f_heel_factored, label=f"heel factor: {factor_heel}")
        axs[1].plot(self.time_ls, self.r_f_medial_factored, label=f"medial factor: {factor_medial}")
        axs[1].plot(self.time_ls, self.r_f_lateral_factored, label=f"lateral factor: {factor_lateral}")
        axs[1].plot(self.time_fp, self.fp2_z, label="Fz")

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
    working_directory = curr_path + "\\examples\\data\\"

    file_name = "test_poussee_3"
    pointe_1_ls = DataLoadsol(
        path=working_directory + file_name + ".txt", frequency=200
    )
    pointe_1_fp = DataForceplates(
        path=working_directory + file_name + ".c3d", frequency=1000
    )

    Trial = TrialAnalysis(
        pointe_1_fp,
        pointe_1_ls,
        sync_time_loadsol=3644,
        sync_time_forceplate=int(17745 / 5),
    )

    Trial.test_sum(1,2/3,2/3)
