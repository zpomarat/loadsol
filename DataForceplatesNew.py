import Data
from os import getcwd
from datetime import datetime
import c3d
import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt

class DataForceplates(Data.Data):
    def __init__(self, path: str, frequency:int):
        super().__init__(path, frequency)
        self.path = path
        self.file_name = (self.path.split("\\"))[-1].split(".")[0]
        self.frequency = frequency
        self.raw_data = None
        self.timestamp = None
        self.pre_processed_data = None
        self.resampled_data = None
        self.filtered_data = None

    def c3d_reader_forceplates(self):
        """Reads a c3d file and extracts the raw analog data and time.
        """
        
        ## Extract timestamp
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

        ## Read the c3d file
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
        
        ## Extract time
        time = np.arange(0,len(raw_data)/self.frequency,1/self.frequency)

        ## Extract raw data
        raw_data_f1 = raw_data[:,0:3]
        raw_data_f2 = raw_data[:,6:9]
        raw_data_f3 = raw_data[:,12:15]
        raw_data_f4 = raw_data[:,18:21]
        raw_data_f5 = raw_data[:,24:27]

        ## Fill the dictionnary with raw data
        self.raw_data = {
                "time": time,
                "fx1": raw_data_f1[:,0],
                "fy1": raw_data_f1[:,1],
                "fz1": raw_data_f1[:,2],
                "fx2": raw_data_f2[:,0],
                "fy2": raw_data_f2[:,1],
                "fz2": raw_data_f2[:,2],
                "fx3": raw_data_f3[:,0],
                "fy3": raw_data_f3[:,1],
                "fz3": raw_data_f3[:,2],
                "fx4": raw_data_f4[:,0],
                "fy4": raw_data_f4[:,1],
                "fz4": raw_data_f4[:,2]}
        try:
            self.raw_data["fx5"] = raw_data_f5[:,0]
        except:
            self.raw_data["fx5"] = []
        try:
            self.raw_data["fy5"] = raw_data_f5[:,0]
        except:
            self.raw_data["fy5"] = []
        try:
            self.raw_data["fz5"] = raw_data_f5[:,0]
        except:
            self.raw_data["fz5"] = []

    def pre_process_data(self):
        """Inverses the orientation of the forceplates and set values to zero.
        """

        if self.raw_data is None:
            self.c3d_reader_forceplates()

        # Initialise pre processed data
        self.pre_processed_data = deepcopy(self.raw_data)

        # Change orientation
        self.pre_processed_data["fx1"] = -self.pre_processed_data["fx1"]
        self.pre_processed_data["fy1"] = -self.pre_processed_data["fy1"]
        self.pre_processed_data["fz1"] = -self.pre_processed_data["fz1"]

        self.pre_processed_data["fx2"] = -self.pre_processed_data["fx2"]
        self.pre_processed_data["fy2"] = -self.pre_processed_data["fy2"]
        self.pre_processed_data["fz2"] = -self.pre_processed_data["fz2"]

        self.pre_processed_data["fx3"] = -self.pre_processed_data["fx3"]
        self.pre_processed_data["fy3"] = -self.pre_processed_data["fy3"]
        self.pre_processed_data["fz3"] = -self.pre_processed_data["fz3"]

        self.pre_processed_data["fx4"] = -self.pre_processed_data["fx4"]
        self.pre_processed_data["fy4"] = -self.pre_processed_data["fy4"]
        self.pre_processed_data["fz4"] = -self.pre_processed_data["fz4"]

        try:
            self.pre_processed_data["fx5"] = -self.pre_processed_data["fx5"]
            self.pre_processed_data["fy5"] = -self.pre_processed_data["fy5"]
            self.pre_processed_data["fz5"] = -self.pre_processed_data["fz5"]
        except:
            self.pre_processed_data["fx5"] = []
            self.pre_processed_data["fy5"] = []
            self.pre_processed_data["fz5"] = []

        # Set values to zero
        # Mean values of force on the 1000 first samples
        mean_fx1 = np.mean(self.pre_processed_data["fx1"][0:1000])
        mean_fy1 = np.mean(self.pre_processed_data["fy1"][0:1000])
        mean_fz1 = np.mean(self.pre_processed_data["fz1"][0:1000])

        mean_fx2 = np.mean(self.pre_processed_data["fx2"][0:1000])
        mean_fy2 = np.mean(self.pre_processed_data["fy2"][0:1000])
        mean_fz2 = np.mean(self.pre_processed_data["fz2"][0:1000])
        
        mean_fx3 = np.mean(self.pre_processed_data["fx3"][0:1000])
        mean_fy3 = np.mean(self.pre_processed_data["fy3"][0:1000])
        mean_fz3 = np.mean(self.pre_processed_data["fz3"][0:1000])
        
        mean_fx4 = np.mean(self.pre_processed_data["fx4"][0:1000])
        mean_fy4 = np.mean(self.pre_processed_data["fy4"][0:1000])
        mean_fz4 = np.mean(self.pre_processed_data["fz4"][0:1000])

        try: 
            mean_fx5 = np.mean(self.pre_processed_data["fx5"][0:1000])
            mean_fy5 = np.mean(self.pre_processed_data["fy5"][0:1000])
            mean_fz5 = np.mean(self.pre_processed_data["fz5"][0:1000])
        except:
            mean_fx5 = []
            mean_fy5 = []
            mean_fz5 = []
        
        # Substract the mean value to the data
        self.pre_processed_data["fx1"][:] -= mean_fx1
        self.pre_processed_data["fy1"][:] -= mean_fy1
        self.pre_processed_data["fz1"][:] -= mean_fz1

        self.pre_processed_data["fx2"][:] -= mean_fx2
        self.pre_processed_data["fy2"][:] -= mean_fy2
        self.pre_processed_data["fz2"][:] -= mean_fz2

        self.pre_processed_data["fx3"][:] -= mean_fx3
        self.pre_processed_data["fy3"][:] -= mean_fy3
        self.pre_processed_data["fz3"][:] -= mean_fz3

        self.pre_processed_data["fx4"][:] -= mean_fx4
        self.pre_processed_data["fy4"][:] -= mean_fy4
        self.pre_processed_data["fz4"][:] -= mean_fz4

        try:
            self.pre_processed_data["fx5"][:] -= mean_fx5
            self.pre_processed_data["fy5"][:] -= mean_fy5
            self.pre_processed_data["fz5"][:] -= mean_fz5
        except:
            self.pre_processed_data["fx5"] = []
            self.pre_processed_data["fy5"] = []
            self.pre_processed_data["fz5"] = []
                

            


