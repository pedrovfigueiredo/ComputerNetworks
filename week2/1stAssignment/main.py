from models import *
import json


def load_json(filename =''):
    with open(filename, "r") as read_file:
        data = json.load(read_file)

        # Allocating graph
        links = []
        for link in data['links']:
            links.append(Link(link['points'], link['capacity']))

        graph = Graph(data['end-points'], data['switches'], links, data['possible-circuits'])

        # Allocating Simulation
        demands = []
        for demand in data['simulation']['demands']:
            demands.append(Demand(demand['start-time'], demand['end-time'], demand['end-points'], demand['demand']))
        simulation = Simulation(data['simulation']['duration'], demands)
        return graph, simulation


def simulate_network_resource_allocation():
    graph, simulation = load_json('cs1.json')
    # Handling actions based on current time unit
    for t in range(simulation.duration):
        # check states of every demand
        for i in range(len(simulation.demands)):
            demand = simulation.demands[i]

            if t == demand.start_time:
                allocation = graph.allocate_resources(demand.end_points, demand.value)
                if allocation['result']:
                    demand.allocated_circuit = allocation['value']
                    print('Demand', i + 1, 'reservation:', '{}<->{}'.format(demand.end_points[0], demand.end_points[1]),
                          'st:{}'.format(t), '- successful')
                else:
                    print('Demand', i + 1, 'reservation:', '{}<->{}'.format(demand.end_points[0], demand.end_points[1]),
                          'st:{}'.format(t), '- UNSUCCESSFUL')

            if demand.allocated_circuit and t == demand.end_time:
                graph.deallocate_resources(demand.allocated_circuit, demand.value)
                print('Demand', i + 1, 'release:', '{}<->{}'.format(demand.end_points[0], demand.end_points[1]),
                      'st:{}'.format(t))


simulate_network_resource_allocation()
