import Data
from os import getcwd
from datetime import datetime
import c3d
import numpy as np
import matplotlib.pyplot as plt


class DataForceplates(Data.Data):
    def __init__(self, path: str, frequency:int):
        super().__init__(path, frequency)
        # Define some attributs as None only to see whether specific methods have already been called or not.
        self.raw_data = None
        self.raw_data_f1 = None
        self.pre_processed_data_f1 = None


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
        """ Creates the attribute "time" of the DataForcplates class."""

        if self.raw_data is None:
            self.c3d_reader_forceplates()

        # Set forceplate frequency
        FP_FREQUENCY = 1000

        self.time = np.arange(0,len(self.raw_data)/FP_FREQUENCY,1/FP_FREQUENCY)


    def get_time(self):
        """Returns the raw time vector.
        """
        try:
            return self.time
        except:
            self.extract_time()
            return self.time


    def extract_data(self):
        """Creates specific attributes "data" to the DataForceplates class.
        """

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
        if self.raw_data_f1 is None:
            self.extract_data()
            
        match forceplate_number:
            case 1:
                raw_data = self.raw_data[:,0:3]
            case 2:
                raw_data = self.raw_data[:,6:10]
            case 3:
                raw_data = self.raw_data[:,12:15]
            case 4:
                raw_data = self.raw_data[:,18:21]
            case 5:
                raw_data = self.raw_data[:,24:27]
        return raw_data
            
    def change_orientation(self):
        """Inverses the orientation of the forceplates."""

        # Initialise pre processed data
        self.pre_processed_data_f1 = self.get_raw_data(1)
        self.pre_processed_data_f2 = self.get_raw_data(2)
        self.pre_processed_data_f3 = self.get_raw_data(3)
        self.pre_processed_data_f4 = self.get_raw_data(4)
        self.pre_processed_data_f5 = self.get_raw_data(5)

        # Change orientation
        self.pre_processed_data_f1 = -self.pre_processed_data_f1
        self.pre_processed_data_f2 = -self.pre_processed_data_f2
        self.pre_processed_data_f3 = -self.pre_processed_data_f3
        self.pre_processed_data_f4 = -self.pre_processed_data_f4
        self.pre_processed_data_f5 = -self.pre_processed_data_f5

        # Redefine time attribut
        self.pre_processed_time = self.time     ## TODO: move to set_zero

    def set_zero(self):
        if self.pre_processed_data_f1 is None:
            self.change_orientation()

        # Mean values of force on the 1000 first samples
        mean_fx1 = np.mean(self.pre_processed_data_f1[0:1000,0])
        mean_fy1 = np.mean(self.pre_processed_data_f1[0:1000,1])
        mean_fz1 = np.mean(self.pre_processed_data_f1[0:1000,2])

        mean_fx2 = np.mean(self.pre_processed_data_f2[0:1000,0])
        mean_fy2 = np.mean(self.pre_processed_data_f2[0:1000,1])
        mean_fz2 = np.mean(self.pre_processed_data_f2[0:1000,2])

        mean_fx3 = np.mean(self.pre_processed_data_f3[0:1000,0])
        mean_fy3 = np.mean(self.pre_processed_data_f3[0:1000,1])
        mean_fz3 = np.mean(self.pre_processed_data_f3[0:1000,2])

        mean_fx4 = np.mean(self.pre_processed_data_f4[0:1000,0])
        mean_fy4 = np.mean(self.pre_processed_data_f4[0:1000,1])
        mean_fz4 = np.mean(self.pre_processed_data_f4[0:1000,2])

        mean_fx5 = np.mean(self.pre_processed_data_f5[0:1000,0])
        mean_fy5 = np.mean(self.pre_processed_data_f5[0:1000,1])
        mean_fz5 = np.mean(self.pre_processed_data_f5[0:1000,2])

        # Substract the mean value to the data
        self.pre_processed_data_f1[:,0] -= mean_fx1
        self.pre_processed_data_f1[:,1] -= mean_fy1
        self.pre_processed_data_f1[:,2] -= mean_fz1

        self.pre_processed_data_f2[:,0] -= mean_fx2
        self.pre_processed_data_f2[:,1] -= mean_fy2
        self.pre_processed_data_f2[:,2] -= mean_fz2

        self.pre_processed_data_f3[:,0] -= mean_fx3
        self.pre_processed_data_f3[:,1] -= mean_fy3
        self.pre_processed_data_f3[:,2] -= mean_fz3

        self.pre_processed_data_f4[:,0] -= mean_fx4
        self.pre_processed_data_f4[:,1] -= mean_fy4
        self.pre_processed_data_f4[:,2] -= mean_fz4

        self.pre_processed_data_f5[:,0] -= mean_fx5
        self.pre_processed_data_f5[:,1] -= mean_fy5
        self.pre_processed_data_f5[:,2] -= mean_fz5
        
        
    def get_pre_processed_data(self,forceplate_number:int):
        """Returns specific attributes "pre_processed_data" of the DataForceplates class."""

        if self.pre_processed_data_f1 is None:
            self.set_zero()

        # Get pre-processed data
        match forceplate_number:
            case 1:
                pre_processed_data = self.pre_processed_data_f1
            case 2:
                pre_processed_data = self.pre_processed_data_f2
            case 3:
                pre_processed_data = self.pre_processed_data_f3
            case 4:
                pre_processed_data = self.pre_processed_data_f4
            case 5:
                pre_processed_data = self.pre_processed_data_f5
        return pre_processed_data
    
    def get_pre_processed_time(self):
        """Returns the pre-processed time vector.
        """
        try:
            return self.pre_processed_time
        except:
            self.pre_processed_time = self.get_time()       ## TODO: change to set_zero
            return self.pre_processed_time













