from datetime import datetime

class AnalysisHistory:
    def __init__(self):
        self.storage = []

    def save(self, input_data, result):
        self.storage.append({
            "input": input_data,
            "result": result,
            "timestamp": datetime.now()
        })