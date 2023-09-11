from datetime import datetime


class Order:

    def __init__(self, arrival, departure, frame, station):
        self._arrival: datetime = arrival
        self._departure: datetime = departure
        self._frame: int = frame
        self._station: int = station

    @property
    def arrival_time(self):
        return self._arrival

    @property
    def departure_time(self):
        return self._departure

    @property
    def frame_id(self):
        return self._frame

    @property
    def station_id(self):
        return self._station

    def __str__(self):
        return f"arrival: {self._arrival}, departure: {self._departure}, frame: {self._frame}, station: {self._station}"