if __name__ == "__main__":
    curr_path = getcwd()

    test = DataForceplates(curr_path + "\\examples\\data\\test_poussee_1.c3d", frequency=1000)
    print(f"Time: {test.time}")

    print(f"File name: {test.file_name}")

    test.set_timestamp()
    print(f"Timestamp: {test.timestamp}")

    test.c3d_reader_forceplates()
    print(f"Raw analog data: {test.raw_data}")
    print(f"Raw data dimension: {test.raw_data.shape}")

    test.extract_time()
    print(f"Time: {test.time}")

    test.extract_data()
    
    fp1 = test.get_raw_data(1)
    print(f"Data forceplate 1: {fp1}")
    print(f"Data dimension: {fp1.shape}")
    plt.plot(test.time,fp1)
    plt.show()

    test.change_orientation()
    plt.plot(test.time,test.pre_processed_data_f1)
    plt.show()

    plt.plot(test.time,test.pre_processed_data_f1,label="before zero setting")
    test.set_zero()
    plt.plot(test.time,test.pre_processed_data_f1,label="after zero setting")
    plt.legend()
    plt.show()

    resampled_data_fp1 = test.downsample(200,forceplate_number=1)
    resampled_time = test.downsample(200, time=test.time)
    
    filtered_data_x_1 = test.filter_data(2,20,10,data = resampled_data_fp1, column = 0)
    filtered_data_y_1 = test.filter_data(2,20,10,data = resampled_data_fp1, column = 1)
    filtered_data_z_1 = test.filter_data(2,20,10,data = resampled_data_fp1, column = 2)
    
    plt.plot(test.time,test.raw_data[:,0:3],"-o" ,label = "raw", markersize = 2)
    plt.plot(resampled_time, resampled_data_fp1, "-o", label = "resampled", markersize = 2)
    plt.plot(resampled_time, filtered_data_x_1, "-o", label = "filtered", markersize = 2)
    plt.plot(resampled_time, filtered_data_y_1, "-o", label = "filtered", markersize = 2)
    plt.plot(resampled_time, filtered_data_z_1, "-o", label = "filtered", markersize = 2)

    plt.legend()
    plt.show()
