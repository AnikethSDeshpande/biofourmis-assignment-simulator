# module imports
import simulator.simulator_constants as sc

# built in imports
import datetime
import random


class Simulator:

    def __init__(self, schema=None, schema_validator=None):
        self.simulator_data = {}
        self.schema = schema
        self.schema_validator = schema_validator

    def construct_simulator_schema(self):
        '''
            method to populate self.simulator_data.
            - checks for schema_validator
            - validate schema
            - populates simulated data with default value
        '''
        if self.schema_validator is None:
            return
        
        if not self.schema_validator(self.schema, sc.SINGLE_LAYER_SIMULATOR_SUPPORTED_TYPES):
            return
        
        for attribute, attribute_type in self.schema.items():
            self.simulator_data[attribute] = sc.SUPPORTED_DEFAULT_VALUES.get(attribute_type)
    
    def run(self):
        pass


class SimpleSimulator(Simulator):

    def __init__(self, schema, schema_validator):
        super().__init__(schema=schema, schema_validator=schema_validator)
        self.construct_simulator_schema()

    def run(self, interval_seconds):
        '''
            generates customers wearable device records for two hours
            each second a new record is generated
            returns the records
        '''

        start = datetime.datetime.utcnow()
        start_time = int(start.timestamp())
        end_time = int((start + datetime.timedelta(seconds=interval_seconds)).timestamp())
        
        current_time = start_time

        records = []
        i=0
        while current_time < end_time:
            current_time = int((start + datetime.timedelta(seconds=i)).timestamp())
            i += 1
            record = {
                "user_id": "abc",
                "timestamp": current_time,
                "heart_rate": random.randint(60,100),
                "respiration_rate": random.randint(12,16),
                "activity": random.randint(0,10)
            }
            records.append(record)
        
        return records
