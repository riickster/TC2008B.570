import uuid
import random
import logging
import numpy as np

class Vehicle:
    def __init__(self, config={}):
        self.__set_default_config()
        self.__init_properties()

        for attr, val in config.items():
            setattr(self, attr, val)

        
    def __set_default_config(self):    
        
        self.id = uuid.uuid4()

        self.length = 4
        
        self.s0 = 4
        self.max_velocity = 16.6
        self.max_acceleration = 2.88
        self.b_max = 4.61

        self.path = []
        self.current_road_index = 0

        self.x = 0
        self.velocity = 0
        self.acceleration = 0
        self.stopped = False

        self.color = list(np.random.choice(range(256), size=3))

    def __init_properties(self):
        self.sqrt_ab = 2*np.sqrt(self.max_acceleration*self.b_max)
        self._max_velocity = self.max_velocity

        logging.basicConfig(filename='simulation.log', encoding='utf-8', level=logging.INFO, format='%(asctime)s | %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

    def update(self, lead, delta_time, message_broker):

        try:
            voting_request = message_broker.read_messages()[0]
            if(voting_request.get("action") == "make_vote"):
                message_broker.add_message({"level": "info", "action": "vote", "vote": self.__generate_vote()})
        except:
            pass
        
        alpha = 0

        if((self.velocity + self.acceleration * delta_time) < 0):
            self.x -= (1/2 * self.velocity * self.velocity / self.acceleration)
            self.velocity = 0
        else:
            self.velocity += self.acceleration * delta_time
            self.x += (self.velocity * delta_time) + (self.acceleration * delta_time * delta_time / 2)
        
        if(lead):
            delta_x = lead.x - self.x - lead.length
            delta_v = self.velocity - lead.velocity

            alpha = (self.s0 + max(0, self.velocity + delta_v*self.velocity/self.sqrt_ab)) / delta_x

        self.acceleration = self.max_acceleration * (1-(self.velocity/self.max_velocity)**4 - alpha**2)

        if(self.stopped): 
            self.acceleration = -self.b_max * self.velocity / self.max_velocity

    def __generate_vote(self):
        choice = random.choice(["Change", "Maintain"])
        logging.info(f"Car {self.id} Voted: {choice}")
        return choice
        
    def stop(self):
        self.stopped = True

    def go(self):
        self.stopped = False

    def slow(self, velocity):
        self.max_velocity = velocity

    def accelerate(self):
        self.max_velocity = self._max_velocity