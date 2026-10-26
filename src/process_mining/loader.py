"""

This script loads, standardize and clean raw .xes files containing event logs, converting them into DFGs (Direcytly-Follows Graphs).

This will enable downstream Process Mining analysis.


"""

import pm4py
import numpy as np
import pandas as pd


class EventLog:
    def __inint__(self, identifier, case, timestamps, activity):
        self.identifier = str
        self.case = str
        self.timestamps = str
        self.activity = str 
        
        
log = pm4py.read_xes('C:/Users/aless/Documents/master-thesis-pistone/data/raw/road_traffic/road_fines.xes')

print(log.head())

