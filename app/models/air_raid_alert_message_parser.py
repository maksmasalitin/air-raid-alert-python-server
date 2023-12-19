

class AirRaidAlertMessageParser:
  CHANNEL_NAME = 'air_alert_ua'
  REGION_MAP = {
    'Вінницька_область': 2,
    'Волинська_область': 3,
    'Дніпропетровська_область': 4,
    'Донецька_область': 5,
    'Житомирська_область': 6,
    'Закарпатська_область': 7,
    'Запорізька_область': 8,
    'Івано-Франківська_область': 9,
    'Київська_область': 10,
    'Кіровоградська_область': 11,
    'Луганська_область': 12,
    'Львівська_область': 13,
    'Миколаївська_область': 14,
    'Одеська_область': 15,
    'Полтавська_область': 16,
    'Рівненська_область': 17,
    'Сумська_область': 18,
    'Тернопільська_область': 19,
    'Харківська_область': 20,
    'Херсонська_область': 21,
    'Хмельницька_область': 22,
    'Черкаська_область': 23,
    'Чернівецька_область': 24,
    'Чернігівська_область': 25
  }

  ALERT_MESSAGE = "\U0001F534 Тривога"
  END_MESSAGE = "\U0001F7E2 Відбій тривоги"

  def __init__(self, message):
    self.text = message.message
    self.timestamp = message.date

  def is_an_air_raid_alert(self):
    return "Повітряна тривога" in self.text

  def region_id(self):
    for tag, id in self.REGION_MAP.items():
      if tag in self.text:
        return id
    return None

  def status_text(self):
    return self.ALERT_MESSAGE if self.is_an_air_raid_alert() else self.END_MESSAGE
