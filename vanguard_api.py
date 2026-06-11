from fastapi import FastAPI

app = FastAPI()

@app.get("/summary")
def summary():
    return {
        "control_rate": 0.6559,
        "test_rate": 0.6929,
        "lift": 0.0371
    }