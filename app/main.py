# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
from pydantic.typing import Literal

app = FastAPI()

class Item(BaseModel):
    sex: Literal['male', 'female']
    bill_length_mm: float
    bill_depth_mm: float
    flipper_length_mm: float
    body_mass_g: float
    # Add more features as needed

@app.post("/predict")
async def predict(features: Item):
    try:
        # Load your pre-trained machine learning model
        model = joblib.load('model/model.joblib')
        preprocessor = joblib.load('model/preprocessor.joblib')

        # Prepare input features for prediction
        print(features.__dict__)
        features_df = pd.DataFrame(features.__dict__, index=[0])

        # Make predictions
        prediction = model.predict(preprocessor.transform(features_df))

        # Return the prediction as JSON response
        return {"predicted class": prediction[0]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
