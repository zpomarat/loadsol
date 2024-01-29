from Data import Data
import csv
import numpy as np
from os import getcwd
from datetime import datetime
import matplotlib.pyplot as plt
from scipy import interpolate

class DataLoadsol(Data):
    def __init__(self,path:str, frequency):
        super().__init__(path, frequency)
        self.raw_data = None
        self.pre_processed_data_l_f_heel = None
        self.pre_processed_time = None
        self.raw_data_l_f_heel = None # Defined here as None only to see whether the method extract_data has already been called or not.

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

    def extact_time(self):
        """Creates the attribute "time" to the DataLoadsol class.

            Time in s.

            self.time: np.ndarray [1D]"""
        if self.raw_data is None:
            self.csv_reader_loadsol()
        
        self.raw_time = self.raw_data[:, 0]

    def extact_time_left(self):
        """Creates the attribute "time" to the DataLoadsol class.

            Time in s.

            self.time: np.ndarray [1D]"""
        if self.raw_data is None:
            self.csv_reader_loadsol()
        
        self.raw_time_left = self.raw_data[:, 0]

    def extact_time_right(self):
        """Creates the attribute "time" to the DataLoadsol class.

            Time in s.

            self.time: np.ndarray [1D]"""
        if self.raw_data is None:
            self.csv_reader_loadsol()
        
        self.raw_time_right = self.raw_data[:, 12]
    
    def get_raw_time(self):
        try:
            return self.raw_time
        except:
            self.extact_time()
            return self.raw_time
    
    def get_raw_time_left(self):
        try:
            return self.raw_time_left
        except:
            self.extact_time_left()
            return self.raw_time_left
        
    def get_raw_time_right(self):
        try:
            return self.raw_time_right
        except:
            self.extact_time_right()
            return self.raw_time_right

    def extract_raw_data(self):
        """Fills the arrays of the raw data.
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
        """Creates the attribute "data" to the DataLoadSol class and returns it.

        Args:
            insole_side (str): "LEFT" or "RIGHT"
            data_type (str): "F_HEEL" or "F_MEDIAL" or "F_LATERAL" or "F_TOTAL" or "ACC" or "GYRO"

        data: np.ndarray [1D] if "F_HEEL" or "F_MEDIAL" or "F_LATERAL" or "F_TOTAL"
        data: np.ndarray [3D] if "ACC" or "GYRO"
        """
        
        if self.raw_data_l_f_heel is None:
            self.extract_raw_data()

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

        if self.pre_processed_data_l_f_heel is None:
            self.pre_processed_time = self.get_raw_time()

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

    def supress_duplicate_data(self):

        if self.pre_processed_data_l_f_heel is None:
            self.suppress_incorrect_values()

        # Indexes of duplicate values
        index_duplicate_left = [
            index for index, item in enumerate(self.raw_time_left) if item in self.raw_time_left[:index]
        ]

        index_duplicate_right = [
            index for index, item in enumerate(self.raw_time_right) if item in self.raw_time_right[:index]
        ]

        # Frequency
        FREQUENCY = 1 / (self.raw_time[1] - self.raw_time[0])

        # Replace by nan values the line before the line corresponding to the index identified
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

        self.pre_processed_time = self.pre_processed_time_left


    def fill_missing_data(self):

        if self.pre_processed_time is None:
            self.supress_duplicate_data()

        time = list(self.get_raw_time())
        indexes_missing_values = [indx for indx, item in enumerate(self.pre_processed_data_l_f_heel.tolist()) if np.isnan(item)]
        ntime=[]
        ndata = []
        for i in range(len(time)):
            if not(i in indexes_missing_values):
                ntime.append(time[i])
                ndata.append(time[i])
        
        ntime = np.array(ntime)
        ndata = np.array(ndata)

        f = interpolate.CubicSpline(ntime,ndata)

        time_interpolated = f(self.pre_processed_time)
        data_interpolated = f(self.pre_processed_data_l_f_heel)

        return data_interpolated,time_interpolated

        


       
           



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
    
    # resampled_data_l_f_tot = test.downsample(100,insole_side="LEFT",data_type="F_TOTAL")
    # resampled_time = test.downsample(100, time=test.time)
    
    # filter_data_l_f_tot = test.filter_data(2,20,10,data=resampled_data_l_f_tot,column=0,dimension_1=True)
    
    # plt.plot(test.raw_time,raw_data_l_f_tot,"-o" ,label = "raw", markersize = 2)
    # plt.plot(resampled_time, resampled_data_l_f_tot, "-o", label = "resampled", markersize = 2)
    # plt.plot(resampled_time, filter_data_l_f_tot, "-o", label = "filtered", markersize = 2)

    # plt.legend()
    # plt.show()

    plt.plot(test.raw_time, raw_data_l_f_tot,label="raw")
    test.suppress_incorrect_values()
    plt.plot(test.raw_time, test.raw_data_l_f_total,label="incorrect data suppressed")
    plt.legend()
    plt.show()

    test.extact_time_left()
    test.extact_time_right()
    plt.plot(test.raw_time_left,"-o",label="raw time left",markersize = 2)
    plt.plot(test.raw_time_right,"-o",label="raw time right",markersize = 2)
    test.supress_duplicate_data()
    plt.plot(test.raw_time_left,"-o",label="processed time left",markersize = 2)
    plt.plot(test.raw_time_right,"-o",label="processed time left",markersize = 2)
    plt.legend()
    plt.show()

    data_interpolated,time_interpolated = test.fill_missing_data()
    plt.plot(test.raw_time,test.pre_processed_data_l_f_heel,label='pre_processed')
    plt.plot(time_interpolated,data_interpolated,label='interpolated')
    plt.legend()
    plt.show()
