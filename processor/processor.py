# third party imports
import pandas as pd

# built in imports
from statistics import mean
import datetime


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

        df['dt'] = df.timestamp.apply(lambda x: datetime.datetime.fromtimestamp(x))
        dt = df.dt
        min_d = dt[0].to_pydatetime()
        max_d = list(dt)[-1].to_pydatetime()
        user_id = df.user_id[0]

        min_d = min_d.replace(microsecond=0, second=0, minute=0)
        max_d = max_d.replace(microsecond=59, second=59, minute=59)
        
        new_index=pd.date_range(min_d.isoformat(), max_d.isoformat(), freq='s')

        df=df.set_index('dt')
        df=df.reindex(new_index).fillna(0)
        df=df.rename_axis('dt').reset_index()
        df['timestamp']=df.dt.apply(lambda x: int(datetime.datetime.timestamp(x)))
        df=df.sort_values('timestamp')
        df['user_id'] = user_id

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
        df['datetime_seg_start'] = df.seg_start.apply(lambda x: datetime.datetime.fromtimestamp(x))
        df['datetime_seg_end'] = df.seg_end.apply(lambda x: datetime.datetime.fromtimestamp(x))
        df = df.sort_values('seg_start')
        df.to_csv(f'{location}/{file_name}')
