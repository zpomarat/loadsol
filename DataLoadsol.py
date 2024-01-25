import Data
import csv
import numpy as np
from os import getcwd
from datetime import datetime


class DataLoadsol(Data.Data):
    def __init__(self,path:str):
        super().__init__(path)


    def convert_txt_to_csv(self, output_path: str):
        """Converts a txt file to a csv file and change the attribute "path" to the DataLoadsol class by the path of csv file.

        Args:
            output_path (str): path of the converted file.
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
        output_file = self.file_name + ".csv"
        with open(
            output_path + output_file, "w", newline="", encoding="utf-8"
        ) as outfile:
            # Create a CSV writer object for the output file
            writer = csv.writer(outfile, delimiter=output_delimiter)

            # Write the data to the CSV file
            writer.writerows(data)

        self.path = output_path + output_file

    def csv_reader_loadsol(self):
        """Reads csv file containing raw insoles data and write them in a ndarray.

        Returns:
            raw_data (np.ndarray): raw data of both insoles of a pair.
        """

        ## Read csv file line by line after going to the directory containing the file to handle
        lines = open(self.path, "r").readlines()

        # Start reading the file at line k to skip the header
        k = 4

        ## Select data
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
                print("Data missing, the file is not processed.")
                break
            raw_data[i, :] = data_line

        return raw_data

    def set_timestamp(self):
        """Creates the attribute "timestamp" to the DataLoadsol class."""
        ## Read csv file line by line after going to the directory containing the file to handle
        lines = open(self.path, "r").readlines()

        # Line containing the timestamp
        line = lines[0]

        # Extract the timestamp as a str
        str_timestamp = line[-33:-10]

        # Specify the format of the timestamp (Year_Month_Day_Hour_Minute_Second_Microsecond)
        format = '%Y_%m_%d_%H_%M_%S_%f'

        # Define the timestamp
        timestamp = datetime.strptime(str_timestamp,format)

        self.timestamp = timestamp

    def set_time(self):
        """Creates the attribute "time" to the DataLoadsol class.

            Time in s.

            self.time: np.ndarray [1D]"""
        raw_data = self.csv_reader_loadsol()
        self.time = raw_data[:, 0]

    def set_data(self,insole_side:str,data_type:str):
        """Creates the attribute "data" to the DataLoadSol class.

        Args:
            insole_side (str): "LEFT" or "RIGHT"
            data_type (str): "F_HEEL" or "F_MEDIAL" or "F_LATERAL" or "F_TOTAL" or "ACC" or "GYRO"

        self.data: np.ndarray [1D] if "F_HEEL" or "F_MEDIAL" or "F_LATERAL" or "F_TOTAL"
        self.data: np.ndarray [3D] if "ACC" or "GYRO"
        """
        raw_data = self.csv_reader_loadsol()
        match insole_side, data_type:
            case "LEFT", "F_HEEL":
                self.data = raw_data[:,1]
            case "LEFT", "F_MEDIAL":
                self.data = raw_data[:,2]
            case "LEFT", "F_LATERAL":
                self.data = raw_data[:,3]
            case "LEFT", "F_TOTAL":
                self.data = raw_data[:,4]
            case "LEFT", "ACC":
                self.data = raw_data[:,6:9]
            case "LEFT", "GYRO":
                self.data = raw_data[:,9:12]
            case "RIGHT", "F_HEEL":
                self.data = raw_data[:,13]
            case "RIGHT", "F_MEDIAL":
                self.data = raw_data[:,14]
            case "RIGHT", "F_LATERAL":
                self.data = raw_data[:,15]
            case "RIGHT", "F_TOTAL":
                self.data = raw_data[:,16]
            case "RIGHT", "ACC":
                self.data = raw_data[:,18:21]
            case "RIGHT", "GYRO":
                self.data = raw_data[:,21:24]


    # def remove_duplicate_data(self):
    #     """Identify duplicate data in raw data and replace them by NaN values.

    #     Returns:
    #         time (np.ndarray): time with unique and interpolated data.
    #         left_force, right_force (np.ndarray): unique force data.
    #         left_accelero, right_accelero (np.ndarray): unique accelerometer data.
    #         left_gyro, right_gyro (np.ndarray): unique gyrometer data.
    #     """
    #     # Get raw data
    #     time = self.get_time()
    #     left_force = self.get_left_force()
    #     right_force = self.get_right_force()
    #     left_accelero = self.get_left_accelero()
    #     right_accelero = self.get_right_accelero()
    #     left_gyro = self.get_left_gyro()
    #     right_gyro = self.get_right_gyro()

    #     # Indexes of duplicate values
    #     index_duplicate = [
    #         index for index, item in enumerate(time) if item in time[:index]
    #     ]

    #     # Frequency
    #     FREQUENCY = 1 / (time[1] - time[0])

    #     # Replace by nan values the line before the line corresponding to the index identified
    #     for i in index_duplicate:
    #         time[i - 1] = np.NaN
    #         left_force[i - 1] = np.NaN
    #         right_force[i - 1] = np.NaN
    #         left_accelero[i - 1] = np.NaN
    #         right_accelero[i - 1] = np.NaN
    #         left_gyro[i - 1] = np.NaN
    #         right_gyro[i - 1] = np.NaN

    #         # Complete time nan values
    #         time[i - 1] = (i - 1) / FREQUENCY

    #     return (
    #         time,
    #         left_force,
    #         right_force,
    #         left_accelero,
    #         right_accelero,
    #         left_gyro,
    #         right_gyro,
    #     )

    # def suppress_outliers(self):
    #     """Suppresses the outliers in force data without duplicate (outlier = negative value of force).

    #     Returns:
    #         time, left_force, right_force, left_accelero, right_accelero, left_gyro, right_gyro (np.ndarray): data with outliers suppressed.
    #     """
    #     # Get data without duplicate
    #     (
    #         time,
    #         left_force,
    #         right_force,
    #         left_accelero,
    #         right_accelero,
    #         left_gyro,
    #         right_gyro,
    #     ) = self.remove_duplicate_data()
    #     # left_force = self.get_left_force()
    #     # right_force = self.get_right_force()

    #     # Indexes of outliers of the left insole
    #     index_outlier_left = [
    #         index for index, item in enumerate(left_force[:, 0]) if item < 0
    #     ]

    #     # Indexes of outliers of the right insole
    #     index_outlier_right = [
    #         index for index, item in enumerate(right_force[:, 0]) if item < 0
    #     ]

    #     ## Replace by nan values the line corresponding to the indexes of outliers
    #     for i in index_outlier_left:
    #         left_force[i, :] = np.NaN
    #     for i in index_outlier_right:
    #         right_force[i, :] = np.NaN

    #     return (
    #         time,
    #         left_force,
    #         right_force,
    #         left_accelero,
    #         right_accelero,
    #         left_gyro,
    #         right_gyro,
    #     )

    # def interpolate(self):
    #     """Interpolates missing data from data without duplicate and outliers.

    #     Returns:
    #         tile, left_force, right_force, left_accelero, right_accelero, left_gyro, right_gyro (np.ndarray): data interpolated.
    #     """
    #     # Get raw data without duplicate and outliers
    #     (
    #         time,
    #         left_force,
    #         right_force,
    #         left_accelero,
    #         right_accelero,
    #         left_gyro,
    #         right_gyro,
    #     ) = self.suppress_outliers()

    #     # Create TimeSeries
    #     data = ktk.TimeSeries()

    #     # Add data to the TimeSeries
    #     data.time = time
    #     data.data["ForceLeft"] = left_force
    #     data.data["ForceRight"] = right_force
    #     data.data["AcceleroLeft"] = left_accelero
    #     data.data["AcceleroRight"] = right_accelero
    #     data.data["GyroLeft"] = left_gyro
    #     data.data["GyroRight"] = right_gyro

    #     # Interpolate data
    #     data = data.fill_missing_samples(
    #         max_missing_samples=0, method="cubic", in_place=True
    #     )

    #     # Extract interpolated data
    #     left_force_interpolated = data.data["ForceLeft"]
    #     right_force_interpolated = data.data["ForceRight"]
    #     left_accelero_interpolated = data.data["AcceleroLeft"]
    #     right_accelero_interpolated = data.data["AcceleroRight"]
    #     left_gyro_interpolated = data.data["GyroLeft"]
    #     right_gyro_interpolated = data.data["GyroRight"]

    #     return (
    #         time,
    #         left_force_interpolated,
    #         right_force_interpolated,
    #         left_accelero_interpolated,
    #         right_accelero_interpolated,
    #         left_gyro_interpolated,
    #         right_gyro_interpolated,
    #     )


if __name__ == "__main__":
    curr_path = getcwd()

    test = DataLoadsol(curr_path + "\\examples\\data\\test_poussee_4_ls.txt")
    print("Time:")
    print(test.time)
    print("File name: ")
    print(test.file_name)

    test.convert_txt_to_csv(curr_path + "\\examples\\data\\")

    raw_data = test.csv_reader_loadsol()
    print("Raw data:")
    print(raw_data)

    test.set_timestamp()
    print("Timestamp:")
    print(test.timestamp)

    test.set_time()
    print("Time:")
    print(test.time)

    test.set_data("LEFT","F_TOTAL")
    print("Data (total force of the left insole)")
    print(test.data)