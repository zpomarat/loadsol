import numpy as np
from scipy import signal 


class Data:
    def __init__(self,path:str, frequency:int):
        self.path = path
        self.file_name = (self.path.split("\\"))[-1].split(".")[0]
        self.time = []
        self.frequency = frequency
        self.raw_data = []
        self.downsampled_data = []
        self.filtered_data = []

              
    def downsample(self, final_frequency:int, insole_side = None, data_type = None, forceplate_number = None, time = None):
        
        # Check if arguments are correctly entered
        if insole_side is not None and forceplate_number is not None or data_type is not None and forceplate_number is not None:
            raise AssertionError("Cannot give both forceplate number & insole side / data type at the same time.")
        if time is not None and forceplate_number is not None or time is not None and data_type is not None:
            raise AssertionError("Error in arguments.")

        # Define downsampling ratio
        downsample_ratio = int(self.frequency/final_frequency)

        # If the final frequency is not a multiple of the original frequency, it's too complicated for now.
        if self.frequency % final_frequency != 0:
            raise ValueError("The final frequency is not a multiple of the original frequency.")

        # Get the data 
        if data_type is not None:
            data = self.get_filled_data(insole_side, data_type) # Raw data from loadsol
        if forceplate_number is not None:    
            data = self.get_pre_processed_data(forceplate_number) # Raw data from forceplate
        if time is not None:
            data = self.get_filled_time() 

        # Initialise a list
        downsampled_data = []

        # Create a list with downsampled data
        for itr, value in enumerate(data):
            if itr % downsample_ratio == 0:
                downsampled_data.append(value)

        # Convert list into array
        self.downsampled_data = np.array(downsampled_data)

        return self.downsampled_data
    

    def filter_data(self,order : int, cutoff_frequency : float, sampling_frequency:int, column=2, dimension_1=False, insole_side = None, data_type = None, forceplate_number = None):
        """Apply a butterworth filter with a backward & forward pass.

        Args:
            order (int): order of the filter. Note that with the backward & forward pass, this order will be multiplied by 2.
            cutoff_frequency (float): Frequency where the gain drops to 1/sqrt(2) that of the passband (the -3dB point).
        """

        # Get the data 
        if data_type is not None:
            data = self.downsample(insole_side = insole_side, data_type=data_type, final_frequency = 200) # Raw data from loadsol
        if forceplate_number is not None:    
            data = self.downsample(forceplate_number=forceplate_number, final_frequency=200) # Raw data from forceplate

        nyquist = 0.5 * sampling_frequency
        normal_cutoff = cutoff_frequency / nyquist
        b, a = signal.butter(order, Wn=1, fs = normal_cutoff, analog=False)
        if dimension_1 is False:
            self.filtered_data = signal.filtfilt(b,a,data[:,column])
        else:
            self.filtered_data = signal.filtfilt(b,a,data)
        return self.filtered_data
    
    
    def sync_signals(self,order = 4, cutoff_frequency = 10, sampling_frequency = 1, column = 2, start_sync = 0,dimension_1=False, insole_side = None, data_type = None, forceplate_number = None, time = None):
        if time is not None:
            return self.downsample(final_frequency=200, time= True)[start_sync:]
        if data_type is not None:
            # data = self.get_filled_data(insole_side, data_type)
            data = self.filter_data(order = order, cutoff_frequency= cutoff_frequency, sampling_frequency=sampling_frequency,dimension_1=dimension_1, column = column, insole_side =insole_side, data_type=data_type) # Raw data from forceplate
            return data[start_sync:]
        if forceplate_number is not None:    
            data = self.filter_data(order = order, cutoff_frequency= cutoff_frequency, sampling_frequency=sampling_frequency, column=column,dimension_1=dimension_1,forceplate_number=forceplate_number) # Raw data from forceplate
            return data[start_sync:]
