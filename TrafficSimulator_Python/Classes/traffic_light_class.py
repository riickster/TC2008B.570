import datetime

#* Defines a TrafficLight Class that saves all the parameters, configurations and actions of each Traffic Light
class TrafficLight:
    def __init__(self, roads, websocket_sender):
        self.roads = roads
        self.websocket_sender = websocket_sender

        self.__init_properties()  # Initialize properties and configure traffic light settings
        self.__set_default_config()  # Set default configuration values for the traffic light

    def __init_properties(self):
        for i in range(len(self.roads)):  # Iterate over the roads.
            for road in self.roads[i]:  # Iterate over the roads in each group
                road.set_traffic_light(self, i)  # Set the traffic light for each road

    def __set_default_config(self):
        # Set default parameters for traffic light behavior
        self.slow_distance = 25
        self.slow_factor = 0.4
        self.stop_distance = 15

        # Define the traffic light cycle (alternating between states)
        self.cycle = [(False, True), (True, False)]
        self.current_cycle_index = 0
        self.cycle_length = 10

        # Initialize time-related variables
        self.local_time = datetime.datetime.now()  # Get the current local time
        self.new_cycle_time = self.local_time + datetime.timedelta(seconds=self.cycle_length)  # Calculate the time for the next cycle

        # Flags to track state changes
        self.changed = False
        self.voted = False

    @property
    def get_current_cycle(self): # Return the current cycle state
        return self.cycle[self.current_cycle_index]

    def set_cycle(self, voted):
        # Toggle to the next cycle state
        if self.current_cycle_index == 0:
            self.current_cycle_index = 1
        else:
            self.current_cycle_index = 0

        # Calculate the time for the next cycle
        self.new_cycle_time = datetime.datetime.now() + datetime.timedelta(seconds=self.cycle_length)

        self.websocket_sender({"action": "update_lights_cycle", "data": []})

        # If voted, mark the traffic light as voted to change
        if voted:
            self.voted = True

    def update(self):
        # Check if its time to switch to the next cycle
        if datetime.datetime.now().strftime('%H:%M:%S') == self.new_cycle_time.strftime('%H:%M:%S') and not self.changed:
            self.set_cycle(voted=False)  # Change the cycle
            self.changed = True
            self.voted = False
        else:
            self.changed = False  # Reset the changed flag if not yet time to change the cycle
