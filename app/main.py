from fastapi import FastAPI
from models import InstallationData, AnalysisResult
from services import Calculator, Validator, LightingSchedule
from db import SessionLocal, AnalysisHistoryDB, init_db
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

calculator = Calculator()
validator = Validator()
schedule = LightingSchedule()


@app.post("/analyze", response_model=AnalysisResult)
def analyze(data: InstallationData):

    db = SessionLocal()

    yearly_hours = schedule.yearly_hours()

    power = data.power_kw or 0
    consumption = data.yearly_consumption_kwh or 0
    night_reduction = data.night_reduction_percent or 0

    expected_consumption = calculator.yearly_consumption(power, yearly_hours, night_reduction)
    estimated_power = calculator.estimate_power(consumption, yearly_hours, night_reduction) if consumption else 0

    monthly = calculator.monthly_consumption(power, schedule.hours_per_month, night_reduction)

    status = validator.validate(expected_consumption, consumption) if power and consumption else "UNKNOWN"

    result = AnalysisResult(
        yearly_consumption=expected_consumption,
        monthly_consumption=monthly,
        estimated_power=estimated_power,
        status=status
    )

    db_obj = AnalysisHistoryDB(
        power_kw=power,
        yearly_consumption=expected_consumption,
        status=status
    )
    db.add(db_obj)
    db.commit()
    db.close()

    return result

@app.get("/history")
def get_history():
    db = SessionLocal()
    data = db.query(AnalysisHistoryDB).all()
    db.close()

    return [
        {
            "id": x.id,
            "power_kw": x.power_kw,
            "yearly_consumption": x.yearly_consumption,
            "status": x.status,
            "timestamp": x.timestamp
        }
        for x in data
    ]