import asyncio
from Classes.window_class import Window
from Classes.simulation_class import Simulation
from Classes.vehicle_generator import VehicleGenerator

sim = Simulation()

#North Fragments
I_NORTH_1_RIGHT_ORIGIN = (-10, 40)
NORTH_1_RIGHT_CHK_1 = (-10, 20)
I_NORTH_1_RIGHT_CHK_2 = (-10, 10)
NORTH_1_RIGHT_CHK_3 = (-10,0)
NORTH_1_RIGHT_CHK_4 = (0,-10)
NORTH_1_RIGHT_CHK_5 = (20, -20)
NORTH_1_RIGHT_CHK_6 = (20, -30)
NORTH_1_RIGHT_CHK_7 = (20, -60)
NORTH_2_RIGHT_ORIGIN = (-60, 0)
NORTH_2_RIGHT_CHK_1 = (-60, -40)
NORTH_2_RIGHT_CHK_2 = (-60, -60)
NORTH_3_RIGHT_CHK_1 = (80, 90)
NORTH_3_RIGHT_CHK_2 = (80, 40)
NORTH_3_RIGHT_CHK_3 = (80, 20)

#South Fragments
SOUTH_RIGHT_ORIGIN = (-50,50)
I_SOUTH_RIGHT_CHK_1 = (-20, 50)
SOUTH_RIGHT_CHK_2 = (-10, 50)
SOUTH_RIGHT_CHK_3 = (20, 50)
SOUTH_RIGHT_CHK_4 = (30, 60)
SOUTH_RIGHT_CHK_5 = (30, 90)
SOUTH_RIGHT_CHK_6 = (40, 100)
SOUTH_RIGHT_CHK_7 = (70, 100)
SOUTH_2_RIGHT_ORIGIN = (-60, 20)
SOUTH_2_RIGHT_CHK_1 = (-60, 40)
SOUTH_2_RIGHT_CHK_2 = (-60, -50)
SOUTH_2_RIGHT_CHK_3 = (-60, 10)
SOUTH_3_RIGHT_ORIGIN = (110, -60)
SOUTH_3_RIGHT_CHK_1 = (110, -20)
SOUTH_3_RIGHT_CHK_3 = (110, 0)

#West Fragments
I_WEST_1_RIGHT_ORIGIN = (-20, 10)
WEST_1_RIGHT_CHK_1 = (-50, 10)
WEST_1_RIGHT_CHK_2 = (100, 10)
WEST_1_RIGHT_CHK_3 = (70,10)
WEST_1_RIGHT_CHK_4 = (40, 10)
WEST_1_RIGHT_CHK_5 = (0, 10)

#East Fragments
EAST_1_RIGHT_ORIGIN = (10,-10)
I_EAST_1_RIGHT_CHK_1 = (100, -10)
EAST_2_RIGHT_ORIGIN = (-50, -70)
EAST_2_RIGHT_CHK_1 = (30, -70)
EAST_2_RIGHT_CHK_2 = (10, -70)
EAST_2_RIGHT_CHK_3 = (70, -70)
EAST_2_RIGHT_CHK_4 = (100, -70)

#North Curve Controls
NORTH_RIGHT_CTRL_1 = (-10, 50)
NORTH_RIGHT_CTRL_2 = (-10, -10)
NORTH_RIGHT_CTRL_3 = (-60, 10)
NORTH_RIGHT_CTRL_4 = (20, -10)
NORTH_RIGHT_CTRL_5 = (80, 100)
NORTH_RIGHT_CTRL_6 = (-10, 10)

#South Curve Controls
SOUTH_RIGHT_CTRL_1 = (30, 50)
SOUTH_RIGHT_CTRL_2 = (30, 100)
SOUTH_RIGHT_CTRL_3 = (-60, 10)
SOUTH_RIGHT_CTRL_4 = (-60, 50)
SOUTH_RIGHT_CTRL_5 = (110, -70)
SOUTH_RIGHT_CTRL_6 = (110, -10)

#WEST Curve Controls
WEST_RIGHT_CTRL_1 = (-10, 10)
WEST_RIGHT_CTRL_2 = (110, 10)
WEST_RIGHT_CTRL_3 = (80, 10)

#East Curve Controls
EAST_RIGHT_CTRL_1 = (-60, -70)
EAST_RIGHT_CTRL_2 = (20, -70)

