from pydantic import BaseModel
from typing import Dict

class InstallationData(BaseModel):
    power_kw: float | None = None
    yearly_consumption_kwh: float | None = None
    location: str | None = None
    control_type: str | None = None
    night_reduction_percent: float | None = 0


class AnalysisResult(BaseModel):
    yearly_consumption: float
    monthly_consumption: Dict[str, float]
    estimated_power: float
    status: str