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
        self.raw_data = []
        
        for i in range(len(data_analog)):
            if i==0:
                self.raw_data = data_analog[i][2].T
            else:  
                self.raw_data = np.concatenate((self.raw_data,data_analog[i][2].T),axis=0)

        return self.raw_data

    def set_time(self):
        """ Creates the attribute "time of the DataForcplates class."""
        if self.raw_data is None:
            self.c3d_reader_forceplates()
        self.time = np.arange(0,len(self.raw_data)/self.frequency,1/self.frequency)


    def set_data(self,forceplate_number:int):
        """Creates the attribute "data" to the DataForceplates class.

        Args:
            forceplate_number (int): 1 or 2 or 3 or 4 or 5

        self.data: np.ndarray [3D] (Fx, Fy, Fz)
        """
        if self.raw_data is None:
            self.c3d_reader_forceplates()
        match forceplate_number:
            case 1:
                self.data = self.raw_data[:,0:3]
            case 2:
                self.data = self.raw_data[:,6:10]
            case 3:
                self.data = self.raw_data[:,12:15]
            case 4:
                self.data = self.raw_data[:,18:21]
            case 5:
                self.data = self.raw_data[:,24:27]
            
    def change_orientation(self):
        """Inverses the orientation of the forceplates."""
        self.data = -self.data

    # def set_zero(self):










if __name__ == "__main__":
    curr_path = getcwd()

    # test = DataForceplates(curr_path + "\\examples\\data\\test_poussee_4_fp.c3d")
    test = DataForceplates(curr_path + "/examples/data/test_poussee_4_fp.c3d", frequency=1000)

    print("Time:")
    print(test.time)

    print("File name:")
    print(test.file_name)

    test.set_timestamp()
    print("Timestamp:")
    print(test.timestamp)

    raw_data = test.c3d_reader_forceplates()
    print("Raw analog data:")
    print(raw_data)
    print("Raw data dimension:")
    print(raw_data.shape)

    test.set_time()
    print("Time:")
    print(test.time)
    
    test.set_data(1)
    print("Data:")
    print(test.data)
    print("Data dimension")
    print(test.data.shape)
    plt.plot(test.time,test.data)
    plt.show()

    test.change_orientation()
    plt.plot(test.time,test.data)
    plt.show()