sim.set_road(SOUTH_RIGHT_ORIGIN, I_SOUTH_RIGHT_CHK_1), # 0
sim.set_road(I_SOUTH_RIGHT_CHK_1, SOUTH_RIGHT_CHK_2),  # 1
sim.set_road(SOUTH_RIGHT_CHK_2, SOUTH_RIGHT_CHK_3), # 2
sim.set_curved_road(SOUTH_RIGHT_CHK_3, SOUTH_RIGHT_CHK_4, SOUTH_RIGHT_CTRL_1), # 3
sim.set_road(SOUTH_RIGHT_CHK_4, SOUTH_RIGHT_CHK_5), # 4
sim.set_curved_road(SOUTH_RIGHT_CHK_5, SOUTH_RIGHT_CHK_6, SOUTH_RIGHT_CTRL_2), # 5
sim.set_road(SOUTH_RIGHT_CHK_6, SOUTH_RIGHT_CHK_7), # 6
sim.set_curved_road(I_SOUTH_RIGHT_CHK_1, I_NORTH_1_RIGHT_ORIGIN, NORTH_RIGHT_CTRL_1),  # 7
sim.set_road(I_NORTH_1_RIGHT_ORIGIN, NORTH_1_RIGHT_CHK_1), # 8
sim.set_road(NORTH_1_RIGHT_CHK_1, I_NORTH_1_RIGHT_CHK_2), # 9
sim.set_road(I_NORTH_1_RIGHT_CHK_2, NORTH_1_RIGHT_CHK_3), # 10
sim.set_curved_road(NORTH_1_RIGHT_CHK_3, NORTH_1_RIGHT_CHK_4, NORTH_RIGHT_CTRL_2),  # 11
sim.set_road(NORTH_1_RIGHT_CHK_4, EAST_1_RIGHT_ORIGIN), # 12
sim.set_curved_road(EAST_1_RIGHT_ORIGIN, NORTH_1_RIGHT_CHK_5, NORTH_RIGHT_CTRL_4), # 13
sim.set_road(NORTH_1_RIGHT_CHK_5, NORTH_1_RIGHT_CHK_6), # 14
sim.set_road(NORTH_1_RIGHT_CHK_6, NORTH_1_RIGHT_CHK_7), # 15
sim.set_curved_road(NORTH_1_RIGHT_CHK_7, EAST_2_RIGHT_CHK_1, EAST_RIGHT_CTRL_2), 0 # 16
sim.set_road(EAST_1_RIGHT_ORIGIN, I_EAST_1_RIGHT_CHK_1), # 17
sim.set_curved_road(I_EAST_1_RIGHT_CHK_1, SOUTH_3_RIGHT_CHK_3, SOUTH_RIGHT_CTRL_6), # 18
sim.set_curved_road(NORTH_1_RIGHT_CHK_1, I_WEST_1_RIGHT_ORIGIN, WEST_RIGHT_CTRL_1), # 19
sim.set_road(I_WEST_1_RIGHT_ORIGIN, WEST_1_RIGHT_CHK_1), # 20
sim.set_curved_road(WEST_1_RIGHT_CHK_1, NORTH_2_RIGHT_ORIGIN, NORTH_RIGHT_CTRL_3), # 21
sim.set_road(NORTH_2_RIGHT_ORIGIN, NORTH_2_RIGHT_CHK_1),  # 22
sim.set_road(NORTH_2_RIGHT_CHK_1, NORTH_2_RIGHT_CHK_2),  # 23
sim.set_curved_road(NORTH_2_RIGHT_CHK_2, EAST_2_RIGHT_ORIGIN, EAST_RIGHT_CTRL_1), # 24
sim.set_road(EAST_2_RIGHT_ORIGIN, EAST_2_RIGHT_CHK_2),  # 25
sim.set_road(EAST_2_RIGHT_CHK_2, EAST_2_RIGHT_CHK_1),  # 26
sim.set_road(EAST_2_RIGHT_CHK_1, EAST_2_RIGHT_CHK_3),  # 27
sim.set_road(EAST_2_RIGHT_CHK_3, EAST_2_RIGHT_CHK_4),  # 28
sim.set_curved_road(EAST_2_RIGHT_CHK_4, SOUTH_3_RIGHT_ORIGIN, SOUTH_RIGHT_CTRL_5), # 29
sim.set_road(SOUTH_3_RIGHT_ORIGIN, SOUTH_3_RIGHT_CHK_1),  # 30
sim.set_road(SOUTH_3_RIGHT_CHK_1, SOUTH_3_RIGHT_CHK_3),  # 31
sim.set_curved_road(SOUTH_3_RIGHT_CHK_3, WEST_1_RIGHT_CHK_2, WEST_RIGHT_CTRL_2), # 32
sim.set_curved_road(WEST_1_RIGHT_CHK_1, SOUTH_2_RIGHT_ORIGIN, SOUTH_RIGHT_CTRL_3), # 33
sim.set_road(SOUTH_2_RIGHT_ORIGIN, SOUTH_2_RIGHT_CHK_1),  # 34
sim.set_curved_road(SOUTH_2_RIGHT_CHK_1, SOUTH_RIGHT_ORIGIN, SOUTH_RIGHT_CTRL_4), # 35
sim.set_curved_road(SOUTH_RIGHT_CHK_7, NORTH_3_RIGHT_CHK_1, NORTH_RIGHT_CTRL_5), # 36
sim.set_road(NORTH_3_RIGHT_CHK_1, NORTH_3_RIGHT_CHK_2),  # 37
sim.set_road(NORTH_3_RIGHT_CHK_2, NORTH_3_RIGHT_CHK_3),  # 38
sim.set_curved_road(SOUTH_RIGHT_CHK_7, NORTH_3_RIGHT_CHK_1, NORTH_RIGHT_CTRL_5), # 39
sim.set_road(WEST_1_RIGHT_CHK_2, WEST_1_RIGHT_CHK_3),  # 40
sim.set_road(WEST_1_RIGHT_CHK_3, WEST_1_RIGHT_CHK_4),  # 41
sim.set_road(WEST_1_RIGHT_CHK_4, WEST_1_RIGHT_CHK_5),  # 42
sim.set_curved_road(WEST_1_RIGHT_CHK_5, NORTH_1_RIGHT_CHK_3, NORTH_RIGHT_CTRL_6), # 43
sim.set_curved_road(NORTH_3_RIGHT_CHK_3, WEST_1_RIGHT_CHK_3, WEST_RIGHT_CTRL_3), # 44
sim.set_road(WEST_1_RIGHT_CHK_5, I_WEST_1_RIGHT_ORIGIN),  # 45

