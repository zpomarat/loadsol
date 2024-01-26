import numpy as np

class Data:
    def __init__(self,path:str, frequency):
        self.path = path
        self.file_name = (self.path.split("\\"))[-1].split(".")[0]
        self.time = []
        self.data = []
        self.frequency = frequency
        
        
    def filter_data(self, order, cutoff_frequency):
        pass
    
    def downsample(self, final_frequency):
        
        downsample_ratio = int(self.frequency/final_frequency)
        # If the final frequency is not a multiple of the original frequency, it's too complicated for now.
        if self.frequency % final_frequency != 0:
            raise ValueError("The final frequency is not a multiple of the original frequency.")

        self.downsample_data = []
        for itr, value in enumerate(self.data):
            if itr % downsample_ratio == 0:
                self.downsample_data.append(value)
        

    
    