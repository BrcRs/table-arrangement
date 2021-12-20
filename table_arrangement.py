class TAProblem:
    types = ["maxmin", "maxsum"]
    def __init__(self):
        self.guests = dict()
        self.topology = dict()
        self.constraints = dict()
        self.function = ""

    def add_guest(self, name, alias):
        self.guests[alias] = name
        self.constraints[alias] = dict()

    def add_guests(self, aliases: dict):
        for a in aliases.keys():
            self.add_guest(aliases[a], a)

    def add_edge(self, first, second):
        if first not in self.topology.keys():
            self.topology[first] = set()

        if second not in self.topology.keys():
            self.topology[second] = set()
        
        self.topology[first].add(second)
        self.topology[second].add(first)
    
    def add_constraint(self, guest, other, value):
        # other could be a seat or a guest
        self.constraints[guest][other] = value

    def set_opt_function(self, fun):
        self.function = fun