class Region:
    def __init__(self, id):
        self.id = id
        self.is_alert = False
    def air_raid_alert(self):
        self.is_alert = True
    def air_raid_end(self):
        self.is_alert = False