#TARGETS
sim.set_curved_road((30, 60), (40,70), (30, 70)), # 46
sim.set_curved_road((-60, 20), (-50,30), (-60, 30)), # 47
sim.set_curved_road((20, -30), (10,-40), (20, -40)), # 48
sim.set_curved_road((-60, -40), (-50,-50), (-60, -50)), # 49
sim.set_curved_road((70, -70), (80,-60), (80, -70)), # 50
sim.set_curved_road((80, 40), (70,30), (80, 30)), # 51
sim.set_curved_road((40, 10), (30, 0), (30, 10)), # 52

# sim.set_traffic_light([[8]])
sim.set_traffic_light([[8, 25, 30], [42, 38]])

vg = VehicleGenerator({
    'vehicles': [
        (1, {'path': [0, 1, 2, 3, 46], 'velocity': 33.2}),
        (1, {'path': [0, 1, 2, 3, 4, 5, 6, 39, 37, 51], 'velocity': 33.2}),
        (1, {'path': [0, 7, 8, 19, 20, 33, 47], 'velocity': 33.2}),
        (1, {'path': [0, 7, 8, 19, 20, 21, 22, 49], 'velocity': 33.2}),

        (1, {'path': [25, 26, 27, 50], 'velocity': 33.2}),
        (1, {'path': [25, 26, 27, 28, 29, 30, 31, 32, 40, 41, 52], 'velocity': 33.2}),
        (1, {'path': [25, 26, 27, 28, 29, 30, 31, 32, 40, 41, 42, 45, 20, 33, 47], 'velocity': 33.2}),
        (1, {'path': [25, 26, 27, 28, 29, 30, 31, 32, 40, 41, 42, 43, 11, 12, 13, 14, 48], 'velocity': 33.2}),

        (1, {'path': [37, 38, 44, 41, 52], 'velocity': 33.2}),
        ]
    })
sim.set_vehicle_generator(vg)

win = Window(sim)
win.run()
win.show()