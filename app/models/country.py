from .region import Region

class Country:
    def __init__(self):
        self.regions = [Region(region_number) for region_number in range(2, 26)]

    def find_region(self, region_id):
        for region in self.regions:
            if region.id == region_id:
                return region

    def air_raid_alert(self, region_id):
        region = self.find_region(region_id)
        region.air_raid_alert()

    def air_raid_end(self, region_id):
        region = self.find_region(region_id)
        region.air_raid_end()

    def get_active_air_raid_regions(self):
        return [region.id for region in self.regions if region.is_alert]
