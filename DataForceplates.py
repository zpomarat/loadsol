import Data
from os import getcwd
from datetime import datetime
import c3d
import numpy as np
import matplotlib.pyplot as plt


class DataForceplates(Data.Data):
    def __init__(self, path: str, frequency):
        super().__init__(path, frequency)
        self.raw_data = None

    # def get_name(self):
    #     name_split = self.path.split("\\")
    #     self.name = name_split[-1][:-4]
    #     return self.name

    def set_timestamp(self):
        """Creates the attribute "timestamp" of the DataForceplates class."""
        # Path of the xcp file containing the timestamp
        file_path = self.path[:-3] + "xcp"

        # Read the line line containing the timestamp in the text file
        with open(file_path) as file:
            lines = file.readlines()

        # Line containing the timestamp
        line = lines[7]

        # Split the line to extract the part containing the timestamp
        txt = line.split('START_TIME="')

        # Extract the timestamp as a str
        str_timestamp = txt[1][:-7]

        # Specify the format of the timestamp (Year-Month-Day Hour:Minute:Second.Microsecond)
        format = '%Y-%m-%d %H:%M:%S.%f'

        # Define the timestamp
        timestamp = datetime.strptime(str_timestamp,format)

        self.timestamp = timestamp

    def c3d_reader_forceplates(self):
        """Reads a c3d file and extracts the raw analog data.

        Returns:
            raw_data (np.ndarray): raw analog data [ix30]
        """
        # Read the c3d file
        reader = c3d.Reader(open(self.path,'rb'))

        # Extract analog data (raw data + others parameters)
        data_analog = []
       
        for analog in reader.read_frames():
            data_analog.append(analog)

        # Create an array containing only the raw analog data
        raw_data = []
        
        for i in range(len(data_analog)):
            if i==0:
                raw_data = data_analog[i][2].T
            else:  
                raw_data = np.concatenate((raw_data,data_analog[i][2].T),axis=0)

        self.raw_data = raw_data

    def extract_time(self):
        """ Creates the attribute "time of the DataForcplates class."""

        if self.raw_data is None:
            self.c3d_reader_forceplates()

        # Set forceplate frequency
        FP_FREQUENCY = 1000

        self.time = np.arange(0,len(self.raw_data)/FP_FREQUENCY,1/FP_FREQUENCY)

    def get_time(self):
        try:
            return self.time
        except:
            self.extact_time()
            return self.time

    def extract_data(self):
        if self.raw_data is None:
            self.c3d_reader_forceplates()

        self.raw_data_f1 = self.raw_data[:,0:3]
        self.raw_data_f2 = self.raw_data[:,6:10]
        self.raw_data_f3 = self.raw_data[:,12:15]
        self.raw_data_f4 = self.raw_data[:,18:21]
        self.raw_data_f5 = self.raw_data[:,24:27]
            

    def get_raw_data(self,forceplate_number:int):
        """Creates the attribute "data" to the DataForceplates class.

        Args:
            forceplate_number (int): 1 or 2 or 3 or 4 or 5

        self.data: np.ndarray [3D] (Fx, Fy, Fz)
        """
        if self.raw_data is None:
            self.extract_data()
            
        match forceplate_number:
            case 1:
                data = self.raw_data[:,0:3]
            case 2:
                data = self.raw_data[:,6:10]
            case 3:
                data = self.raw_data[:,12:15]
            case 4:
                data = self.raw_data[:,18:21]
            case 5:
                data = self.raw_data[:,24:27]
        return data
            
    def change_orientation(self):
        """Inverses the orientation of the forceplates."""
        self.data = -self.data

    # def set_zero(self):











if __name__ == "__main__":
    curr_path = getcwd()

    test = DataForceplates(curr_path + "\\examples\\data\\test_poussee_4_fp.c3d", frequency=1000)
    print("Time:")
    print(test.time)

    print("File name:")
    print(test.file_name)

    test.set_timestamp()
    print("Timestamp:")
    print(test.timestamp)

    test.c3d_reader_forceplates()
    print("Raw analog data:")
    print(test.raw_data)
    print("Raw data dimension:")
    print(test.raw_data.shape)

    test.extract_time()
    print("Time:")
    print(test.time)

    test.extract_data()
    
    # test.set_data(1)
    # print("Data:")
    # print(test.data)
    # print("Data dimension")
    # print(test.data.shape)
    # plt.plot(test.time,test.data)
    # plt.show()

    # test.change_orientation()
    # plt.plot(test.time,test.data)
    # plt.show()

    
    resampled_data = test.downsample(200,forceplate_number=1)
    resampled_time = test.downsample(200, time=test.time)
    
    filtered_data_x = test.filter_data(2,20,10,data = resampled_data, column = 0)
    filtered_data_y = test.filter_data(2,20,10,data = resampled_data, column = 1)
    filtered_data_z = test.filter_data(2,20,10,data = resampled_data, column = 2)
    
    plt.plot(test.time,test.raw_data[:,0:3],"-o" ,label = "raw", markersize = 2)
    plt.plot(resampled_time, resampled_data, "-o", label = "resampled", markersize = 2)
    plt.plot(resampled_time, filtered_data_x, "-o", label = "filtered", markersize = 2)
    plt.plot(resampled_time, filtered_data_y, "-o", label = "filtered", markersize = 2)
    plt.plot(resampled_time, filtered_data_z, "-o", label = "filtered", markersize = 2)

    plt.legend()
    plt.show()
