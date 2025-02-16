from fastapi import FastAPI, HTTPException

from . import data_acquisition

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to the FPLAgent FastAPI App"}


@app.post("/refresh-data")
async def refresh_data():
    try:
        success = data_acquisition.fetch_and_store_data()
        return {"status": "success", "message": "Data refresh completed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
