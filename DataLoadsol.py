from Data import Data
import csv
import numpy as np
from os import getcwd
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

class DataLoadsol(Data):
    def __init__(self,path:str, frequency:int):
        super().__init__(path, frequency)
        # Define some attributs as None only to see whether specific methods have already been called or not.
        self.raw_data = None
        self.raw_data_l_f_heel = None
        self.pre_processed_data_l_f_heel = None
        self.pre_processed_time = None 
        self.filled_data_l_f_heel = None
        self.path_csv = self.path[:-3] + "csv"
        

    def convert_txt_to_csv(self, output_directory: str):
        """Converts a txt file to a csv file and change the attribute "path" to the DataLoadsol class by the path of csv file.

        Args:
            output_directory (str): path of the directory contaning the converted file.
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
        """Reads csv file containing raw insoles data and writes them in a ndarray.

        Returns:
            raw_data (np.ndarray): raw data of both insoles of a pair.
        """

        ## Read csv file line by line after going to the directory containing the file to handle
        lines = open(self.path_csv, "r").readlines()

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
                raise ValueError("Data missing, the file '" + self.file_name + "' is not processed.")
                break
            raw_data[i, :] = data_line
        self.raw_data = raw_data


    def extract_timestamp(self):
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


    def extract_time_left(self):
        """Creates the attribute "time_left" to the DataLoadsol class.

            Time in s.

            self.time: np.ndarray [1D]"""
        
        if self.raw_data is None:
            self.csv_reader_loadsol()
        
        self.raw_time_left = self.raw_data[:, 0]


    def extract_time_right(self):
        """Creates the attribute "time_right" to the DataLoadsol class.

            Time in s.

            self.time: np.ndarray [1D]"""
        
        if self.raw_data is None:
            self.csv_reader_loadsol()
        
        self.raw_time_right = self.raw_data[:, 12]
    

    def get_raw_time_left(self):
        """Returns the raw left time vector."""

        try:
            return self.raw_time_left
        except:
            self.extract_time_left()
            return self.raw_time_left
        

    def get_raw_time_right(self):
        """Returns the raw right time vector."""

        try:
            return self.raw_time_right
        except:
            self.extract_time_right()
            return self.raw_time_right


    def extract_raw_data(self):
        """Creates specific attributes "data" to the DataLoadSol class.
        """

        if self.raw_data is None:
            self.csv_reader_loadsol()

        self.raw_data_l_f_heel = self.raw_data[:,1]
        self.raw_data_l_f_medial = self.raw_data[:,2]
        self.raw_data_l_f_lateral = self.raw_data[:,3]
        self.raw_data_l_f_total = self.raw_data[:,4]
        self.raw_data_l_acc = self.raw_data[:,6:9]
        self.raw_data_l_gyro = self.raw_data[:,9:12]

        self.raw_data_r_f_heel = self.raw_data[:,13]
        self.raw_data_r_f_medial = self.raw_data[:,14]
        self.raw_data_r_f_lateral = self.raw_data[:,15]
        self.raw_data_r_f_total = self.raw_data[:,16]
        self.raw_data_r_acc = self.raw_data[:,18:21]
        self.raw_data_r_gyro = self.raw_data[:,21:24]

        
    def get_raw_data(self,insole_side:str,data_type:str):
        """Returns specific attributes "raw_data" of the DataLoadSol class.

        Args:
            insole_side (str): "LEFT" or "RIGHT"
            data_type (str): "F_HEEL" or "F_MEDIAL" or "F_LATERAL" or "F_TOTAL" or "ACC" or "GYRO"

        raw_data: np.ndarray [1D] if "F_HEEL" or "F_MEDIAL" or "F_LATERAL" or "F_TOTAL"
        raw_data: np.ndarray [3D] if "ACC" or "GYRO"
        """
        
        if self.raw_data_l_f_heel is None:
            self.extract_raw_data()

        # Get raw data
        match insole_side, data_type:
            case "LEFT", "F_HEEL":
                raw_data = self.raw_data[:,1]
            case "LEFT", "F_MEDIAL":
                raw_data = self.raw_data[:,2]
            case "LEFT", "F_LATERAL":
                raw_data = self.raw_data[:,3]
            case "LEFT", "F_TOTAL":
                raw_data = self.raw_data[:,4]
            case "LEFT", "ACC":
                raw_data = self.raw_data[:,6:9]
            case "LEFT", "GYRO":
                raw_data = self.raw_data[:,9:12]
            case "RIGHT", "F_HEEL":
                raw_data = self.raw_data[:,13]
            case "RIGHT", "F_MEDIAL":
                raw_data = self.raw_data[:,14]
            case "RIGHT", "F_LATERAL":
                raw_data = self.raw_data[:,15]
            case "RIGHT", "F_TOTAL":
                raw_data = self.raw_data[:,16]
            case "RIGHT", "ACC":
                raw_data = self.raw_data[:,18:21]
            case "RIGHT", "GYRO":
                raw_data = self.raw_data[:,21:24]
        return raw_data     


    def suppress_incorrect_values(self):
        """Replaces the incorrect values in force data by NaN (incorrect value = negative value of force per zone).
            Creates new specific attributes "pre_processed_data" to the DataLoadsol class.
        """

        if self.raw_data_l_f_heel is None:
            self.extract_raw_data()

        # Initialise pre processed data
            self.pre_processed_data_l_f_heel = self.get_raw_data('LEFT','F_HEEL')
            self.pre_processed_data_l_f_medial = self.get_raw_data('LEFT','F_MEDIAL')
            self.pre_processed_data_l_f_lateral = self.get_raw_data('LEFT','F_LATERAL')
            self.pre_processed_data_l_f_total = self.get_raw_data('LEFT','F_TOTAL')
            self.pre_processed_data_l_acc = self.get_raw_data('LEFT','ACC')
            self.pre_processed_data_l_gyro = self.get_raw_data('LEFT','GYRO')
            self.pre_processed_time_left = self.get_raw_time_left()

            self.pre_processed_data_r_f_heel = self.get_raw_data('RIGHT','F_HEEL')
            self.pre_processed_data_r_f_medial = self.get_raw_data('RIGHT','F_MEDIAL')
            self.pre_processed_data_r_f_lateral = self.get_raw_data('RIGHT','F_LATERAL')
            self.pre_processed_data_r_f_total = self.get_raw_data('RIGHT','F_TOTAL')
            self.pre_processed_data_r_acc = self.get_raw_data('RIGHT','ACC')
            self.pre_processed_data_r_gyro = self.get_raw_data('RIGHT','GYRO')
            self.pre_processed_time_right = self.get_raw_time_right()

        # Find indexes of incorrect values
        index_incorrect_values_left = [index for index, item in enumerate(self.raw_data_l_f_heel) if item < 0]
        index_incorrect_values_right = [index for index, item in enumerate(self.raw_data_r_f_heel) if item < 0]

        # Replace incorrect values by NaN
        for i in index_incorrect_values_left:
            self.pre_processed_data_l_f_heel[i] = np.NaN
            self.pre_processed_data_l_f_medial[i] = np.NaN
            self.pre_processed_data_l_f_lateral[i] = np.NaN
            self.pre_processed_data_l_f_total[i] = np.NaN

        for i in index_incorrect_values_right:
            self.pre_processed_data_r_f_heel[i] = np.NaN
            self.pre_processed_data_r_f_medial[i] = np.NaN
            self.pre_processed_data_r_f_lateral[i] = np.NaN
            self.pre_processed_data_r_f_total[i] = np.NaN


    def suppress_duplicate_data(self):
        """Finds and suppresses duplicate data.
            Redefines specififc attributes "pre_processed_data".
            Redefine the attribut "time".
        """

        if self.pre_processed_data_l_f_heel is None:
            self.suppress_incorrect_values()

        # Initialise pre processed time
        self.pre_processed_time_left = self.get_raw_time_left()
        self.pre_processed_time_right = self.get_raw_time_right()

        # Indexes of duplicate values
        index_duplicate_left = [
            index for index, item in enumerate(self.raw_time_left) if item in self.raw_time_left[:index]
        ]

        index_duplicate_right = [
            index for index, item in enumerate(self.raw_time_right) if item in self.raw_time_right[:index]
        ]

        # Frequency
        # FREQUENCY = 1 / (self.raw_time_left[1] - self.raw_time_left[0])
        FREQUENCY = self.frequency

        # Replace by nan values the line before the line corresponding to the index identified for the left side
        for i in index_duplicate_left:
            self.pre_processed_time_left[i-1] = np.NaN
            self.pre_processed_data_l_f_heel[i-1] = np.NaN
            self.pre_processed_data_l_f_medial[i-1] = np.NaN
            self.pre_processed_data_l_f_lateral[i-1] = np.NaN
            self.pre_processed_data_l_f_total[i-1] = np.NaN
            self.pre_processed_data_l_acc[i-1] = np.NaN
            self.pre_processed_data_l_gyro[i-1] = np.NaN

            # Complete time nan values
            self.pre_processed_time_left[i - 1] = (i - 1) / FREQUENCY

        # Replace by nan values the line before the line corresponding to the index identified for the right side
        for i in index_duplicate_right:
            self.pre_processed_time_right[i-1] = np.NaN
            self.pre_processed_data_r_f_heel[i-1] = np.NaN
            self.pre_processed_data_r_f_medial[i-1] = np.NaN
            self.pre_processed_data_r_f_lateral[i-1] = np.NaN
            self.pre_processed_data_r_f_total[i-1] = np.NaN
            self.pre_processed_data_r_acc[i-1] = np.NaN
            self.pre_processed_data_r_gyro[i-1] = np.NaN

            # Complete time nan values
            self.pre_processed_time_right[i - 1] = (i - 1) / FREQUENCY

        # Redefine time attribut
        self.pre_processed_time = self.pre_processed_time_left


    def get_pre_processed_data(self,insole_side, data_type):
        """Returns specific attributes "pre_processed_data" of the DataLoadSol class.

        Args:
            insole_side (str): "LEFT" or "RIGHT"
            data_type (str): "F_HEEL" or "F_MEDIAL" or "F_LATERAL" or "F_TOTAL" or "ACC" or "GYRO"

        pre_processed_data: np.ndarray [1D] if "F_HEEL" or "F_MEDIAL" or "F_LATERAL" or "F_TOTAL"
        pre_processed_data: np.ndarray [3D] if "ACC" or "GYRO"
        """

        if self.pre_processed_data_l_f_heel is None:
            self.suppress_duplicate_data()

        # Get pre-processed data
        match insole_side, data_type:
            case "LEFT", "F_HEEL":
                pre_processed_data = self.pre_processed_data_l_f_heel
            case "LEFT", "F_MEDIAL":
                pre_processed_data = self.pre_processed_data_l_f_lateral
            case "LEFT", "F_LATERAL":
                pre_processed_data = self.pre_processed_data_l_f_medial
            case "LEFT", "F_TOTAL":
                pre_processed_data = self.pre_processed_data_l_f_total
            case "LEFT", "ACC":
                pre_processed_data = self.pre_processed_data_l_acc
            case "LEFT", "GYRO":
                pre_processed_data = self.pre_processed_data_l_gyro
            case "RIGHT", "F_HEEL":
                pre_processed_data = self.pre_processed_data_r_f_heel
            case "RIGHT", "F_MEDIAL":
                pre_processed_data = self.pre_processed_data_r_f_lateral
            case "RIGHT", "F_LATERAL":
                pre_processed_data = self.pre_processed_data_r_f_medial
            case "RIGHT", "F_TOTAL":
                pre_processed_data = self.pre_processed_data_r_f_total
            case "RIGHT", "ACC":
                pre_processed_data = self.pre_processed_data_r_acc
            case "RIGHT", "GYRO":
                pre_processed_data = self.pre_processed_data_r_gyro
        return pre_processed_data 
    

    def get_pre_processed_time(self):
        """Returns the pre-processed time vector.
        """

        if self.pre_processed_time is None:
            self.suppress_duplicate_data()
            
        return self.pre_processed_time


    def fill_missing_data(self):
        """Interpolates missing data."""

        if self.pre_processed_time is None:
            self.suppress_duplicate_data()

        # Initialise filled data
        self.filled_data_l_f_heel = self.get_pre_processed_data('LEFT','F_HEEL')
        self.filled_data_l_f_medial = self.get_pre_processed_data('LEFT','F_MEDIAL')
        self.filled_data_l_f_lateral = self.get_pre_processed_data('LEFT','F_LATERAL')
        self.filled_data_l_f_total = self.get_pre_processed_data('LEFT','F_TOTAL')
        self.filled_data_l_acc = self.get_pre_processed_data('LEFT','ACC')
        self.filled_data_l_gyro = self.get_pre_processed_data('LEFT','GYRO')

        self.filled_data_r_f_heel = self.get_pre_processed_data('RIGHT','F_HEEL')
        self.filled_data_r_f_medial = self.get_pre_processed_data('RIGHT','F_MEDIAL')
        self.filled_data_r_f_lateral = self.get_pre_processed_data('RIGHT','F_LATERAL')
        self.filled_data_r_f_total = self.get_pre_processed_data('RIGHT','F_TOTAL')
        self.filled_data_r_acc = self.get_pre_processed_data('RIGHT','ACC')
        self.filled_data_r_gyro = self.get_pre_processed_data('RIGHT','GYRO')

        # Convert the data to fill into dataframe
        data_l_f_heel = pd.DataFrame(self.filled_data_l_f_heel)
        data_l_f_medial = pd.DataFrame(self.filled_data_l_f_medial)
        data_l_f_lateral = pd.DataFrame(self.filled_data_l_f_lateral)
        data_l_f_total = pd.DataFrame(self.filled_data_l_f_total)
        data_l_acc = pd.DataFrame(self.filled_data_l_acc)
        data_l_gyro = pd.DataFrame(self.filled_data_l_gyro)

        data_r_f_heel = pd.DataFrame(self.filled_data_r_f_heel)
        data_r_f_medial = pd.DataFrame(self.filled_data_r_f_medial)
        data_r_f_lateral = pd.DataFrame(self.filled_data_r_f_lateral)
        data_r_f_total = pd.DataFrame(self.filled_data_r_f_total)
        data_r_acc = pd.DataFrame(self.filled_data_r_acc)
        data_r_gyro = pd.DataFrame(self.filled_data_r_gyro)

        # Interpolate with the cubic method
        data_l_f_heel_filled = data_l_f_heel.interpolate('cubic')
        data_l_f_medial_filled = data_l_f_medial.interpolate('cubic')
        data_l_f_lateral_filled = data_l_f_lateral.interpolate('cubic')
        data_l_f_total_filled = data_l_f_total.interpolate('cubic')
        data_l_acc_filled = data_l_acc.interpolate('cubic')
        data_l_gyro_filled = data_l_gyro.interpolate('cubic')

        data_r_f_heel_filled = data_r_f_heel.interpolate('cubic')
        data_r_f_medial_filled = data_r_f_medial.interpolate('cubic')
        data_r_f_lateral_filled = data_r_f_lateral.interpolate('cubic')
        data_r_f_total_filled = data_r_f_total.interpolate('cubic')
        data_r_acc_filled = data_r_acc.interpolate('cubic')
        data_r_gyro_filled = data_r_gyro.interpolate('cubic')
        
        # Convert the data interpolated into ndarray
        data_l_f_heel_filled = np.reshape(data_l_f_heel_filled.to_numpy(),(len(data_l_f_heel_filled),))
        data_l_f_medial_filled = np.reshape(data_l_f_medial_filled.to_numpy(),(len(data_l_f_medial_filled),))
        data_l_f_lateral_filled = np.reshape(data_l_f_lateral_filled.to_numpy(),(len(data_l_f_lateral_filled),))
        data_l_f_total_filled = np.reshape(data_l_f_total_filled.to_numpy(),(len(data_l_f_total_filled),))
        data_l_acc_filled = data_l_acc_filled.to_numpy()
        data_l_gyro_filled = data_l_gyro_filled.to_numpy()

        data_r_f_heel_filled = np.reshape(data_r_f_heel_filled.to_numpy(),(len(data_r_f_heel_filled),))
        data_r_f_medial_filled = np.reshape(data_r_f_medial_filled.to_numpy(),(len(data_r_f_medial_filled),))
        data_r_f_lateral_filled = np.reshape(data_r_f_lateral_filled.to_numpy(),(len(data_r_f_lateral_filled),))
        data_r_f_total_filled = np.reshape(data_r_f_total_filled.to_numpy(),(len(data_r_f_total_filled),))
        data_r_acc_filled = data_r_acc_filled.to_numpy()
        data_r_gyro_filled = data_r_gyro_filled.to_numpy()
        
        # Fill attributes
        self.filled_data_l_f_heel = data_l_f_heel_filled
        self.filled_data_l_f_medial = data_l_f_medial_filled
        self.filled_data_l_f_lateral = data_l_f_lateral_filled
        self.filled_data_l_f_total = data_l_f_total_filled
        self.filled_data_l_acc = data_l_acc_filled
        self.filled_data_l_gyro = data_l_gyro_filled

        self.filled_data_r_f_heel = data_r_f_heel_filled
        self.filled_data_r_f_medial = data_r_f_medial_filled
        self.filled_data_r_f_lateral = data_r_f_lateral_filled
        self.filled_data_r_f_total = data_r_f_total_filled
        self.filled_data_r_acc = data_r_acc_filled
        self.filled_data_r_gyro = data_r_gyro_filled
 
    
    def get_filled_data(self, insole_side, data_type):
        """Returns specific attributes "filled_data" of the DataLoadSol class.

        Args:
            insole_side (str): "LEFT" or "RIGHT"
            data_type (str): "F_HEEL" or "F_MEDIAL" or "F_LATERAL" or "F_TOTAL" or "ACC" or "GYRO"

        filled_data: np.ndarray [1D] if "F_HEEL" or "F_MEDIAL" or "F_LATERAL" or "F_TOTAL"
        filled_data: np.ndarray [3D] if "ACC" or "GYRO"
        """
        
        if self.filled_data_l_f_heel is None:
            self.fill_missing_data()

        # Get pre-processed data
        match insole_side, data_type:
            case "LEFT", "F_HEEL":
                filled_data = self.filled_data_l_f_heel
            case "LEFT", "F_MEDIAL":
                filled_data = self.filled_data_l_f_lateral
            case "LEFT", "F_LATERAL":
                filled_data = self.filled_data_l_f_medial
            case "LEFT", "F_TOTAL":
                filled_data = self.filled_data_l_f_total
            case "LEFT", "ACC":
                filled_data = self.filled_data_l_acc
            case "LEFT", "GYRO":
                filled_data = self.filled_data_l_gyro
            case "RIGHT", "F_HEEL":
                filled_data = self.filled_data_r_f_heel
            case "RIGHT", "F_MEDIAL":
                filled_data = self.filled_data_r_f_lateral
            case "RIGHT", "F_LATERAL":
                filled_data = self.filled_data_r_f_medial
            case "RIGHT", "F_TOTAL":
                filled_data = self.filled_data_r_f_total
            case "RIGHT", "ACC":
                filled_data = self.filled_data_r_acc
            case "RIGHT", "GYRO":
                filled_data = self.filled_data_r_gyro
        return filled_data
        



if __name__ == "__main__":
    curr_path = getcwd()

    test = DataLoadsol(curr_path + "\\examples\\data\\test_poussee_4_ls.txt",200)
    # test = DataLoadsol(curr_path + "/examples/data/test_poussee_4_ls.txt", frequency=200)

    print(f"Time: {test.time}")
    print(f"File name: {test.file_name}")

    test.convert_txt_to_csv(curr_path + "\\examples\\data\\")

    raw_data = test.csv_reader_loadsol()
    print(f"Raw data: {test.raw_data}")

    test.extract_timestamp()
    print(f"Timestamp: {test.timestamp}")

    test.extact_time()
    print(f"Time: {test.time}")

    raw_data_l_f_tot = test.get_raw_data("LEFT","F_TOTAL")
    print(f"Data (total force of the left insole): {raw_data_l_f_tot}")

    plt.plot(test.raw_time, raw_data_l_f_tot,label="raw")
    test.suppress_incorrect_values()
    plt.plot(test.raw_time, test.raw_data_l_f_total,label="incorrect data suppressed")
    plt.legend()
    plt.show()

    test.extract_time_left()
    test.extract_time_right()
    plt.plot(test.raw_time_left,"-o",label="raw time left",markersize = 2)
    plt.plot(test.raw_time_right,"-o",label="raw time right",markersize = 2)
    test.suppress_duplicate_data()
    plt.plot(test.raw_time_left,"-o",label="processed time left",markersize = 2)
    plt.plot(test.raw_time_right,"-o",label="processed time left",markersize = 2)
    plt.legend()
    plt.show()

    filled_data_l_f_heel = test.get_filled_data('LEFT','F_HEEL')

    plt.plot(test.pre_processed_time,filled_data_l_f_heel,label='interpolated')
    plt.plot(test.raw_time,test.pre_processed_data_l_f_heel,label='pre_processed')
    plt.legend()
    plt.show()

    resampled_data_l_f_heel = test.downsample(100,insole_side="LEFT",data_type="F_HEEL")
    resampled_time = test.downsample(100, time=test.pre_processed_time)

    filter_data_l_f_heel = test.filter_data(2,20,10,data=resampled_data_l_f_heel,column=0,dimension_1=True)

    
    plt.plot(test.pre_processed_time, filled_data_l_f_heel,"-o" ,label = "filled", markersize = 2)
    plt.plot(resampled_time, resampled_data_l_f_heel, "-o", label = "resampled", markersize = 2)
    plt.plot(test.raw_time,test.raw_data_l_f_heel,"-o" ,label = "raw", markersize = 2)
    plt.plot(resampled_time, filter_data_l_f_heel, "-o", label = "filtered", markersize = 2)

    plt.legend()
    plt.show()
