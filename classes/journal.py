class Journal:
    def __init__(self, destination:str, distance: float, travel_time: int,
                 is_express: bool, is_superexpress: bool, is_bus: bool, is_airplane: bool):
        self.destination = destination
        self.distance = distance
        self.travel_time = travel_time
        self.is_express = is_express
        self.is_superexpress = is_superexpress
        self.is_bus = is_bus
        self.is_airplane = is_airplane


