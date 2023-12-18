class Region:
    def __init__(self, id):
        self.id = id
        self.is_alert = False
        self.last_change_at = None
    def air_raid_alert(self, timestamp):
        self.is_alert = True
        self.last_change_at = timestamp
    def air_raid_end(self, timestamp):
        self.is_alert = False
        self.last_change_at = timestamp
