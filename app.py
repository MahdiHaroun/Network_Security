from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
from fastapi import FastAPI , File , UploadFile , Request 
from fastapi.responses import Response 
from starlette.responses import RedirectResponse 
from fastapi.responses import FileResponse, JSONResponse
import uvicorn




import os , sys 
import certifi 
from dotenv import load_dotenv 
import pymongo 
import pandas as pd
from datetime import datetime
import json


from Network_Security.exception.exception import NetworkSecurityException 
from Network_Security.logging.logger import logger 
from Network_Security.piplines.training_pipeline import TrainingPipeline
from Network_Security.utils.main_utils.utils import load_object
from Network_Security.utils.ml_utils.model.estimator import NetworkModel
import Mongo_push_Trined_Data


ca = certifi.where() 
load_dotenv() 
uri = "mongodb+srv://MahdiHaroun:"+os.getenv("MONGODB_PASSWORD")+"@cluster0.vgezfpm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
print(uri)
client = pymongo.MongoClient(uri , tlsCAFile=ca)
from Network_Security.constants.training_pipeline import DATA_INGESTION_DATABASE_NAME , DATA_INGESTION_COLLECTION_NAME 
database = client[DATA_INGESTION_DATABASE_NAME] 
collection = client[DATA_INGESTION_COLLECTION_NAME]



app = FastAPI() 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")

@app.get('/') 
async def index():
    return RedirectResponse(url="/docs")


@app.get("/train")
async def train_route():
    try : 
        train_pipline = TrainingPipeline()
        train_pipline.run_pipeline()
        return Response ("Training is Successful")
    except Exception as e: 
        raise NetworkSecurityException(e, sys) 

from datetime import datetime
import os



@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...), response_type: str = "html"):
    try:
        df = pd.read_csv(file.file)

        preprocessor = load_object("final_model/preprocessor.pkl")
        final_model = load_object("final_model/model.pkl")
        network_model = NetworkModel(preprocessor=preprocessor, model=final_model)

        # Make predictions
        y_pred = network_model.predict(df)
        df['predicted_column'] = y_pred
        df['predicted_column'] = df['predicted_column'].replace(-1, 0)

        # Create timestamped filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        original_name = os.path.splitext(file.filename)[0]
        safe_name = original_name.replace(" ", "_")

        output_dir = "prediction_output"
        os.makedirs(output_dir, exist_ok=True)

        csv_path = os.path.join(output_dir, f"{safe_name}_{timestamp}.csv")
        json_path = os.path.join(output_dir, f"{safe_name}_{timestamp}.json")

        df.to_csv(csv_path, index=False)
        df.to_json(json_path, orient='records', lines=True)

        # 🔹 If n8n asks for CSV, return it
        if response_type == "csv":
            return FileResponse(csv_path, media_type="text/csv", filename=f"{safe_name}_{timestamp}.csv")

        # 🔹 Default: return HTML table for browser viewing
        table_html = df.to_html(classes='table table-striped')
        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})

    except Exception as e:
        raise NetworkSecurityException(e, sys)

    
@app.post("/json_file_upload/")
async def upload_json_file(file: UploadFile = File(...)):
    try:
        # Read JSON file
        contents = await file.read()
        data = json.loads(contents)

        # Extract original file name without extension
        file_name = file.filename.rsplit('.', 1)[0]  

        # Generate collection name with file name + timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        collection_name = f"predicted_{file_name}_{timestamp}"

        # Push to MongoDB
        uploader = Mongo_push_Trined_Data.Predicted_JSON_Uplaoder()
        records_inserted = uploader.push_data_to_mongoDB(
            records=data,
            database="Pridected_csvs_to_json",
            collection=collection_name
        )

        return JSONResponse(content={
            "message": f"Successfully inserted {records_inserted} records into collection '{collection_name}'."
        })

    except Exception as e:
        raise NetworkSecurityException(e, sys)
    



if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)