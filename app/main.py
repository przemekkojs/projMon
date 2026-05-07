from fastapi import FastAPI
from models import InstallationData, AnalysisResult
from services import Calculator, Validator, LightingSchedule
from data import AnalysisHistory

app = FastAPI()

calculator = Calculator()
validator = Validator()
schedule = LightingSchedule()
history = AnalysisHistory()


@app.post("/analyze", response_model=AnalysisResult)
def analyze(data: InstallationData):

    yearly_hours = schedule.yearly_hours()

    # fallback jeśli brak danych
    power = data.power_kw or 0
    consumption = data.yearly_consumption_kwh or 0

    expected_consumption = calculator.yearly_consumption(power, yearly_hours)
    estimated_power = calculator.estimate_power(consumption, yearly_hours) if consumption else 0

    monthly = calculator.monthly_consumption(power, schedule.hours_per_month)

    status = validator.validate(expected_consumption, consumption) if power and consumption else "UNKNOWN"

    result = AnalysisResult(
        yearly_consumption=expected_consumption,
        monthly_consumption=monthly,
        estimated_power=estimated_power,
        status=status
    )

    history.save(data.dict(), result.dict())

    return result