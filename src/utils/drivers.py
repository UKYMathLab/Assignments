import pandas as pd
import numpy as np

class ExamineData:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        print(f'Data\n====\n{data.head}\n')

    def pause(self):
        input('Press any key to continue . . . \n')



class ShowSample:
    def __init__(self, data):
        self.data = data
        idx = np.random.choice(self.data.shape[0])
        print(f'Sample #{idx+1}\n==============\n{self.data.iloc[idx]}\n')

    def pause(self):
        input('Press any key to continue . . . \n')
