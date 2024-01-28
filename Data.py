import numpy as np
from scipy import signal 


class Data:
    def __init__(self,path:str, frequency):
        self.path = path
        # self.file_name = (self.path.split("\\"))[-1].split(".")[0]
        self.file_name = (self.path.split("/"))[-1].split(".")[0]

        self.time = []
        self.data = []
        self.frequency = frequency
        self.raw_data = []
        self.downsampled_data = []
        self.filtered_data = []

        
    def filter_data(self, order : int, cutoff_frequency : float): # TODO : It doesn't work now
        """Apply a butterworth filter with a backward & forward pass.

        Args:
            order (int): order of the filter. Note that with the backward & forward pass, this order will be multiplied by 2.
            cutoff_frequency (float): Frequency where the gain drops to 1/sqrt(2) that of the passband (the -3dB point).
        """
        b, a = signal.butter(order, Wn=1, fs=cutoff_frequency, analog=False) # https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.butter.html
        self.filtered_data = signal.filtfilt(b,a,self.downsampled_data) # https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.filtfilt.html
        return self.filtered_data
        
    
    def downsample(self, final_frequency, insole_side = None,data_type = None, forceplate_number = None, time = None):
        
        if not insole_side is None and forceplate_number is not None or data_type is not None and forceplate_number is not None:
            raise AssertionError("Cannot give both forceplate number & insolde / data type at the same time.")
        if not time is None and forceplate_number is not None or time is not None and data_type is not None:
            raise AssertionError("Error in arguments.")

        downsample_ratio = int(self.frequency/final_frequency)
        # If the final frequency is not a multiple of the original frequency, it's too complicated for now.
        if self.frequency % final_frequency != 0:
            raise ValueError("The final frequency is not a multiple of the original frequency.")

        # Get the data 
        if data_type is not None:
            data = self.get_raw_data(insole_side, data_type)
        if forceplate_number is not None:    
            data = self.get_raw_data(forceplate_number)
        if time is not None:
            data = self.get_time()
        self.downsampled_data = []
        for itr, value in enumerate(data):
            if itr % downsample_ratio == 0:
                self.downsampled_data.append(value)
        return self.downsampled_data
        

    def get_raw_data(self):
        """Dummy method
        """
        print("bonjour")
        
    def get_time(self):
        """Dummy method
        """
        print("bonsoir")