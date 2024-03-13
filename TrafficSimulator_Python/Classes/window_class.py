import math
import dearpygui.dearpygui as dpg

class Window:
    def __init__(self, simulation):
        self.simulation = simulation
        self.speed = 1

        self.zoom = 4
        self.zoom_speed = 1
        self.offset = (0, 0)
        self.old_offset = (0, 0)

        self.is_running = False
        self.is_dragging = False

        self.background_color = (250, 250, 250)
        self.road_color = (80, 80, 80)
        self.arrow_color = (240, 240, 240)
        self.green_color = (0, 255, 0)
        self.red_color = (255, 0, 0)

        self.__setup()
        self.__create_windows()
        self.__resize_windows()
        self.__create_handlers()

    @property
    def __canvas_width(self):
        return dpg.get_item_width("MainWindow")

    @property
    def __canvas_height(self):
        return dpg.get_item_height("MainWindow")

    def __setup(self):
        dpg.create_context()
        dpg.create_viewport(title="TrafficSimulator", width=1280, height=720)
        dpg.setup_dearpygui()

    def __create_windows(self):
        dpg.add_window(tag="MainWindow", label="Traffic Simulation", no_close=True, no_collapse=True, no_resize=True, no_move=True)
        
        dpg.add_draw_node(tag="OverlayCanvas", parent="MainWindow")
        dpg.add_draw_node(tag="Canvas", parent="MainWindow")

    def __resize_windows(self):
        dpg.set_item_width("MainWindow", dpg.get_viewport_width())
        dpg.set_item_height("MainWindow", dpg.get_viewport_height())

    def __create_handlers(self):
        with dpg.handler_registry():
            dpg.add_mouse_down_handler(callback=self.__mouse_down)
            dpg.add_mouse_drag_handler(callback=self.__mouse_drag)
            dpg.add_mouse_release_handler(callback=self.__mouse_release)
            dpg.add_mouse_wheel_handler(callback=self.__mouse_wheel)
        dpg.set_viewport_resize_callback(self.__resize_windows)

    def __mouse_down(self):
        if(not self.is_dragging):
            if(dpg.is_item_hovered("MainWindow")):
                self.is_dragging = True
                self.old_offset = self.offset
        
    def __mouse_drag(self, sender, app_data):
        if(self.is_dragging):
            self.offset = (self.old_offset[0] + (app_data[1] / self.zoom), self.old_offset[1] + (app_data[2] / self.zoom))

    def __mouse_release(self):
        self.is_dragging = False

    def __mouse_wheel(self, sender, app_data):
        if(dpg.is_item_hovered("MainWindow")):
            self.zoom_speed = 1 + 0.01*app_data

    def __update_inertial_zoom(self, clip=0.005):
        if(self.zoom_speed != 1):
            self.zoom *= self.zoom_speed
            self.zoom_speed = 1 + (self.zoom_speed - 1) / 1.05
        if(abs(self.zoom_speed - 1) < clip):
            self.zoom_speed = 1

    def __draw_background(self):
        dpg.draw_rectangle((-10, -10), (self.__canvas_width+10, self.__canvas_height+10),  thickness=0, fill=self.background_color, parent="OverlayCanvas")

    def __draw_roads(self):
        for road in self.simulation.roads:
            dpg.draw_polyline(road.points, color=self.road_color, thickness=3.5*self.zoom, parent="Canvas")
            dpg.draw_arrow(road.points[-1], road.points[-2], thickness=0, size=2, color=self.arrow_color, parent="Canvas")
    
    def __draw_traffic_lights(self):
        for traffic_light in self.simulation.traffic_lights:
            for i in range(len(traffic_light.roads)):
                color = self.green_color if(traffic_light.get_current_cycle[i]) else self.red_color
                for road in traffic_light.roads[i]:
                    node = dpg.add_draw_node(parent="Canvas")

                    d1, d2 = self.__get_line_direction(road.points[0][0], road.points[0][1], road.points[1][0], road.points[1][1])
                    dpg.draw_line(p1=(d1),p2=(d2),thickness=1.76*self.zoom,color=color,parent=node)

    def __get_line_direction(self, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1

        if(abs(dx) > abs(dy)):
            if(dx > 0):
                return (x2,y2), (x2+1,y2)
            else:
                return (x2,y2), (x2-1,y2)
        else:
            if(dy > 0):
                return (x2,y2), (x2,y2+1)
            else:
                return (x2,y2), (x2,y2-1)
    
    def __draw_vehicles(self):
        vehicle_coordinates = []
        for road in self.simulation.roads:
            for vehicle in road.vehicles:
                vehicle = self.simulation.vehicles[vehicle.id]
                progress = vehicle.x / road.get_length()
                position = road.get_point(progress)
                heading = road.get_heading(progress)

                node = dpg.add_draw_node(parent="Canvas")
                dpg.draw_line((0, 0), (vehicle.length, 0), thickness=1.76*self.zoom, color=vehicle.color, parent=node)

                translate = dpg.create_translation_matrix(position)
                rotate = dpg.create_rotation_matrix(heading, [0, 0, 1])
                dpg.apply_transform(node, translate*rotate)

                vehicle_coordinates.append({"id": str(vehicle.id), "x": position[0], "y": position[1], "heading": math.degrees(heading)})
        if(len(vehicle_coordinates) > 0):
            self.simulation.websocket_sender({"action": "update_vehicles", "data": vehicle_coordinates})
            # print(vehicle_coordinates)

    def __apply_transformation(self):
        screen_center = dpg.create_translation_matrix([self.__canvas_width/2, self.__canvas_height/2, -0.01])
        translate = dpg.create_translation_matrix(self.offset)
        scale = dpg.create_scale_matrix([self.zoom, self.zoom])
        dpg.apply_transform("Canvas", screen_center*scale*translate)

    def __render(self):
        self.__update_inertial_zoom()

        dpg.delete_item("OverlayCanvas", children_only=True)
        dpg.delete_item("Canvas", children_only=True)
        
        self.__draw_background()
        
        self.__draw_roads()
        self.__draw_vehicles()
        self.__draw_traffic_lights()

        self.__apply_transformation()

        if(self.is_running):
            self.simulation.run()

    def show(self):
        dpg.show_viewport()
        while dpg.is_dearpygui_running():
            self.__render()
            dpg.render_dearpygui_frame()
        dpg.destroy_context()

    def run(self):
        self.is_running = True