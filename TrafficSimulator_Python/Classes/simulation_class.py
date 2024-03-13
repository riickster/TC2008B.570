import websocket
from Classes.road_class import Road
from Classes.curved_road_class import CurvedRoad
from Classes.traffic_light_class import TrafficLight

class Simulation:
    def __init__(self):
        self.time = 0.0
        self.delta_time = 1/60

        self.roads = []
        self.traffic_lights = []

        self.vehicles = {}
        self.vehicle_generator = []

        self.__generate_websocket()
    
    def __generate_websocket(self):
        self.ws = websocket.WebSocket()
        self.ws.connect("ws://localhost:1123/?uid=python_client")

    def websocket_sender(self, data):
        try:
            self.ws.send(str(data).encode())
        except (ConnectionResetError, ConnectionAbortedError) as e:
            print(e)
            self.__generate_websocket()

    def set_curved_road(self, start, end, control):
        self.roads.append(CurvedRoad(start, control, end))

    def set_road(self, *args):
        self.roads.append(Road(args))

    def set_vehicles(self, vehicle):
        self.vehicles[vehicle.id] = vehicle
        if(len(vehicle.path) > 0):
            self.roads[vehicle.path[0]].set_vehicle(vehicle)

    def set_vehicle_generator(self, gen):
        self.vehicle_generator.append(gen)

    def set_traffic_light(self, roads):
        roads = [[self.roads[i] for i in road_group] for road_group in roads]
        self.traffic_lights.append(TrafficLight(roads, self.websocket_sender))

    def run(self):
        self.update()

    def update(self):
        for road in self.roads:
            road.update(self.delta_time)

        for traffic_light in self.traffic_lights:
            traffic_light.update()

        for gen in self.vehicle_generator:
            gen.update(self)

        for road in self.roads:
            if(len(road.vehicles) == 0): 
                continue

            vehicle = self.vehicles[road.vehicles[0].id]

            if(vehicle.x >= road.get_length()):
                if(vehicle.current_road_index + 1 < len(vehicle.path)):
                    vehicle.current_road_index += 1
                    self.roads[vehicle.path[vehicle.current_road_index]].vehicles.append(road.vehicles[0])
                vehicle.x = 0
                self.websocket_sender({"action": "remove_vehicle", "data": [{"id": str(road.vehicles[0].id)}]})
                road.vehicles.popleft()
        
        self.time += self.delta_time