import csv
import numpy as np
from os import getcwd
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import interp1d
from copy import deepcopy


class DataLoadsol:
    def __init__(self, path: str, frequency: int):
        self.path = path
        self.path_csv = self.path[:-3] + "csv"
        self.file_name = (self.path.split("\\"))[-1].split(".")[0]
        self.frequency = frequency
        self.raw_data = None
        self.timestamp = None
        self.cleaned_data = None
        self.filled_data = None
        self.resampled_data = None
        self.filtered_data = None

    def convert_txt_to_csv(self, output_directory: str):
        """Converts a txt file to a csv file and change the attribute "path" to the DataLoadsol class by the path of csv file.

        Args:
            output_directory: str
                Path of the directory contaning the converted file.
        """

        # Delimiter used in the input file
        input_delimiter = "\t"

        # Delimiter used in the output file
        output_delimiter = ","

        # Open the input file in read mode
        with open(self.path, "r", newline="", encoding="utf-8") as infile:
            # Create a CSV reader object for the input file
            reader = csv.reader(infile, delimiter=input_delimiter)

            # Read the data from the input file
            data = list(reader)

        # Open the output file in write mode
        output_filename = self.file_name + ".csv"
        with open(
            output_directory + output_filename, "w", newline="", encoding="utf-8"
        ) as outfile:
            # Create a CSV writer object for the output file
            writer = csv.writer(outfile, delimiter=output_delimiter)

            # Write the data to the CSV file
            writer.writerows(data)

    def csv_reader_loadsol(self):
        """Reads csv file containing raw insoles data. Creates a dictionnary containing the raw time and the raw data of each insole.

        Returns:
            self.raw_data: dict[str, np.ndarray]
                Contains raw time and raw data of both insoles of a pair.

            keys: time_left, f_heel_l, f_medial_l, f_lateral_l, f_tot_l, acc_x_l, acc_y_l, acc_z_l, gyro_x_l, gyro_y_l, gyro_z_l,
                  time_right, f_heel_r, f_medial_r, f_lateral_r, f_tot_r, acc_x_r, acc_y_r, acc_z_r, gyro_x_r, gyro_y_r, gyro_z_r.
        """

        ## Read csv file line by line after going to the directory containing the file to handle
        lines = open(self.path_csv, "r").readlines()

        ## Extract timestamp
        # Line containing the timestamp
        line = lines[0]

        # Extract the timestamp as a str
        str_timestamp = line[-33:-10]

        # Specify the format of the timestamp (Year_Month_Day_Hour_Minute_Second_Microsecond)
        format = "%Y_%m_%d_%H_%M_%S_%f"

        # Define the timestamp
        self.timestamp = datetime.strptime(str_timestamp, format)

        ## Select data
        # Start reading the file at line k to skip the header
        k = 4

        # Number of lines of the data file to extract
        rows = len(lines) - k - 1

        # Create an array of the right size
        raw_data = np.zeros((rows, 24))

        # Fill the array with data
        for i in range(rows):
            if ",-," in lines[k + i]:
                lines[k + i] = lines[k + i].replace("-,", "nan,")
            data_line = np.fromstring(lines[k + i][:-3], sep=",")

            # Number of columns of the data file
            columns = len(data_line)

            # Print error message if the number of columns is not equal to 24
            if columns != 24:
                raise ValueError(
                    "Data missing, the file '" + self.file_name + "' is not processed."
                )
                break
            raw_data[i, :] = data_line

        ## Fill the dictionnary with raw data
        self.raw_data = {
            "time_l": raw_data[:, 0],
            "f_heel_l": raw_data[:, 1],
            "f_medial_l": raw_data[:, 2],
            "f_lateral_l": raw_data[:, 3],
            "f_total_l": raw_data[:, 4],
            "acc_x_l": raw_data[:, 6],
            "acc_y_l": raw_data[:, 7],
            "acc_z_l": raw_data[:, 8],
            "gyro_x_l": raw_data[:, 9],
            "gyro_y_l": raw_data[:, 10],
            "gyro_z_l": raw_data[:, 11],
            "time_r": raw_data[:, 12],
            "f_heel_r": raw_data[:, 15],
            "f_medial_r": raw_data[:, 14],
            "f_lateral_r": raw_data[:, 13],
            "f_total_r": raw_data[:, 16],
            "acc_x_r": raw_data[:, 18],
            "acc_y_r": raw_data[:, 19],
            "acc_z_r": raw_data[:, 20],
            "gyro_x_r": raw_data[:, 21],
            "gyro_y_r": raw_data[:, 22],
            "gyro_z_r": raw_data[:, 23],
        }

    def clean_data(self):
        """Replaces the incorrect values in force data by NaN (incorrect value = negative value of force per zone).
            Finds and suppresses duplicate data.
        """

        if self.raw_data is None:
            self.csv_reader_loadsol()
            
        ## Suppress incorrect values 
        # Initialise data with incorrect values suppressed
        f_heel_l_incorrect_values_sup = self.raw_data["f_heel_l"]
        f_medial_l_incorrect_values_sup = self.raw_data["f_medial_l"]
        f_lateral_l_incorrect_values_sup = self.raw_data["f_lateral_l"]
        f_total_l_incorrect_values_sup = self.raw_data["f_total_l"]

        f_heel_r_incorrect_values_sup = self.raw_data["f_heel_r"]
        f_medial_r_incorrect_values_sup = self.raw_data["f_medial_r"]
        f_lateral_r_incorrect_values_sup = self.raw_data["f_lateral_r"]
        f_total_r_incorrect_values_sup = self.raw_data["f_total_r"]        

        # Find indexes of incorrect values
        index_incorrect_values_left = [
            index for index, item in enumerate(self.raw_data["f_heel_l"]) if item < 0
        ]
        index_incorrect_values_right = [
            index for index, item in enumerate(self.raw_data["f_heel_r"]) if item < 0
        ]

        # Replace incorrect values by NaN
        for i in index_incorrect_values_left:
            f_heel_l_incorrect_values_sup[i] = np.NaN
            f_medial_l_incorrect_values_sup[i] = np.NaN
            f_lateral_l_incorrect_values_sup[i] = np.NaN
            f_total_l_incorrect_values_sup[i] = np.NaN

        for i in index_incorrect_values_right:
            f_heel_r_incorrect_values_sup[i] = np.NaN
            f_medial_r_incorrect_values_sup[i] = np.NaN
            f_lateral_r_incorrect_values_sup[i] = np.NaN
            f_total_r_incorrect_values_sup[i] = np.NaN

        ## Suppress duplicate data
        # Initialise data with duplicate values suppressed
        time_l_unique = self.raw_data["time_l"]
        time_r_unique = self.raw_data["time_r"]

        f_heel_l_unique = f_heel_l_incorrect_values_sup
        f_medial_l_unique = f_medial_l_incorrect_values_sup
        f_lateral_l_unique = f_lateral_l_incorrect_values_sup
        f_total_l_unique = f_total_l_incorrect_values_sup
        acc_x_l_unique = self.raw_data["acc_x_l"]
        acc_y_l_unique = self.raw_data["acc_y_l"]
        acc_z_l_unique = self.raw_data["acc_z_l"]
        gyro_x_l_unique = self.raw_data["gyro_x_l"]
        gyro_y_l_unique = self.raw_data["gyro_y_l"]
        gyro_z_l_unique = self.raw_data["gyro_z_l"]

        f_heel_r_unique = f_heel_r_incorrect_values_sup
        f_medial_r_unique = f_medial_r_incorrect_values_sup
        f_lateral_r_unique = f_lateral_r_incorrect_values_sup
        f_total_r_unique = f_total_r_incorrect_values_sup
        acc_x_r_unique = self.raw_data["acc_x_r"]
        acc_y_r_unique = self.raw_data["acc_y_r"]
        acc_z_r_unique = self.raw_data["acc_z_r"]
        gyro_x_r_unique = self.raw_data["gyro_x_r"]
        gyro_y_r_unique = self.raw_data["gyro_y_r"]
        gyro_z_r_unique = self.raw_data["gyro_z_r"]

        # Find indexes of duplicate values
        index_duplicate_left = [
            index
            for index, item in enumerate(self.raw_data["time_l"])
            if item in self.raw_data["time_l"][:index]
        ]

        index_duplicate_right = [
            index
            for index, item in enumerate(self.raw_data["time_r"])
            if item in self.raw_data["time_r"][:index]
        ]

        # Replace by nan values the line before the line corresponding to the index identified for the left side
        for i in index_duplicate_left:
            time_l_unique[i - 1] = np.NaN
            f_heel_l_unique[i - 1] = np.NaN
            f_medial_l_unique[i - 1] = np.NaN
            f_lateral_l_unique[i - 1] = np.NaN
            f_total_l_unique[i - 1] = np.NaN
            acc_x_l_unique[i - 1] = np.NaN
            acc_y_l_unique[i - 1] = np.NaN
            acc_z_l_unique[i - 1] = np.NaN
            gyro_x_l_unique[i - 1] = np.NaN
            gyro_y_l_unique[i - 1] = np.NaN
            gyro_z_l_unique[i - 1] = np.NaN

            # Complete time nan values
            time_l_unique[i - 1] = (i - 1) / self.frequency

        # Replace by nan values the line before the line corresponding to the index identified for the right side
        for i in index_duplicate_right:
            time_r_unique[i - 1] = np.NaN
            f_heel_r_unique[i - 1] = np.NaN
            f_medial_r_unique[i - 1] = np.NaN
            f_lateral_r_unique[i - 1] = np.NaN
            f_total_r_unique[i - 1] = np.NaN
            acc_x_r_unique[i - 1] = np.NaN
            acc_y_r_unique[i - 1] = np.NaN
            acc_z_r_unique[i - 1] = np.NaN
            gyro_x_r_unique[i - 1] = np.NaN
            gyro_y_r_unique[i - 1] = np.NaN
            gyro_z_r_unique[i - 1] = np.NaN

            # Complete time nan values
            time_r_unique[i - 1] = (i - 1) / self.frequency

        # Fill the cleaned_data dictionnary
        self.cleaned_data = {
            "time_l": time_l_unique,
            "f_heel_l": f_heel_l_unique,
            "f_medial_l": f_medial_l_unique,
            "f_lateral_l": f_lateral_l_unique,
            "f_total_l": f_total_l_unique,
            "acc_x_l": acc_x_l_unique,
            "acc_y_l": acc_y_l_unique,
            "acc_z_l": acc_z_l_unique,
            "gyro_x_l": gyro_x_l_unique,
            "gyro_y_l": gyro_y_l_unique,
            "gyro_z_l": gyro_z_l_unique,
            "time_r": time_r_unique,
            "f_heel_r": f_heel_r_unique,
            "f_medial_r": f_medial_r_unique,
            "f_lateral_r": f_lateral_r_unique,
            "f_total_r": f_total_r_unique,
            "acc_x_r": acc_x_r_unique,
            "acc_y_r": acc_y_r_unique,
            "acc_z_r": acc_z_r_unique,
            "gyro_x_r": gyro_x_r_unique,
            "gyro_y_r": gyro_y_r_unique,
            "gyro_z_r": gyro_z_r_unique
        }

    def fill_missing_data(self):
        """Interpolates missing data."""

        if self.cleaned_data is None:
            self.clean_data()

        # Initialise filled data
        f_heel_l_filled = self.cleaned_data["f_heel_l"]
        f_medial_l_filled = self.cleaned_data["f_medial_l"]
        f_lateral_l_filled = self.cleaned_data["f_lateral_l"]
        f_total_l_filled = self.cleaned_data["f_total_l"]
        acc_x_l_filled = self.cleaned_data["acc_x_l"]
        acc_y_l_filled = self.cleaned_data["acc_y_l"]
        acc_z_l_filled = self.cleaned_data["acc_z_l"]
        gyro_x_l_filled = self.cleaned_data["gyro_x_l"]
        gyro_y_l_filled = self.cleaned_data["gyro_y_l"]
        gyro_z_l_filled = self.cleaned_data["gyro_z_l"]

        f_heel_r_filled = self.cleaned_data["f_heel_r"]
        f_medial_r_filled = self.cleaned_data["f_medial_r"]
        f_lateral_r_filled = self.cleaned_data["f_lateral_r"]
        f_total_r_filled = self.cleaned_data["f_total_r"]
        acc_x_r_filled = self.cleaned_data["acc_x_r"]
        acc_y_r_filled = self.cleaned_data["acc_y_r"]
        acc_z_r_filled = self.cleaned_data["acc_z_r"]
        gyro_x_r_filled = self.cleaned_data["gyro_x_r"]
        gyro_y_r_filled = self.cleaned_data["gyro_y_r"]
        gyro_z_r_filled = self.cleaned_data["gyro_z_r"]

        time_filled = self.cleaned_data["time_l"]

        # Check if there are nan values at the end of the data array
        max_nan_to_delete = 0
        for data_array in [
            f_heel_l_filled,
            f_medial_l_filled,
            f_lateral_l_filled,
            f_total_l_filled,
            acc_x_l_filled,
            acc_y_l_filled,
            acc_z_l_filled,
            gyro_x_l_filled,
            gyro_y_l_filled,
            gyro_z_l_filled,
            f_heel_r_filled,
            f_medial_r_filled,
            f_lateral_r_filled,
            f_total_r_filled,
            acc_x_r_filled,
            acc_y_r_filled,
            acc_z_r_filled,
            gyro_x_r_filled,
            gyro_y_r_filled,
            gyro_z_r_filled
        ]:
            for itr in range(1, len(data_array)):
                if type(data_array[0]) == np.float_:
                    if np.isnan(data_array[-itr])==False:
                        break
                    else:
                        max_nan_to_delete = max(max_nan_to_delete, itr)
                else:
                    if False in np.isnan(data_array[-itr]):
                        break
                    else:
                        max_nan_to_delete = max(max_nan_to_delete, itr)

        # Truncate nan values if there are nan values at the end of the data array
        if max_nan_to_delete>0:
            f_heel_l_filled = f_heel_l_filled[:-max_nan_to_delete]
            f_medial_l_filled = f_medial_l_filled[:-max_nan_to_delete]
            f_lateral_l_filled = f_lateral_l_filled[:-max_nan_to_delete]
            f_total_l_filled = f_total_l_filled[:-max_nan_to_delete]
            acc_x_l_filled = acc_x_l_filled[:-max_nan_to_delete]
            acc_y_l_filled = acc_y_l_filled[:-max_nan_to_delete]
            acc_z_l_filled = acc_z_l_filled[:-max_nan_to_delete]
            gyro_x_l_filled = gyro_x_l_filled[:-max_nan_to_delete]
            gyro_y_l_filled = gyro_y_l_filled[:-max_nan_to_delete]
            gyro_z_l_filled = gyro_z_l_filled[:-max_nan_to_delete]

            f_heel_r_filled = f_heel_r_filled[:-max_nan_to_delete]
            f_medial_r_filled = f_medial_r_filled[:-max_nan_to_delete]
            f_lateral_r_filled = f_lateral_r_filled[:-max_nan_to_delete]
            f_total_r_filled = f_total_r_filled[:-max_nan_to_delete]
            acc_x_r_filled = acc_x_r_filled[:-max_nan_to_delete]
            acc_y_r_filled = acc_y_r_filled[:-max_nan_to_delete]
            acc_z_r_filled = acc_z_r_filled[:-max_nan_to_delete]
            gyro_x_r_filled = gyro_x_r_filled[:-max_nan_to_delete]
            gyro_y_r_filled = gyro_y_r_filled[:-max_nan_to_delete]
            gyro_z_r_filled = gyro_z_r_filled[:-max_nan_to_delete]

            time_filled = time_filled[:-max_nan_to_delete]

        # Convert the data to fill into dataframe
        data_f_heel_l = pd.DataFrame(f_heel_l_filled)
        data_f_medial_l = pd.DataFrame(f_medial_l_filled)
        data_f_lateral_l = pd.DataFrame(f_lateral_l_filled)
        data_f_total_l = pd.DataFrame(f_total_l_filled)
        data_acc_x_l = pd.DataFrame(acc_x_l_filled)
        data_acc_y_l = pd.DataFrame(acc_y_l_filled)
        data_acc_z_l = pd.DataFrame(acc_z_l_filled)
        data_gyro_x_l = pd.DataFrame(gyro_x_l_filled)
        data_gyro_y_l = pd.DataFrame(gyro_y_l_filled)
        data_gyro_z_l = pd.DataFrame(gyro_z_l_filled)

        data_f_heel_r = pd.DataFrame(f_heel_r_filled)
        data_f_medial_r = pd.DataFrame(f_medial_r_filled)
        data_f_lateral_r = pd.DataFrame(f_lateral_r_filled)
        data_f_total_r = pd.DataFrame(f_total_r_filled)
        data_acc_x_r = pd.DataFrame(acc_x_r_filled)
        data_acc_y_r = pd.DataFrame(acc_y_r_filled)
        data_acc_z_r = pd.DataFrame(acc_z_r_filled)
        data_gyro_x_r = pd.DataFrame(gyro_x_r_filled)
        data_gyro_y_r = pd.DataFrame(gyro_y_r_filled)
        data_gyro_z_r = pd.DataFrame(gyro_z_r_filled)

        # Interpolate with the cubic method
        data_f_heel_l_filled = data_f_heel_l.interpolate("cubic")
        data_f_medial_l_filled = data_f_medial_l.interpolate("cubic")
        data_f_lateral_l_filled = data_f_lateral_l.interpolate("cubic")
        data_f_total_l_filled = data_f_total_l.interpolate("cubic")
        data_acc_x_l_filled = data_acc_x_l.interpolate("cubic")
        data_acc_y_l_filled = data_acc_y_l.interpolate("cubic")
        data_acc_z_l_filled = data_acc_z_l.interpolate("cubic")
        data_gyro_x_l_filled = data_gyro_x_l.interpolate("cubic")
        data_gyro_y_l_filled = data_gyro_y_l.interpolate("cubic")
        data_gyro_z_l_filled = data_gyro_z_l.interpolate("cubic")

        data_f_heel_r_filled = data_f_heel_r.interpolate("cubic")
        data_f_medial_r_filled = data_f_medial_r.interpolate("cubic")
        data_f_lateral_r_filled = data_f_lateral_r.interpolate("cubic")
        data_f_total_r_filled = data_f_total_r.interpolate("cubic")
        data_acc_x_r_filled = data_acc_x_r.interpolate("cubic")
        data_acc_y_r_filled = data_acc_y_r.interpolate("cubic")
        data_acc_z_r_filled = data_acc_z_r.interpolate("cubic")
        data_gyro_x_r_filled = data_gyro_x_r.interpolate("cubic")
        data_gyro_y_r_filled = data_gyro_y_r.interpolate("cubic")
        data_gyro_z_r_filled = data_gyro_z_r.interpolate("cubic")

        # Convert the data interpolated into ndarray
        data_f_heel_l_filled = np.reshape(
            data_f_heel_l_filled.to_numpy(), (len(data_f_heel_l_filled),)
        )
        data_f_medial_l_filled = np.reshape(
            data_f_medial_l_filled.to_numpy(), (len(data_f_medial_l_filled),)
        )
        data_f_lateral_l_filled = np.reshape(
            data_f_lateral_l_filled.to_numpy(), (len(data_f_lateral_l_filled),)
        )
        data_f_total_l_filled = np.reshape(
            data_f_total_l_filled.to_numpy(), (len(data_f_total_l_filled),)
        )
        data_acc_x_l_filled = np.reshape(
            data_acc_x_l_filled.to_numpy(), (len(data_acc_x_l_filled),)
        )
        data_acc_y_l_filled = np.reshape(
            data_acc_y_l_filled.to_numpy(), (len(data_acc_y_l_filled),)
        )
        data_acc_z_l_filled = np.reshape(
            data_acc_z_l_filled.to_numpy(), (len(data_acc_z_l_filled),)
        )
        data_gyro_x_l_filled = np.reshape(
            data_gyro_x_l_filled.to_numpy(), (len(data_gyro_x_l_filled),)
        )
        data_gyro_y_l_filled = np.reshape(
            data_gyro_y_l_filled.to_numpy(), (len(data_gyro_y_l_filled),)
        )
        data_gyro_z_l_filled = np.reshape(
            data_gyro_z_l_filled.to_numpy(), (len(data_gyro_z_l_filled),)
        )

        data_f_heel_r_filled = np.reshape(
            data_f_heel_r_filled.to_numpy(), (len(data_f_heel_r_filled),)
        )
        data_f_medial_r_filled = np.reshape(
            data_f_medial_r_filled.to_numpy(), (len(data_f_medial_r_filled),)
        )
        data_f_lateral_r_filled = np.reshape(
            data_f_lateral_r_filled.to_numpy(), (len(data_f_lateral_r_filled),)
        )
        data_f_total_r_filled = np.reshape(
            data_f_total_r_filled.to_numpy(), (len(data_f_total_r_filled),)
        )
        data_acc_x_r_filled = np.reshape(
            data_acc_x_r_filled.to_numpy(), (len(data_acc_x_r_filled),)
        )
        data_acc_y_r_filled = np.reshape(
            data_acc_y_r_filled.to_numpy(), (len(data_acc_y_r_filled),)
        )
        data_acc_z_r_filled = np.reshape(
            data_acc_z_r_filled.to_numpy(), (len(data_acc_z_r_filled),)
        )
        data_gyro_x_r_filled = np.reshape(
            data_gyro_x_r_filled.to_numpy(), (len(data_gyro_x_r_filled),)
        )
        data_gyro_y_r_filled = np.reshape(
            data_gyro_y_r_filled.to_numpy(), (len(data_gyro_y_r_filled),)
        )
        data_gyro_z_r_filled = np.reshape(
            data_gyro_z_r_filled.to_numpy(), (len(data_gyro_z_r_filled),)
        )

        # Fill the filled_data dictionnary
        self.filled_data = {
                    "time": time_filled,
                    "f_heel_l": data_f_heel_l_filled,
                    "f_medial_l": data_f_medial_l_filled,
                    "f_lateral_l": data_f_lateral_l_filled,
                    "f_total_l": data_f_total_l_filled,
                    "acc_x_l": data_acc_x_l_filled,
                    "acc_y_l": data_acc_y_l_filled,
                    "acc_z_l": data_acc_z_l_filled,
                    "gyro_x_l": data_gyro_x_l_filled,
                    "gyro_y_l": data_gyro_y_l_filled,
                    "gyro_z_l": data_gyro_z_l_filled,
                    "f_heel_r": data_f_heel_l_filled,
                    "f_medial_r": data_f_medial_l_filled,
                    "f_lateral_r": data_f_lateral_l_filled,
                    "f_total_r": data_f_total_l_filled,
                    "acc_x_r": data_acc_x_l_filled,
                    "acc_y_r": data_acc_y_l_filled,
                    "acc_z_r": data_acc_z_l_filled,
                    "gyro_x_r": data_gyro_x_l_filled,
                    "gyro_y_r": data_gyro_y_l_filled,
                    "gyro_z_r": data_gyro_z_l_filled
                }

    def downsample(self,final_frequency:int):
        """Downsamples data to the final frequency.

        Args:
            final_frequency (int): downsampled frequency 
        """

        if self.filled_data is None:
            self.fill_missing_data()

        # Initialise downsampled data
        self.downsampled_data = deepcopy(self.filled_data)

        # Create new time vector based on the final frequency
        t_ds = np.arange(self.filled_data["time"][0],self.filled_data["time"][-1],1/final_frequency)

        for key in self.downsampled_data.keys():

            # Create interpolation function
            f = interp1d(self.filled_data["time"],self.filled_data.get(key))

            # Downsample data
            self.downsampled_data[key] = f(t_ds)

        # Add new time vector downsampled
        self.downsampled_data["time"] = t_ds

    




