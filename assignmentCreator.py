from __future__ import print_function
from six.moves import xrange
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
from database import db_session, GlobalVariables

#speed = 20
#dayLength = 40

###########################
# Problem Data Definition #
###########################
def create_data_model(_locations):
    # store problem data here
    data = {}
    # convert latitude and longitude degrees to miles
    data["locations"] = [(l[0] * 69, l[1] * 69) for l in _locations]

    print(_locations)
    data["num_locations"] = len(data["locations"])
    data["num_vehicles"] = 1
    # specifiy starting location
    data["depot"] = 0
    return data
#######################
# Problem Constraints #
#######################
def manhattan_distance(position_1, position_2):
    # Computes the Manhattan distance between two points
    return (abs(position_1[0] - position_2[0]) + abs(position_1[1] - position_2[1]))
def create_distance_callback(data):
    # Creates callback to return distance between points
    _distances = {}
    for from_node in xrange(data["num_locations"]):
        _distances[from_node] = {}
        for to_node in xrange(data["num_locations"]):
            if from_node == to_node:
                _distances[from_node][to_node] = 0
            else:
                _distances[from_node][to_node] = (manhattan_distance(data["locations"][from_node], data["locations"][to_node]))

    def distance_callback(from_node, to_node):
        # Returns the manhattan distance between the two nodes
        return _distances[from_node][to_node]
    
    return distance_callback
def add_distance_dimension(routing, distance_callback):
    # Add Global Span constraint
    distance = 'Distance'
    maximum_distance = 3000  # Maximum distance per vehicle.
    routing.AddDimension(distance_callback, 0, maximum_distance, True, distance)
    distance_dimension = routing.GetDimensionOrDie(distance)
    # Try to minimize the max distance among vehicles.
    distance_dimension.SetGlobalSpanCostCoefficient(100)

# printing function used for testing
def print_solution(data, routing, assignment):
    # Print route on console
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

# assignment creation function
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
        # inspect the solution to the location order
        while not routing.IsEnd(index):
            if(routing.IndexToNode(index) != 0):
                locs.append(routing.IndexToNode(index))
            # if day length is exceeded don't add another location to the assignment
            if(time >= dayLength):
                break
            previous_index = index
            index = assignment.Value(routing.NextVar(index))
            # get distance between two locations
            distance = routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
            # calculate total time used for that day so far
            time = time + (distance/speed) + duration
        
        # remove used locations from the data set before the next mapping iteration
        locElements = []
        for x in range(len(locs)):
            locElements.append(locations[locs[x]])
        assignmentCollection.append(locElements)
        for x in range(len(locElements)): 
            locations.remove(locElements[x])
    
    return assignmentCollection

# main function used for testing
# def main():
#     locations = \
#               [(4,4),
#                (2,0), (8,0),
#                (6,1), (3,0),
#                (5,2), (7,2)]
#     assn = makeAssign(locations, duration)
#     print(assn)
if __name__ == '__main__':
    main()
