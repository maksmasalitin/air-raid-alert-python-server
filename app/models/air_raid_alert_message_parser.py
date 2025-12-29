import os
import re

class AirRaidAlertMessageParser:
    CHANNEL_NAME = 'air_alert_ua'
    IGNORED = "IGNORED"

    _KEYWORDS_MAP = None
    _CENTERS_MAP = None
    _REGION_NAMES = None

    ALERT_MESSAGE = "\U0001F534 Тривога"
    END_MESSAGE = "\U0001F7E2 Відбій тривоги"

    def __init__(self, message):
        self.text = message.message
        self._load_config()

    @classmethod
    def _load_config(cls):
        if cls._KEYWORDS_MAP is not None:
            return

        cls._KEYWORDS_MAP = {}
        cls._CENTERS_MAP = {}
        cls._REGION_NAMES = {}

        base_dir = os.path.dirname(os.path.abspath(__file__))
        keywords_dir = os.path.abspath(os.path.join(base_dir, '..', '..', 'regions_keywords'))

        if not os.path.exists(keywords_dir):
            return

        for filename in os.listdir(keywords_dir):
            if not filename.endswith('.yaml'):
                continue
            
            filepath = os.path.join(keywords_dir, filename)
            region_id = None
            region_name = None
            center_tag = None
            keywords = []

            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('id:'):
                        region_id = int(line.split('id:')[1].strip())
                    elif line.startswith('name:'):
                        region_name = line.split('name:')[1].strip()
                    elif line.startswith('center_region:'):
                        center_tag = line.split('center_region:')[1].strip().strip('"\'')
                    elif line.startswith('-'):
                        kw = line.lstrip('- ').strip().strip('"\'')
                        if kw:
                            keywords.append(kw)

            if region_id is not None:
                cls._REGION_NAMES[region_id] = region_name
                cls._CENTERS_MAP[region_id] = center_tag
                for kw in keywords:
                    cls._KEYWORDS_MAP[kw] = region_id

    def is_an_air_raid_alert(self):
        return "Повітряна тривога" in self.text

    def region_id(self):
        found_hashtags = re.findall(r'#\w+', self.text)
        
        known_region_detected = False

        for tag in found_hashtags:
            region_id = self._KEYWORDS_MAP.get(tag)
            if region_id is None:
                continue

            if tag == self._CENTERS_MAP.get(region_id):
                return region_id
            
            known_region_detected = True

        if known_region_detected:
            return self.IGNORED
        
        return None

    def status_text(self):
        return self.ALERT_MESSAGE if self.is_an_air_raid_alert() else self.END_MESSAGE

    @classmethod
    def get_all_regions(cls):
        cls._load_config()
        return [(cls._CENTERS_MAP[rid], rid) for rid in sorted(cls._REGION_NAMES.keys()) if cls._CENTERS_MAP.get(rid)]
