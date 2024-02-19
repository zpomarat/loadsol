from os import getcwd
from copy import deepcopy
from DataLoadsolNew import DataLoadsol
from DataForceplatesNew import DataForceplates
import matplotlib.pyplot as plt

class TrialAnalysis:
    def __init__(
        self,
        DataLoadSol: DataLoadsol,
        DataForceplate: DataForceplates,
        final_frequency: int        
    ):
        self.data_loadsol = deepcopy(DataLoadSol)
        self.data_forceplate = deepcopy(DataForceplate)
        self.data_loadsol_sync = None
        self.data_forceplate_sync = None

        if DataLoadSol is not None:
            self.data_loadsol.downsample(final_frequency)
        if DataForceplates is not None:
            self.data_forceplate.downsample(final_frequency)



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
        DataLoadSol=poussee_1_L_ls,
        DataForceplate=poussee_1_L_fp,
        final_frequency = 200
    )

    # Initialise data
    plt.plot(Trial.data_loadsol.downsampled_data["time"], Trial.data_loadsol.downsampled_data["f_total_l"],'-o',label="f total left")
    plt.plot(Trial.data_forceplate.downsampled_data["time"], Trial.data_forceplate.downsampled_data["fz1"],'-x',label="fz1")
    plt.legend()
    plt.title("Total force of the insole vs vertical force of the forceplate for the left foot")
    plt.show()

