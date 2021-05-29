from simulator.simulator import SimpleSimulator
from simulator.simulator_utils import single_layer_schema_validator

from processor.processor import Processor

schema = {
        "user_id" : "string",
        "timestamp" : "number",
        "heart_rate" : "number",
        "respiration_rate" : "number",
        "activity" : "number",
    }

# a SimpleSimulator object 
ss = SimpleSimulator(schema, single_layer_schema_validator)
# run simulation for 7200 seconds (2 hours)
records = ss.run(7200)

# a Processor object
processor = Processor(schema)

# populating records every 2 seconds into processor
i = 0
temp = []
while(i<len(records)):
    temp.append(records[i])
    if i%2==0:
        while(len(temp)!=0):
            record = temp.pop(0)
            processor.add_record(record)
        temp = []
    i+=1

# get report of abc
processor.get_health_report(location='./reports', file_name='abc_health_report.csv')
        