if __name__ == "__main__":
    curr_path = getcwd()

    # Create object
    test = DataLoadsol(
        path=curr_path + "\\examples\\data\\test_pointe_1.txt", frequency=200
    )

    # Convert txt to csv
    test.convert_txt_to_csv(curr_path + "\\examples\\data\\")

    # Raw data
    test.csv_reader_loadsol()
    print(f"Raw time left: {test.raw_data["time_l"]}")
    print(f"Raw left heel force data: {test.raw_data["f_heel_l"]}")
    plt.plot(test.raw_data["time_l"],test.raw_data["f_heel_l"],label="heel")
    plt.plot(test.raw_data["time_l"],test.raw_data["f_medial_l"],label="medial")
    plt.plot(test.raw_data["time_l"],test.raw_data["f_lateral_l"],label="lateral")
    plt.plot(test.raw_data["time_l"],test.raw_data["f_total_l"],label="total")
    plt.legend()
    plt.title("Raw force data of the left insole")
    plt.figure()

    # Clean data: suppres incorrect values and duplicate data
    test.clean_data()
    plt.plot(test.cleaned_data["time_l"],test.cleaned_data["f_heel_l"],label="heel")
    plt.plot(test.cleaned_data["time_l"],test.cleaned_data["f_medial_l"],label="medial")
    plt.plot(test.cleaned_data["time_l"],test.cleaned_data["f_lateral_l"],label="lateral")
    plt.plot(test.cleaned_data["time_l"],test.cleaned_data["f_total_l"],label="total")
    plt.legend()
    plt.title("Cleaned force data of the left insole")
    plt.figure()

    # Fill missing data
    test.fill_missing_data()
    plt.plot(test.filled_data["time"],test.filled_data["f_heel_l"],label="heel")
    plt.plot(test.filled_data["time"],test.filled_data["f_medial_l"],label="medial")
    plt.plot(test.filled_data["time"],test.filled_data["f_lateral_l"],label="lateral")
    plt.plot(test.filled_data["time"],test.filled_data["f_total_l"],label="total")
    plt.legend()
    plt.title("Filled force data of the left insole")
    plt.figure()

    # Downsample data
    test.downsample(final_frequency=33)
    plt.plot(test.filled_data["time"],test.filled_data["f_total_l"],'x',label="filled")   
    plt.plot(test.downsampled_data["time"],test.downsampled_data["f_total_l"],'o',label="downsampled")
    plt.legend()
    plt.title("Dowsampled total force data of the left insole")
    plt.show()


