from Classes.road_class import Road

CURVE_RESOLUTION = 50

class CurvedRoad(Road):
    def __init__(self, start, control, end):
        self.start = start
        self.end = end

        self.control = control

        path = []
        for i in range(CURVE_RESOLUTION):
            t = i / (CURVE_RESOLUTION-1)
            x = (t**2 * self.end[0]) + (2*t*(1-t) * self.control[0]) + ((1-t)**2 * self.start[0])
            y = (t**2 * self.end[1]) + (2*t*(1-t) * self.control[1]) + ((1-t)**2 * self.start[1])

            path.append((x, y))

        super().__init__(path)

        normalized_path = self.get_normalized_path(CURVE_RESOLUTION)
        super().__init__(normalized_path)