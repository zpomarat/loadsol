import csv
import numpy as np
from os import getcwd
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd


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
        # Initialise data with dupmicate values suppressed
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
    plt.show()
