# module imports
import simulator.simulator as sim
import simulator.simulator_utils as sim_utils
import processor.processor as proc

# third party imports
import pandas as pd

# built in imports
import warnings
warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)


schema = {
        "user_id" : "string",
        "timestamp" : "number",
        "heart_rate" : "number",
        "respiration_rate" : "number",
        "activity" : "number",
    }


if __name__ == '__main__':

    # a SimpleSimulator object
    ss = sim.SimpleSimulator(schema, sim_utils.single_layer_schema_validator)

    # run simulation for 7200 seconds (2 hours)
    records = ss.run(7200)

    # a Processor object
    processor = proc.Processor(schema)

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

    # get report for abc (customer)
    processor.get_health_report(location='./reports', file_name='abc_health_report.csv')

    print('Successfully generated report for the customer. \nPlease visit the reports directory to access the file.')