if __name__ == "__main__":
    curr_path = getcwd()

    test = DataForceplates(curr_path + "\\tests_09_02_24\\data\\poussee_5_L.c3d", frequency=1000)

    test.c3d_reader_forceplates()
    plt.plot(test.raw_data['time'],test.raw_data['fx1'],label='fx1')
    plt.plot(test.raw_data['time'],test.raw_data['fy1'],label='fy1')
    plt.plot(test.raw_data['time'],test.raw_data['fz1'],label='fz1')
    plt.plot(test.raw_data['time'],test.raw_data['fx2'],label='fx2')
    plt.plot(test.raw_data['time'],test.raw_data['fy2'],label='fy2')
    plt.plot(test.raw_data['time'],test.raw_data['fz2'],label='fz2')
    plt.legend()
    plt.title("Raw data")
    plt.figure()

    test.pre_process_data()
    plt.plot(test.pre_processed_data['time'],test.pre_processed_data['fx1'],label='fx1')
    plt.plot(test.pre_processed_data['time'],test.pre_processed_data['fy1'],label='fy1')
    plt.plot(test.pre_processed_data['time'],test.pre_processed_data['fz1'],label='fz1')
    plt.plot(test.pre_processed_data['time'],test.pre_processed_data['fx2'],label='fx2')
    plt.plot(test.pre_processed_data['time'],test.pre_processed_data['fy2'],label='fy2')
    plt.plot(test.pre_processed_data['time'],test.pre_processed_data['fz2'],label='fz2')
    plt.legend()
    plt.title("Pre-processed data")
    plt.show()

