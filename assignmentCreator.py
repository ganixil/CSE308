from __future__ import print_function
from six.moves import xrange
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
from database import db_session, GlobalVariables,

#speed = 20
#dayLength = 40

###########################
# Problem Data Definition #
###########################
def create_data_model(_locations):
    """Stores the data for the problem"""
    data = {}
    # Multiply coordinates in block units by the dimensions of an average city block, 114m x 80m,
    # to get location coordinates.
    data["locations"] = _locations
    #data["locations"] = [(l[0] * 114, l[1] * 80) for l in _locations]
    data["num_locations"] = len(data["locations"])
    data["num_vehicles"] = 1
    data["depot"] = 0
    return data
#######################
# Problem Constraints #
#######################
def manhattan_distance(position_1, position_2):
    """Computes the Manhattan distance between two points"""
    return (abs(position_1[0] - position_2[0]) + abs(position_1[1] - position_2[1]))
def create_distance_callback(data):
    """Creates callback to return distance between points."""
    _distances = {}
    for from_node in xrange(data["num_locations"]):
        _distances[from_node] = {}
        for to_node in xrange(data["num_locations"]):
            if from_node == to_node:
                _distances[from_node][to_node] = 0
            else:
                _distances[from_node][to_node] = (manhattan_distance(data["locations"][from_node], data["locations"][to_node]))

    def distance_callback(from_node, to_node):
        """Returns the manhattan distance between the two nodes"""
        return _distances[from_node][to_node]
    
    return distance_callback
def add_distance_dimension(routing, distance_callback):
    """Add Global Span constraint"""
    distance = 'Distance'
    maximum_distance = 3000  # Maximum distance per vehicle.
    routing.AddDimension(distance_callback, 0, maximum_distance, True, distance)
    distance_dimension = routing.GetDimensionOrDie(distance)
    # Try to minimize the max distance among vehicles.
    distance_dimension.SetGlobalSpanCostCoefficient(100)
###########
# Printer #
###########
def print_solution(data, routing, assignment):
    """Print routes on console."""
    total_distance = 0
    for vehicle_id in xrange(data["num_vehicles"]):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        distance = 0
        while not routing.IsEnd(index):
            plan_output += ' {} ->'.format(routing.IndexToNode(index))
            previous_index = index
            index = assignment.Value(routing.NextVar(index))
            distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
        plan_output += ' {}\n'.format(routing.IndexToNode(index))
        plan_output += 'Distance of route: {}m\n'.format(distance)
        print(plan_output)
        total_distance += distance
    print('Total distance of all routes: {}m'.format(total_distance))

def makeAssign(locations, duration):
    
    assignmentCollection = []
    vehicle_id = 0
    globalVar = db_session.query(GlobalVariables).first()
    speed = globalVar.averageSpeed
    dayLength = globalVar.workDayLength

    # Instantiate the data problem.
    while(len(locations) > 1):
        
        data = create_data_model(locations)
        # Create Routing Model
        routing = pywrapcp.RoutingModel(data["num_locations"], data["num_vehicles"], data["depot"])
        # Define weight of each edge
        distance_callback = create_distance_callback(data)
        routing.SetArcCostEvaluatorOfAllVehicles(distance_callback)
        add_distance_dimension(routing, distance_callback)
        # Setting first solution heuristic (cheapest addition).
        search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()
        search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC) # pylint: disable=no-member
        # Solve the problem.
        assignment = routing.SolveWithParameters(search_parameters)
        time = 0
        distance = 0
        #vehicle_id = data["num_vehicles"][0]
        locs = []
        index = routing.Start(0)
        #print(len(locations))
        while not routing.IsEnd(index):
            #print(routing.IndexToNode(index))
            if(routing.IndexToNode(index) != 0):
                #print(routing.IndexToNode(index))
                locs.append(routing.IndexToNode(index))
            if(time >= dayLength):
                break
            previous_index = index
            index = assignment.Value(routing.NextVar(index))
            
            
            distance = routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
            time = time + (distance/speed) + duration
            #print(time)
            
        locElements = []
        #print(locs)
        #print(locations)
        #print(len(locs))
        for x in range(len(locs)):
            locElements.append(locations[locs[x]])
        assignmentCollection.append(locElements)
        for x in range(len(locElements)):
            
            locations.remove(locElements[x])
    
    #print_solution(data, routing, assignment)
    return assignmentCollection
########
# Main #
########
def main():
    locations = \
              [(4,4),
               (2,0), (8,0),
               (6,1), (3,0),
               (5,2), (7,2)]
    assn = makeAssign(locations)
    print(assn)
if __name__ == '__main__':
    main()