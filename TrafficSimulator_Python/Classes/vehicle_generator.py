from numpy.random import randint
from Classes.vehicle_class import Vehicle

#* Defines the VehicleGenerator Class that generates vehicles inside specifies roads
class VehicleGenerator:
    def __init__(self, config={}):
        self.__set_default_config()  # Set default configuration values.
        
        # Set configuration values passed as arguments.
        for attr, val in config.items():
            setattr(self, attr, val)

        self.__init_properties()  # Initialize properties for the vehicle generator.

    def __set_default_config(self):
        self.vehicles = [(1, {})]  # Define the types of vehicles to generate and their respective weights.
        self.vehicle_rate = 22  # Define the rate at which vehicles are generated.
        self.last_added_time = 0

    def __init_properties(self):  # Initialize additional properties of the vehicle generator.
        self.upcoming_vehicle = self.__generate_vehicle()  # Generate the first upcoming vehicle.

    def __generate_vehicle(self):  # Generate a new vehicle based on the configured types and weights.
        total = sum(pair[0] for pair in self.vehicles)  # Calculate the total weight of vehicle types.
        r = randint(1, total+1)  # Generate a random value between 1 and the total weight.
        for weight, config in self.vehicles:
            r -= weight  # Subtract the weight of the current vehicle type.
            if r <= 0:
                return Vehicle(config)  # Return a new instance of the selected vehicle type.

    def update(self, simulation):
        if (simulation.time - self.last_added_time) >= (60 / self.vehicle_rate): # Check if it's time to add a new vehicle based on the configured vehicle rate.
            road = simulation.roads[self.upcoming_vehicle.path[0]]  # Get the road where the vehicle will be added.
            if len(road.vehicles) == 0 or road.vehicles[-1].x > self.upcoming_vehicle.s0 + self.upcoming_vehicle.length:
                simulation.set_vehicles(self.upcoming_vehicle)  # Add the upcoming vehicle to the simulation.
                self.last_added_time = simulation.time  # Update the time of the last added vehicle.
            self.upcoming_vehicle = self.__generate_vehicle()  # Generate the next upcoming vehicle.

            simulation.websocket_sender({"action": "add_vehicle", "data": {"id": str(self.upcoming_vehicle.id)}})
