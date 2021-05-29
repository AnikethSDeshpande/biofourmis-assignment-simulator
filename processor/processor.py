import pandas as pd
from statistics import mean

class Processor:
    def __init__(self, schema=None):
        self.schema = schema
        self.records = []

    def add_record(self, record):
        # after valiating the record
        self.records.append(record)
    
    def get_health_report(self, location, file_name):
        df = pd.DataFrame.from_records(self.records, columns=self.schema.keys())
        df = df.groupby(by=['user_id', lambda x: x//900], axis=0)\
                .agg({
                        'timestamp': [min, max], 
                        'heart_rate': [mean, min, max], 
                        'respiration_rate': [mean]
                    })\
                .reset_index()\
                .drop(columns=['level_1'])
        df.columns = ["_".join(x) for x in df.columns.ravel()]
        columns={
            'timestamp_min': 'seg_start', 
            'timestamp_max': 'seg_end', 
            'heart_rate_mean': 'avg_hr', 
            'heart_rate_min' : 'min_hr',
            'heart_rate_max' : 'max_hr',
            'respiration_rate_mean' : 'avg_rr'
        }
        df.rename(columns=columns, inplace=True)
        # processing
        df.to_csv(f'{location}/{file_name}')

