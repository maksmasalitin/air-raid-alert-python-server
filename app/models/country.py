from .region import Region

class Country:
  def __init__(self):
    self.regions = [Region(region_number) for region_number in range(2, 26)]

  def find_region(self, region_id):
    for region in self.regions:
      if region.id == region_id:
        return region

  def air_raid_alert(self, region_id, timestamp):
    region = self.find_region(region_id)
    region.air_raid_alert(timestamp)

  def air_raid_end(self, region_id, timestamp):
    region = self.find_region(region_id)
    region.air_raid_end(timestamp)
