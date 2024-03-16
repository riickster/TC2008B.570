from Classes.road_class import Road

CURVE_RESOLUTION = 50 # Defines the number of steps of a Curve (Resolution)

#* Class that generates curved roads for the simulation
class CurvedRoad(Road):
    def __init__(self, start, control, end):
        self.start = start # Saves the origin Coordinates
        self.end = end # Saves the destination Coordinates

        self.control = control # Saves the Curve Point Coordinates

        path = []
        for i in range(CURVE_RESOLUTION): # Generates N numbers of coordinates according to the origin, control and end of the curve
            t = i / (CURVE_RESOLUTION-1) # Generates the dispolacement of the road segments for the curve
            x = (t**2 * self.end[0]) + (2*t*(1-t) * self.control[0]) + ((1-t)**2 * self.start[0]) # Generates the X corrdinates according to the curve steps
            y = (t**2 * self.end[1]) + (2*t*(1-t) * self.control[1]) + ((1-t)**2 * self.start[1]) # Generates the Y corrdinates according to the curve steps
            
            path.append((x, y)) # Saves the generated coordinates for that step

        super().__init__(path) # Initialises the Parent Class (Road) to generate a new instance of a Road of type Curved Road