from fastapi import FastAPI
#from postData import loanData
import numpy as np
import pickle 
import pandas as pd
from pydantic import BaseModel

app = FastAPI()
pickle_in = open('deploy_model.pkl','rb')
eligibilityML = pickle.load(pickle_in)

pickle_in2 = open('loan_amount_model.pkl','rb')
amountML = pickle.load(pickle_in2)


class loanData(BaseModel):
    creditHistory:float
    Education:int
    Gender:float
    Married:int
    Income:float
    CoIncome:float
    selfEmployed:int


@app.get('/')
async def index():
    return {'message':'Helllllllllllllllllllo Vitnaaaaaaaaaaaaaaam'}

@app.post('/predict')
async def test(data:loanData):
    result = eligibilityML.predict([[data.creditHistory,data.Education,data.Gender]])
    value = ''
    if result[0] == 0:
        value = 'not eligiable'
    if result[0] == 1:
        value = 'eligiable'
    return{'prediction':value}
   
@app.post('/predictAmount')
async def test2(data:loanData):
    result = amountML.predict([[data.Gender,data.Married,data.selfEmployed,data.Income,data.CoIncome,data.creditHistory]])
    amount = 0
    #print(result)
    #return result[0]
    if result[0] != 0:
        return{'amount is':result[0]}
    if data.Income == 0 and data.CoIncome == 0:
        return{'client is not eligile amount is': amount}
    #return{'error': result}
    
   