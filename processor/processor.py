# third party imports
import pandas as pd

# built in imports
from statistics import mean


class Processor:

    def __init__(self, schema=None):
        self.schema = schema
        self.records = []

    def add_record(self, record):
        '''
            add a record to self.records
        '''
        # after valiating the record (to be implemented)
        self.records.append(record)

    def get_health_report(self, location, file_name):
        '''
            prepares a dataframe from self.records
            performs various data manipulation operations
            saves the customers report in the reports directory
        '''

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

        df.to_csv(f'{location}/{file_name}')
