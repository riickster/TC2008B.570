import uuid
import logging
from abc import ABC
from math import sqrt
from collections import deque
from scipy.integrate import quad
from scipy.spatial import distance
from scipy.interpolate import interp1d
from Classes.messaging_class import MessageBroker
from numpy import arctan2, unwrap, linspace

class Road(ABC):
    def __init__(self, points):
        self.id = uuid.uuid4()

        self.points = points
        self.vehicles = deque()
        
        self.has_traffic_signal = False
        self.executed_vote = False
        self.voting_started = False

        self.message_broker = MessageBroker()

        self.__set_functions()

    def __set_functions(self):
        self.get_point = interp1d(linspace(0, 1, len(self.points)), self.points, axis=0, fill_value="extrapolate")
        
        headings = unwrap([arctan2(self.points[i+1][1] - self.points[i][1], self.points[i+1][0] - self.points[i][0]) for i in range(len(self.points)-1)])
        if(len(headings) == 1):
            self.get_heading = lambda x: headings[0]
        else:
            self.get_heading = interp1d(linspace(0, 1, len(self.points)-1), headings, axis=0, fill_value="extrapolate")

        logging.basicConfig(filename='simulation.log', encoding='utf-8', level=logging.INFO, format='%(asctime)s | %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    
    def __get_abs(self, t):
        return sqrt(self.__get_dx(t)**2 + self.__get_dy(t)**2)
    
    def __get_dx(self, t):
        return (2*t*(self.end[0]-2 * self.control[0] + self.start[0])) + (2*(self.control[0] - self.start[0]))
    
    def __get_dy(self, t):
        return (2*t*(self.end[1]-2 * self.control[1] + self.start[1])) + (2*(self.control[1] - self.start[1]))
    
    def __get_x(self, t):
        return (t**2 * self.end[0]) + (2*t*(1-t) * self.control[0]) + ((1-t)**2 * self.start[0])
    
    def __get_y(self, t):
        return (t**2 * self.end[1]) + (2*t*(1-t) * self.control[1]) + ((1-t)**2 * self.start[1])
    
    @property
    def __get_traffic_signal_state(self):
        if(self.has_traffic_signal):
            return self.traffic_signal.get_current_cycle[self.traffic_signal_group]
        return True
    
    def __get_t(self, a, target_length, epsilon): 
        def get_interval_value(t):
            integral_value, _ = quad(self.__get_abs, a, t)
            return integral_value
        
        if(get_interval_value(1) < target_length):
            return 1
        
        lower_bound = a
        upper_bound = 1
        mid_point = (lower_bound + upper_bound) / 2.0
        interval_value = get_interval_value(mid_point)

        while(abs(interval_value - target_length) > epsilon):
            if(interval_value < target_length):
                lower_bound = mid_point
            else:
                upper_bound = mid_point
            mid_point = (lower_bound + upper_bound) / 2.0
            interval_value = get_interval_value(mid_point)
        return mid_point
    
    def get_length(self):
        length = 0
        for i in range(len(self.points)-1):
            length += distance.euclidean(self.points[i], self.points[i+1])
        return length
    
    def get_normalized_path(self, CURVE_RESOLUTION=50):
        counter = 0
        normalized_path = [(self.__get_x(0), self.__get_y(0))]
        target_length = self.get_length() / (CURVE_RESOLUTION-1)

        for _ in range(CURVE_RESOLUTION-1):
            t = self.__get_t(counter, target_length, 0.01)
            normalized_path.append((self.__get_x(t), self.__get_y(t)))
            if(t == 1): 
                break
            else:
                counter = t
        return normalized_path
    
    def set_traffic_signal(self, traffic_light, group):
        self.traffic_signal = traffic_light
        self.traffic_signal_group = group
        self.has_traffic_signal = True

    def set_vehicle(self, veh):
        self.vehicles.append(veh)
    
    def update(self, delta_time):
        if(len(self.vehicles) > 0):
            self.vehicles[0].update(None, delta_time, self.message_broker)
            
            for i in range(1, len(self.vehicles)):
                self.vehicles[i].update(self.vehicles[i-1], delta_time, self.message_broker)

            if(self.__get_traffic_signal_state):
                self.vehicles[0].go()
                for vehicle in self.vehicles:
                    vehicle.accelerate()
            else:
                if(self.traffic_signal.voted == False):
                    if(len(self.vehicles) > 2 and self.voting_started == False):
                        self.voting_started = True
                        logging.info(f"Start Voting in Road: {self.id}")
                        self.message_broker.add_message(message={"level": "acction_required", "action": "make_vote"})
                
                if(self.voting_started):
                    votes = []
                    if(len(self.message_broker.read_messages()) > 3):
                        for vote in self.message_broker.read_messages():
                            if(vote.get("action") == "vote"):
                                votes.append(vote.get("vote"))

                        if(votes.count("Change") > votes.count("Maintain")):
                            self.traffic_signal.set_cycle(voted=True)
                            self.voting_started = False
                            self.message_broker.clean_messages()
                            logging.info("Voting Completed! - Result: Change to Green Light")
                        else:
                            self.traffic_signal.voted = True
                            self.voting_started = False
                            self.message_broker.clean_messages()
                            logging.info("Voting Completed! - Result: Maintain Red Light")

                if(self.vehicles[0].x >= self.get_length() - self.traffic_signal.slow_distance):
                    self.vehicles[0].slow(self.traffic_signal.slow_factor*self.vehicles[0]._max_velocity)

                if(self.vehicles[0].x >= self.get_length() - self.traffic_signal.stop_distance and self.vehicles[0].x <= self.get_length() - self.traffic_signal.stop_distance / 2):
                    self.vehicles[0].stop()