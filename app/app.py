import boto3
import os
from fastapi import FastAPI, Request
from mangum import Mangum

from api.v1.api import router as api_router
from core import APP_SETTINGS

app = FastAPI(title='Serverless Lambda FastAPI', root_path='/prod')

app.include_router(api_router, prefix="/api/v1")


@app.get("/",  tags=["Home"])
def main_endpoint_test(request: Request):
    return {
        "message": "Welcome CI/CD Pipeline with GitHub Actions!",
        "query": request.query_params,
    }

@app.get("/start-machine",  tags=["Home"])
def main_endpoint_test(request: Request):
    client = boto3.client('stepfunctions')
    resp = client.start_execution(stateMachineArn=os.getenv('STATE_MACHINE_ARN'))
    return {
        'arn': os.getenv('STATE_MACHINE_ARN'),
        'success': resp.get('HTTPStatusCode') == 200,
    }
        

handler = Mangum(app=app) 