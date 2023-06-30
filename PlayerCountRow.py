from datetime import datetime as dt

class PlayerCountRow:
    world : str
    oldSchoolWorld: str
    count : int
    location : str
    type : str
    activity : str
    datetime: dt

    def __init__(self, world, oldSchoolWorld, count, location, type, activity, datetime : dt) -> None:
        self.world = world
        self.oldSchoolWorld = oldSchoolWorld
        self.count = count
        self.location = location
        self.type = type
        self.activity = activity
        self.datetime = datetime.strftime("%Y-%m-%dT%H:%M:%S")

    def __iter__(self):
        return iter([self.world, self.oldSchoolWorld, self.count, self.location, self.type, self.activity, self.datetime])