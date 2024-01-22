import csv
import numpy as np
from os import getcwd
import matplotlib.pyplot as plt
import kineticstoolkit as ktk

ktk.import_extensions()
ktk.change_defaults()


class Loadsol:
    def __init__(self, path: str):
        self.path = path

    def get_name(self):
        name_split = self.path.split("\\")
        self.name = name_split[-1][:-4]
        return self.name

    def convert_txt_to_csv(self, output_path: str):
        """Converts a txt file to a csv file.

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
        output_file = self.get_name() + ".csv"
        with open(
            output_path + output_file, "w", newline="", encoding="utf-8"
        ) as outfile:
            # Create a CSV writer object for the output file
            writer = csv.writer(outfile, delimiter=output_delimiter)

            # Write the data to the CSV file
            writer.writerows(data)

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

    def get_timestamp(self):
        """Returns the timestamp of the insoles data file."""
        ## Read csv file line by line after going to the directory containing the file to handle
        lines = open(self.path, "r").readlines()

        # Line containing the timestamp
        line = lines[0]

        # Extract the timestamp
        timestamp = line[-22:-10]

        return timestamp

    def get_time(self):
        """Returns an array containing the raw time data."""
        raw_data = self.csv_reader_loadsol()
        self.time = raw_data[:, 0]
        return self.time

    def get_left_force(self):
        """Returns an array containing the raw force data of the left insole (Fheel, Fmedial, Flateral, Ftotal)."""
        raw_data = self.csv_reader_loadsol()
        self.left_force = raw_data[:, 1:5]
        return self.left_force

    def get_right_force(self):
        """Returns an array containing the raw force data of the right insole ([Fheel, Fmedial, Flateral, Ftotal])."""
        raw_data = self.csv_reader_loadsol()
        self.right_force = raw_data[:, 13:17]
        return self.right_force

    def get_left_accelero(self):
        """Returns an array containing the raw data of the accelerometer of the left insole ([AccX, AccY, AccZ])."""
        raw_data = self.csv_reader_loadsol()
        self.left_accelero = raw_data[:, 6:9]
        return self.left_accelero

    def get_right_accelero(self):
        """Returns an array containing the raw data of the accelerometer of the right insole ([AccX, AccY, AccZ])."""
        raw_data = self.csv_reader_loadsol()
        self.right_accelero = raw_data[:, 18:21]
        return self.right_accelero

    def get_left_gyro(self):
        """Returns an array containing the raw data of the gyrometer of the left insole ([GyroX, GyroY, GyroZ])."""
        raw_data = self.csv_reader_loadsol()
        self.left_gyro = raw_data[:, 9:12]
        return self.left_gyro

    def get_right_gyro(self):
        """Returns an array containing the raw data of the gyrometer of the right insole ([GyroX, GyroY, GyroZ])."""
        raw_data = self.csv_reader_loadsol()
        self.right_gyro = raw_data[:, 21:24]
        return self.right_gyro

    def remove_duplicate_data(self):
        """Identify duplicate data and replace them by NaN values.

        Returns:
            time (np.ndarray): time with unique and interpolated data.
            left_force, right_force (np.ndarray): unique force data.
            left_accelero, right_accelero (np.ndarray): unique accelerometer data.
            left_gyro, right_gyro (np.ndarray): unique gyrometer data.
        """
        # Get raw data
        time = self.get_time()
        left_force = self.get_left_force()
        right_force = self.get_right_force()
        left_accelero = self.get_left_accelero()
        right_accelero = self.get_right_accelero()
        left_gyro = self.get_left_gyro()
        right_gyro = self.get_right_gyro()

        # Indexes of duplicate values
        index_duplicate = [
            index for index, item in enumerate(time) if item in time[:index]
        ]

        # Frequency
        FREQUENCY = 1 / (time[1] - time[0])

        # Replace by nan values the line before the line corresponding to the index identified
        for i in index_duplicate:
            time[i - 1] = np.NaN
            left_force[i - 1] = np.NaN
            right_force[i - 1] = np.NaN
            left_accelero[i - 1] = np.NaN
            right_accelero[i - 1] = np.NaN
            left_gyro[i - 1] = np.NaN
            right_gyro[i - 1] = np.NaN

            # Complete time nan values
            time[i - 1] = (i - 1) / FREQUENCY

        return (
            time,
            left_force,
            right_force,
            left_accelero,
            right_accelero,
            left_gyro,
            right_gyro,
        )

    def suppress_outliers(self):
        """Suppresses the outliers in force data (outlier = negative value of force).

        Returns:
            left_force, right_force (np.ndarray): force data with outliers suppressed.
        """
        # Get data without duplicate
        (
            time,
            left_force,
            right_force,
            left_accelero,
            right_accelero,
            left_gyro,
            right_gyro,
        ) = self.remove_duplicate_data()
        # left_force = self.get_left_force()
        # right_force = self.get_right_force()

        # Indexes of outliers of the left insole
        index_outlier_left = [
            index for index, item in enumerate(left_force[:, 0]) if item < 0
        ]

        # Indexes of outliers of the right insole
        index_outlier_right = [
            index for index, item in enumerate(right_force[:, 0]) if item < 0
        ]

        ## Replace by nan values the line corresponding to the indexes of outliers
        for i in index_outlier_left:
            left_force[i, :] = np.NaN
        for i in index_outlier_right:
            right_force[i, :] = np.NaN

        return (
            time,
            left_force,
            right_force,
            left_accelero,
            right_accelero,
            left_gyro,
            right_gyro,
        )

    def interpolate(self):
        # Get raw data without duplicate and outliers
        (
            time,
            left_force,
            right_force,
            left_accelero,
            right_accelero,
            left_gyro,
            right_gyro,
        ) = self.suppress_outliers()

        # Create TimeSeries
        data = ktk.TimeSeries()

        # Add data to the TimeSeries
        data.time = time
        data.data["ForceLeft"] = left_force
        data.data["ForceRight"] = right_force
        data.data["AcceleroLeft"] = left_accelero
        data.data["AcceleroRight"] = right_accelero
        data.data["GyroLeft"] = left_gyro
        data.data["GyroRight"] = right_gyro

        # Interpolate data
        data = data.fill_missing_samples(
            max_missing_samples=0, method="cubic", in_place=True
        )

        # Extract interpolated data
        left_force_interpolated = data.data["ForceLeft"]
        right_force_interpolated = data.data["ForceRight"]
        left_accelero_interpolated = data.data["AcceleroLeft"]
        right_accelero_interpolated = data.data["AcceleroRight"]
        left_gyro_interpolated = data.data["GyroLeft"]
        right_gyro_interpolated = data.data["GyroRight"]

        return (
            time,
            left_force_interpolated,
            right_force_interpolated,
            left_accelero_interpolated,
            right_accelero_interpolated,
            left_gyro_interpolated,
            right_gyro_interpolated,
        )


if __name__ == "__main__":
    curr_path = getcwd()

    test = Loadsol(curr_path + "\\examples\\data\\test_poussee_4_ls.csv")

    print("Name: " + test.get_name())
    print("Raw data: ")
    print(test.csv_reader_loadsol())
    print("Timestamp: ")
    print(test.get_timestamp())
    print("Time: ")
    print(test.get_time())
    print("Force left: ")
    print(test.get_left_force())
    print("Force right: ")
    print(test.get_right_force())
    print("Accelero left: ")
    print(test.get_left_accelero())
    print("Accelero right: ")
    print(test.get_right_accelero())
    print("Gyro left: ")
    print(test.get_left_gyro())
    print("Gyro right: ")
    print(test.get_right_gyro())

    (
        time,
        left_force_unique,
        right_force_unique,
        left_accelero_unique,
        right_accelero_unique,
        left_gyro_unique,
        right_gyro_unique,
    ) = test.remove_duplicate_data()

    (
        time,
        left_force_cleaned,
        right_force_cleaned,
        left_accelero_cleaned,
        right_accelero_cleaned,
        left_gyro_cleaned,
        right_gyro_cleaned,
    ) = test.suppress_outliers()

    plt.plot(time, left_force_cleaned)
    plt.show()
    plt.plot(time, right_force_cleaned)
    plt.show()

    (
        time,
        left_force_interpolated,
        right_force_interpolated,
        left_accelero_interpolated,
        right_accelero_interpolated,
        left_gyro_interpolated,
        right_gyro_interpolated,
    ) = test.interpolate()

    plt.plot(time, left_force_cleaned[:, 3], "-")
    plt.plot(time, left_force_interpolated[:, 3], "--")
    plt.show()
