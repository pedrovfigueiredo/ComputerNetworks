class Link:
    def __init__(self, points=[], capacity=0):
        self.points = points
        self.capacity = capacity


class Graph:
    def __init__(self, end_points=[], switches=[], links=[], possible_circuits=[]):
        self.end_points = end_points
        self.switches = switches
        self.links = links
        # Sorts incoming array of possible circuits its size (shorter circuits on top)
        self.possible_circuits = sorted(possible_circuits, key=len)

    def allocate_resources(self, end_points, value) -> {str:bool, str: []}:
        for circuit in self.possible_circuits:
            if circuit[0] == end_points[0] and self.__is_circuit_capable(circuit, value):
                for i in range(len(circuit) - 1):
                    link = self.__get_link([circuit[i], circuit[i+1]])
                    link.capacity -= value
                return {'result': True, 'value': circuit}
        return {'result': False, 'value': None}

    def deallocate_resources(self, circuit, value):
        for i in range(len(circuit) - 1):
            link = self.__get_link([circuit[i], circuit[i+1]])
            link.capacity += value

    # Checks if circuit can handle the given traffic
    def __is_circuit_capable(self, circuit, traffic_value) -> bool:
        for i in range(len(circuit) - 1):
            link = self.__get_link([circuit[i], circuit[i+1]])
            if (not link) or link.capacity < traffic_value:
                return False
        return True

    # Returns the link, if found, or False otherwise
    def __get_link(self, points: []):
        return next((x for x in self.links if x.points == [points[0], points[1]]), False)


class Demand:
    allocated_circuit = None

    def __init__(self, start_time=0, end_time=0, end_points=[], value=0):
        self.start_time = start_time
        self.end_time = end_time
        self.end_points = end_points
        self.value = value


class Simulation:
    def __init__(self, duration=0, demands=[]):
        self.duration = duration
        self.demands = demands
