"""

This script loads, standardize and clean raw .xes files containing event logs, converting them into DFGs (Direcytly-Follows Graphs).

This will enable downstream Process Mining analysis.


"""

import pm4py
import numpy as np
import pandas as pd


        
def load_and_convert_to_dfg(file_path):
    """
    Load an .xes file and convert it to a DFG.
    
    Args:
        file_path (str): Path to the .xes file.
    
    Returns:
        pm4py.objects.conversion.dfg.DFG: The DFG object.
    """
    # Load the event log from the .xes file
    log = pm4py.read_xes(file_path)
    
    # Convert the event log to a DFG
    dfg = pm4py.discover_dfg(log)
    
    return dfg

# Example usage
if __name__ == "__main__":
    file_path = 'C:/Users/aless/Documents/master-thesis-pistone/data/raw/road_traffic/road_fines.xes'
    dfg = load_and_convert_to_dfg(file_path)
    print(dfg)

