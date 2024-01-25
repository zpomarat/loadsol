import numpy as np

class Data:
    def __init__(self,path:str):
        self.path = path
        self.file_name = (self.path.split("\\"))[-1].split(".")[0]
        self.time = []
        self.data = []


    