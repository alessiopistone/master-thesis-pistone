class dfg:
    def __init__(self, source):
        self.source = source
        

class ProcessGraph:
    def __init__(self, dfg, objects, events, graph):
        self.dfg = dfg
        self.objects = objects 
        self.events = events
        self.graph = graph

    

    