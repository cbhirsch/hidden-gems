import json


class TrailMetadata:
    def __init__(self):
        self.trails = json.load(open("cotrex.json"))

    def get_trail_by_timestamp(self, seconds_timestamp):
        minutes_timestamp = seconds_timestamp / 60
        for trail in self.trails:
            if trail["segment-start"] <= minutes_timestamp < trail["segment-end"]:
                trail.pop("segment-start")
                trail.pop("segment-end")
                trail.pop("map-thumbnail")
                return trail
        return None
