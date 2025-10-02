import os
import warnings
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from fastapi.responses import JSONResponse
import uvicorn
from tensorflow.keras.models import load_model

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Filter common warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Constants
SEQUENCE_LENGTH = 10
MODEL_PATH = "bi_lstm_model.keras"

# Load Bi-LSTM model
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
model = load_model(MODEL_PATH)

# Create FastAPI app
app = FastAPI(title="Bi-LSTM Stock Forecast API")

# Input schema
class PriceInput(BaseModel):
    prices: list[float]

    @validator("prices")
    def check_length(cls, v):
        if len(v) != SEQUENCE_LENGTH:
            raise ValueError(f"Expected {SEQUENCE_LENGTH} prices, got {len(v)}")
        return v

# Prediction endpoint
@app.post("/predict_next")
async def predict_next(input_data: PriceInput):
    try:
        prices = np.array(input_data.prices).reshape(1, SEQUENCE_LENGTH, 1)
        prediction = model.predict(prices)
        return {"predicted_price": float(prediction[0][0])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/test", response_class=JSONResponse)
async def home():
    return """
    <html>
        <body>
            <h1>Nagarajan-1</h1>
            
        </body>
    </html>
    """

# Run the server
#if __name__ == "__main__":
    #uvicorn.run(app, host= "localhost", port=8000)

