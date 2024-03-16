import uuid
import logging
from abc import ABC
from collections import deque
from scipy.spatial import distance
from scipy.interpolate import interp1d
from Classes.messaging_class import MessageBroker
from numpy import arctan2, unwrap, linspace

#* Defines a Road class that instanciates visually a road segment inside the map that also generates vehicles and adds direction and a destiny
class Road(ABC):
    def __init__(self, points):
        self.id = uuid.uuid4() # Generates a Unique ID for each Road 

        self.points = points
        self.vehicles = deque() # Generates a Double Eneded Queue due to the large ammount of pop and append operations
        
        self.has_traffic_light = False
        self.voting_started = False

        self.message_broker = MessageBroker() # Generates a new Instance of the Class MessageBroker for the road

        self.__set_functions()

    def __set_functions(self):
        self.get_point = interp1d(linspace(0, 1, len(self.points)), self.points, axis=0, fill_value="extrapolate")  # Interpolate points along the saved path

        headings = unwrap([arctan2(self.points[i+1][1] - self.points[i][1], self.points[i+1][0] - self.points[i][0]) for i in range(len(self.points)-1)])  # Calculate headings between consecutive points
        if(len(headings) == 1):  # If there is only one heading (straight line), set it as a constant function
            self.get_heading = lambda x: headings[0]
        else:  # If there are multiple headings (curved road), interpolate between them
            self.get_heading = interp1d(linspace(0, 1, len(self.points)-1), headings, axis=0, fill_value="extrapolate")

        logging.basicConfig(filename='simulation.log', encoding='utf-8', level=logging.INFO, format='%(asctime)s | %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')  # Configure logging format and filename
    
    @property
    def __get_traffic_light_state(self):
        if(self.has_traffic_light):
            return self.traffic_light.get_current_cycle[self.traffic_light_group] # Return the current state of the traffic signal for the assigned group
        return True
    
    def get_length(self):
        length = 0
        for i in range(len(self.points)-1): # Iterate over each pair of consecutive points.
            length += distance.euclidean(self.points[i], self.points[i+1]) # Add the Euclidean distance between consecutive points to the total length
        return length
    
    def set_traffic_light(self, traffic_light, group): # Sets a new Traffic light on the road
        self.traffic_light = traffic_light
        self.traffic_light_group = group
        self.has_traffic_light = True

    def set_vehicle(self, vehicle): # Saves a new Vehicle in the deque
        self.vehicles.append(vehicle)
    
    def update(self, delta_time):
        if(len(self.vehicles) > 0):
            self.vehicles[0].update(None, delta_time, self.message_broker)  # Update the first vehicle in the list without setting a leader

            for i in range(1, len(self.vehicles)):
                self.vehicles[i].update(self.vehicles[i-1], delta_time, self.message_broker)  # Update the remaining vehicles in the list considering the vehicle in front of them as a leader

            if(self.__get_traffic_light_state):  # Check if the traffic light its on green
                self.vehicles[0].go()  # Allow the first vehicle to move
                for vehicle in self.vehicles:  # Accelerate all vehicles
                    vehicle.accelerate()
            else:  # If the traffic signal its on red
                if(self.traffic_light.voted == False):  # Check if the traffic light efectuated a voting
                    if(len(self.vehicles) > 2 and self.voting_started == False):  # Check if there is more than 2 cars to start a voting match
                        self.voting_started = True
                        logging.info(f"Start Voting in Road: {self.id}")
                        self.message_broker.add_message(message={"level": "acction_required", "action": "make_vote"})  # Add a message to the message broker to initiate voting
                
                if(self.voting_started):  # If the voting process is ongoing
                    votes = []
                    if(len(self.message_broker.read_messages()) > 3):  # Check if there are enough votes collected
                        for vote in self.message_broker.read_messages():  # Iterate over the collected votes
                            if(vote.get("action") == "vote"):  # Check if the message is a vote
                                votes.append(vote.get("vote"))  # Append the vote to the list of votes

                        if(votes.count("Change") > votes.count("Maintain")):  # Check the voting result
                            self.traffic_light.set_cycle(voted=True)  # Set the traffic signal cycle to the voted state
                            self.voting_started = False  # Reset the voting status
                            self.message_broker.clean_messages()  # Clean up collected messages
                            logging.info("Voting Completed! - Result: Change to Green Light")  # Log the voting result
                        else:
                            self.traffic_light.voted = True  # Indicate that the signal has been voted to maintain its state
                            self.voting_started = False  # Reset the voting status
                            self.message_broker.clean_messages()  # Clean up collected messages
                            logging.info("Voting Completed! - Result: Maintain Red Light")  # Log the voting result

                if(self.vehicles[0].x >= self.get_length() - self.traffic_light.slow_distance):  # Check if the first vehicle is approaching the slowing point
                    self.vehicles[0].slow(self.traffic_light.slow_factor*self.vehicles[0]._max_velocity)  # Slow down the first vehicle

                if(self.vehicles[0].x >= self.get_length() - self.traffic_light.stop_distance and self.vehicles[0].x <= self.get_length() - self.traffic_light.stop_distance / 2):  # Check if the first vehicle is approaching the stopping point
                    self.vehicles[0].stop()  # Stop the first vehicle
