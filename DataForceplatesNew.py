from os import getcwd
from datetime import datetime
import c3d
import numpy as np
from copy import deepcopy
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from scipy import signal

class DataForceplates:
    def __init__(self, path: str, frequency:int):
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
                
    def downsample(self,final_frequency:int):
        """Downsamples data to the final frequency.

        Args:
            final_frequency (int): downsampled frequency 
        """

        if self.pre_processed_data is None:
            self.pre_process_data()

        self.final_frequency = final_frequency

        # Initialise downsampled data
        self.downsampled_data = deepcopy(self.pre_processed_data)

        # Create new time vector based on the final frequency
        t_ds = np.arange(self.pre_processed_data["time"][0],self.pre_processed_data["time"][-1],1/final_frequency)

        for key in self.downsampled_data.keys():

            # Create interpolation function
            if len(self.pre_processed_data.get(key)) != 0:
                f = interp1d(self.pre_processed_data["time"],self.pre_processed_data.get(key))
            
                # Downsample data
                self.downsampled_data[key] = f(t_ds)

        # Add new time vector downsampled
        self.downsampled_data["time"] = t_ds 

    def filter(
        self,
        order: int,
        fcut: int
        ):
        """Apply a butterworth filter with a backward & forward pass.

        Args:
            order (int): order of the filter. Note that with the backward & forward pass, this order will be multiplied by 2.
            fcut (int): Must be smaller than the half of the sampling frequency.
        """

        if self.downsampled_data is None:
            self.downsample()

        # Initialise downsampled data
        self.filtered_data = deepcopy(self.downsampled_data)

        Wn = fcut / (self.final_frequency/2)

        b, a = signal.butter(order, Wn, analog=False)

        # Filter data
        self.filtered_data["fx1"] = signal.filtfilt(b, a, self.filtered_data["fx1"])
        self.filtered_data["fy1"] = signal.filtfilt(b, a, self.filtered_data["fy1"])
        self.filtered_data["fz1"] = signal.filtfilt(b, a, self.filtered_data["fz1"])

        self.filtered_data["fx2"] = signal.filtfilt(b, a, self.filtered_data["fx2"])
        self.filtered_data["fy2"] = signal.filtfilt(b, a, self.filtered_data["fy2"])
        self.filtered_data["fz2"] = signal.filtfilt(b, a, self.filtered_data["fz2"])

        self.filtered_data["fx3"] = signal.filtfilt(b, a, self.filtered_data["fx3"])
        self.filtered_data["fy3"] = signal.filtfilt(b, a, self.filtered_data["fy3"])
        self.filtered_data["fz3"] = signal.filtfilt(b, a, self.filtered_data["fz3"])

        self.filtered_data["fx4"] = signal.filtfilt(b, a, self.filtered_data["fx4"])
        self.filtered_data["fy4"] = signal.filtfilt(b, a, self.filtered_data["fy4"])
        self.filtered_data["fz4"] = signal.filtfilt(b, a, self.filtered_data["fz4"])

        try:
            self.filtered_data["fx5"] = signal.filtfilt(b, a, self.filtered_data["fx5"])
            self.filtered_data["fy5"] = signal.filtfilt(b, a, self.filtered_data["fy5"])
            self.filtered_data["fz5"] = signal.filtfilt(b, a, self.filtered_data["fz5"])

        except:
            self.filtered_data["fx5"] = []
            self.filtered_data["fy5"] = []
            self.filtered_data["fz5"] = []



if __name__ == "__main__":
    curr_path = getcwd()

    test = DataForceplates(curr_path + "\\tests_09_02_24\\data\\poussee_5_L.c3d", frequency=1000)

    # Raw data
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

    # Pre-processed data: orientation changed and zero set
    test.pre_process_data()
    plt.plot(test.pre_processed_data['time'],test.pre_processed_data['fx1'],label='fx1')
    plt.plot(test.pre_processed_data['time'],test.pre_processed_data['fy1'],label='fy1')
    plt.plot(test.pre_processed_data['time'],test.pre_processed_data['fz1'],label='fz1')
    plt.plot(test.pre_processed_data['time'],test.pre_processed_data['fx2'],label='fx2')
    plt.plot(test.pre_processed_data['time'],test.pre_processed_data['fy2'],label='fy2')
    plt.plot(test.pre_processed_data['time'],test.pre_processed_data['fz2'],label='fz2')
    plt.legend()
    plt.title("Pre-processed data")
    plt.figure()

    # Downsample data
    test.downsample(final_frequency=200)
    plt.plot(test.pre_processed_data["time"],test.pre_processed_data["fx1"],'-x',label="filled")   
    plt.plot(test.downsampled_data["time"],test.downsampled_data["fx1"],'-o',label="downsampled")
    plt.legend()
    plt.title("Dowsampled fx1")
    plt.figure()

    # Filtered data
    test.filter(order=4,fcut = 20)
    plt.plot(test.downsampled_data["time"],test.downsampled_data["fx1"],label="downsampled fx1")   
    plt.plot(test.filtered_data["time"],test.filtered_data["fx1"],label="filtered fx1")
    plt.plot(test.downsampled_data["time"],test.downsampled_data["fy1"],label="downsampled fy1")   
    plt.plot(test.filtered_data["time"],test.filtered_data["fy1"],label="filtered fy1")
    plt.plot(test.downsampled_data["time"],test.downsampled_data["fz1"],label="downsampled fz1")   
    plt.plot(test.filtered_data["time"],test.filtered_data["fz1"],label="filtered fz1")
    plt.plot(test.downsampled_data["time"],test.downsampled_data["fx2"],label="downsampled fx2")   
    plt.plot(test.filtered_data["time"],test.filtered_data["fx2"],label="filtered fx2")
    plt.plot(test.downsampled_data["time"],test.downsampled_data["fy2"],label="downsampled fy2")   
    plt.plot(test.filtered_data["time"],test.filtered_data["fy2"],label="filtered fy2")
    plt.plot(test.downsampled_data["time"],test.downsampled_data["fz2"],label="downsampled fz2")   
    plt.plot(test.filtered_data["time"],test.filtered_data["fz2"],label="filtered fz2")
    plt.legend()
    plt.title("Filtered data")
    plt.show()
