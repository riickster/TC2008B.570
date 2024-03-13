from numpy.random import randint
from Classes.vehicle_class import Vehicle

class VehicleGenerator:
    def __init__(self, config={}):
        self.__set_default_config()

        for attr, val in config.items():
            setattr(self, attr, val)

        self.__init_properties()

    def __set_default_config(self):
        self.vehicles = [(1, {})]
        self.vehicle_rate = 22
        self.last_added_time = 0

    def __init_properties(self):
        self.upcoming_vehicle = self.__generate_vehicle()

    def __generate_vehicle(self):
        total = sum(pair[0] for pair in self.vehicles)
        r = randint(1, total+1)
        for weight, config in self.vehicles:
            r -= weight
            if(r <= 0):
                return Vehicle(config)

    def update(self, simulation):
        if((simulation.time - self.last_added_time) >= (60 / self.vehicle_rate)):
            road = simulation.roads[self.upcoming_vehicle.path[0]]      
            if(len(road.vehicles) == 0 or road.vehicles[-1].x > self.upcoming_vehicle.s0 + self.upcoming_vehicle.length):
                simulation.set_vehicles(self.upcoming_vehicle)
                self.last_added_time = simulation.time
            self.upcoming_vehicle = self.__generate_vehicle()
            simulation.websocket_sender({"action": "add_vehicle", "data": {"id": str(self.upcoming_vehicle.id)}})
