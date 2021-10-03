import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn import preprocessing


class DataReader():
    df = None
    train_stats = None
    data_array = None
    fin_risk = None

   
    def pre_data(self):
        df = pd.read_csv("train_data.csv")  # [162634, 103]
        encoder = preprocessing.LabelEncoder()
        df['c_object_type'] = encoder.fit_transform(df['c_object_type'])      
        df.fillna(value=0, inplace=True)
        self.df = df
        return df

    
    def get_risk(self):
        df = self.pre_data()
        fin_risk = np.zeros(13154)        
        fin_timetotca = np.zeros(13154)       
        event_id = 0
        for index, row in df.iterrows():        
            if row['event_id'] == event_id:     
                fin_risk[event_id] = row['risk']
                fin_timetotca[event_id] = row['time_to_tca']
            else:
                event_id = event_id + 1
                fin_risk[event_id] = row['risk']
                fin_timetotca[event_id] = row['time_to_tca']
        self.fin_risk = fin_risk
        self.fin_timetotca = fin_timetotca
        return fin_risk, fin_timetotca

    
    def get_stats(self):
        df = self.pre_data()
        event = df.pop('event_id')
        risk = df.pop('risk')
        train_stats = df.describe()
        self.train_stats = train_stats.transpose()
        df['event_id'] = event
        df['risk'] = risk
        return self.train_stats

    
    def norm(self, x):
        train_stats = self.get_stats()
        return (x - train_stats['mean']) / train_stats['std']

    def get_norm_data(self):
        self.get_stats()
        df = self.df
        event = df.pop('event_id')
        risk = df.pop('risk')
        df = self.norm(df)
        df['risk'] = risk
        df['event_id'] = event
        return df

    
    def get_data_array(self):
        df = self.get_norm_data()
        fin_risk, final_timetotca = self.get_risk()
        final_risk = np.zeros(7293)     
        test_risk = np.zeros(1902)      
        data_array = []
        test_array = []
        temp_vector = []
        event_id = 0
        n = 0
        k = 0
        k1 = 0
        for index, row in df.iterrows():
            if row['event_id'] < 3000:       
                if row['event_id'] == event_id:
                    if final_timetotca[event_id] < 1:      
                        if row['time_to_tca'] > -0.671:        
                            temp_vector.append(row.values[:-1])
                            n = n + 1
                else:
                    if n > 0:   
                        if n < 25:
                            for i in range(25 - n):      
                                temp_vector.append(np.zeros(102, ))
                        test_array.append(np.array(temp_vector))
                        test_risk[k1] = fin_risk[event_id]    
                        k1 = k1+1
                    temp_vector = []
                    event_id = event_id + 1
                    n = 0
                    if final_timetotca[event_id] < 1:   
                        if row['time_to_tca'] > -0.671:
                            temp_vector.append(row.values[:-1])
                            n = n + 1
            else:
                if row['event_id'] == event_id:     
                    if final_timetotca[event_id] < 1:
                        temp_vector.append(row.values[:-1])
                        n = n + 1
                else:
                    if n > 0:
                        if n < 25:
                            for i in range(25 - n):
                                temp_vector.append(np.zeros(102, ))
                        data_array.append(np.array(temp_vector))
                        final_risk[k] = fin_risk[event_id]
                        k = k+1
                    temp_vector = []
                    event_id = event_id + 1
                    n = 0
                    if final_timetotca[event_id] < 1:
                        temp_vector.append(row.values[:-1])
                        n = n + 1

        test_array = np.array(test_array)
        data_array = np.array(data_array)
        print(data_array.shape,  test_array.shape)
        return data_array, final_risk, test_array, test_risk

    
    def get_shuffle_data(self):
        data_array, fin_risk, test_array, test_risk = self.get_data_array()
        index = np.array(range(7293))
        np.random.shuffle(index)
        data_array = data_array[index]
        fin_risk = fin_risk[index]
        return data_array, fin_risk

