import datetime

class TrafficLight:
    def __init__(self, roads, websocket_sender):
        self.roads = roads
        self.websocket_sender = websocket_sender

        self.__init_properties()
        self.__set_default_config()

    def __init_properties(self):
        for i in range(len(self.roads)):
            for road in self.roads[i]:
                road.set_traffic_signal(self, i)
                
    def __set_default_config(self):
        self.slow_distance = 25
        self.slow_factor = 0.4
        self.stop_distance = 15

        self.cycle = [(False, True), (True, False)]
        self.current_cycle_index = 0
        self.cycle_length = 10

        self.local_time = datetime.datetime.now()
        self.new_cycle_time = self.local_time + datetime.timedelta(seconds=self.cycle_length)

        self.changed = False
        self.voted = False

    @property
    def get_current_cycle(self):
        return self.cycle[self.current_cycle_index]
    
    def set_cycle(self, voted):
        if(self.current_cycle_index == 0):
            self.current_cycle_index = 1
        else:
            self.current_cycle_index = 0

        self.new_cycle_time = datetime.datetime.now() + datetime.timedelta(seconds=self.cycle_length)

        self.websocket_sender({"action": "update_lights_cycle", "data": []})

        if(voted):
            self.voted = True

    def update(self):
        if(datetime.datetime.now().strftime('%H:%M:%S') == self.new_cycle_time.strftime('%H:%M:%S') and self.changed == False):
            self.set_cycle(voted=False)
            self.changed = True
            self.voted = False
        else:
            self.changed = False