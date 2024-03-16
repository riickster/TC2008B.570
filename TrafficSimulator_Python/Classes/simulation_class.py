import websocket
from Classes.road_class import Road
from Classes.curved_road_class import CurvedRoad
from Classes.traffic_light_class import TrafficLight

#* Generates the Simulation Class that coordinates all the components of the simulation, including the agents and the environment
class Simulation:
    def __init__(self):
        self.time = 0.0
        self.delta_time = 1/60

        self.roads = []
        self.traffic_lights = []

        self.vehicles = {}
        self.vehicle_generator = []

        self.__generate_websocket()  # Call the method to set up websocket connection
    
    def __generate_websocket(self):
        self.ws = websocket.WebSocket()  # Create a WebSocket object
        self.ws.connect("ws://localhost:1123/?uid=python_client")  # Connect to the specified WebSocket server

    def websocket_sender(self, data):
        try:
            self.ws.send(str(data).encode())  # Send data through the websocket connection
        except (ConnectionResetError, ConnectionAbortedError) as e:
            self.__generate_websocket()  # Reestablish the websocket connection

    def set_curved_road(self, start, end, control):  # Define a method to set up a curved road
        self.roads.append(CurvedRoad(start, control, end))

    def set_road(self, *args):  # Define a method to set up a road
        self.roads.append(Road(args))

    def set_vehicles(self, vehicle):  # Define a method to set up vehicles
        self.vehicles[vehicle.id] = vehicle
        if(len(vehicle.path) > 0):
            self.roads[vehicle.path[0]].set_vehicle(vehicle)  # Set the vehicle on the corresponding road

    def set_vehicle_generator(self, gen):  # Define a method to set up a vehicle generator
        self.vehicle_generator.append(gen)

    def set_traffic_light(self, roads):  # Define a method to set up traffic lights.
        roads = [[self.roads[i] for i in road_group] for road_group in roads]  # Convert road indices to road objects.
        self.traffic_lights.append(TrafficLight(roads, self.websocket_sender))  # Create a TrafficLight object and add it to the list of traffic lights

    def run(self):  # Define a method to run the simulation
        self.update()

    def update(self):  # Define a method to update the simulation state
        for road in self.roads:  # Iterate over each road
            road.update(self.delta_time)  # Update the road state

        for traffic_light in self.traffic_lights:  # Iterate over each traffic light
            traffic_light.update()  # Update the traffic light state

        for gen in self.vehicle_generator:  # Iterate over each vehicle generator
            gen.update(self)  # Update the vehicle generation process

        for road in self.roads:  # Iterate over each road
            if(len(road.vehicles) == 0):  # Check if the road has no vehicles
                continue  # Skip to the next road

            vehicle = self.vehicles[road.vehicles[0].id]  # Get the first vehicle on the road

            if(vehicle.x >= road.get_length()):  # Check if the vehicle has reached the end of the road
                if(vehicle.current_road_index + 1 < len(vehicle.path)):  # Check if there's another road in the vehicle's path
                    vehicle.current_road_index += 1  # Update the current road index for the vehicle
                    self.roads[vehicle.path[vehicle.current_road_index]].vehicles.append(road.vehicles[0])  # Move the vehicle to the next road
                vehicle.x = 0  # Reset the vehicle's position on the road
                self.websocket_sender({"action": "remove_vehicle", "data": [{"id": str(road.vehicles[0].id)}]})
                road.vehicles.popleft()  # Remove the vehicle from the road.
        
        self.time += self.delta_time
