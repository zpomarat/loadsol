from os import getcwd
from copy import deepcopy
from DataLoadsolNew import DataLoadsol
from DataForceplatesNew import DataForceplates

class TrialAnalysis:
    def __init__(
        self,
        DataForceplate: DataForceplates,
        DataLoadSol: DataLoadsol
    ):
        self.DataLoadsol = deepcopy(DataLoadSol)
        self.DataForceplate = deepcopy(DataForceplate)
        self.DataLoadsol_sync = None
        self.DataForceplates_sync = None

        if DataLoadSol is not None:
            self.DataLoadsol.downsample(final_frequency=200)
        if DataForceplates is not None:
            self.DataForceplate.downsample(final_frequency=200)



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
        DataForceplate=poussee_1_L_fp
    )
