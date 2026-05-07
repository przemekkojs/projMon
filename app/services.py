from typing import Dict

class LightingSchedule:
    def __init__(self):
        # uproszczone godziny świecenia
        self.hours_per_month = {
            "jan": 400, "feb": 350, "mar": 300,
            "apr": 200, "may": 150, "jun": 100,
            "jul": 120, "aug": 180, "sep": 250,
            "oct": 320, "nov": 380, "dec": 420
        }

    def yearly_hours(self):
        return sum(self.hours_per_month.values())


class Calculator:

    def yearly_consumption(self, power_kw, yearly_hours):
        return power_kw * yearly_hours

    def monthly_consumption(self, power_kw, hours_per_month):
        return {
            m: power_kw * h for m, h in hours_per_month.items()
        }

    def estimate_power(self, yearly_consumption, yearly_hours):
        return yearly_consumption / yearly_hours


class Validator:

    def validate(self, expected, actual):
        diff = abs(expected - actual) / expected

        if diff < 0.1:
            return "GREEN"
        elif diff < 0.3:
            return "YELLOW"
        return "RED"