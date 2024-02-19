from os import getcwd
from copy import deepcopy
from DataLoadsolNew import DataLoadsol
from DataForceplatesNew import DataForceplates
import matplotlib.pyplot as plt


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


if __name__ == "__main__":
    curr_path = getcwd()
    working_directory = curr_path + "\\tests_09_02_24\\data\\"
    file_name = "poussee_1_L"

    poussee_1_L_ls = DataLoadsol(
        path=working_directory + file_name + ".txt", frequency=200
    )

    poussee_1_L_fp = DataForceplates(
        path=working_directory + file_name + ".c3d", frequency=1000
    )

    Trial = TrialAnalysis(
        DataLoadSol=poussee_1_L_ls, DataForcePlates=poussee_1_L_fp, final_frequency=200, sync_index_loadsol=2345, sync_index_forceplates=int(12092/5)
    )

    # Initialise data (synchronised signals)
    plt.plot(Trial.data_loadsol_sync["time"],Trial.data_loadsol_sync['f_total_l'],"-o",label="f total left")
    plt.plot(Trial.data_forceplates_sync["time"],Trial.data_forceplates_sync["fz1"],"-x",label="fz1")
    plt.xlabel("Time (s)")
    plt.ylabel("Force (N)")
    plt.legend()
    plt.title("Synchronised  and resampled data")
    plt.show()


    # plt.plot(
    #     Trial.data_loadsol.downsampled_data["time"],
    #     Trial.data_loadsol.downsampled_data["f_total_l"],
    #     "-o",
    #     label="f total left",
    # )
    # plt.plot(
    #     Trial.data_forceplates.downsampled_data["time"],
    #     Trial.data_forceplates.downsampled_data["fz1"],
    #     "-x",
    #     label="fz1",
    # )
    # plt.legend()
    # plt.title(
    #     "Total force of the insole vs vertical force of the forceplate for the left foot"
    # )
    # plt.show()

    

    print("vh")
