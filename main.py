from fastapi import FastAPI
#from postData import loanData
import numpy as np
import pickle 
import pandas as pd
from pydantic import BaseModel
import asyncio

app = FastAPI()
pickle_in = open('deploy_model.pkl','rb')
eligibilityML = pickle.load(pickle_in)

pickle_in2 = open('loan_amount_model.pkl','rb')
amountML = pickle.load(pickle_in2)

pickle_in3 = open('loan_amount_term_model.pkl','rb')
amountTermML = pickle.load(pickle_in3)

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
def checkEligibility(data:loanData):
    result = eligibilityML.predict([[data.creditHistory,data.Education,data.Gender]])
    value = ''
    if result[0] == 0:
        value = 'not eligiable'
    if result[0] == 1:
        value = 'eligiable'
    return{'prediction':value}
   
@app.post('/predictAmount')
def calcAmount(data:loanData):
    checkloanee = checkEligibility(data)
    amount = 0
    print(checkloanee)
    if list(checkloanee.values())[0] == 'not eligiable':
        return{'client is not eligile amount is': amount}
    else:
        if data.Income == 0:
            return{'client is not eligile amount is': amount}
        result = amountML.predict([[data.Gender,data.Married,data.selfEmployed,data.Income,data.CoIncome,data.creditHistory]])
        if result[0] != 0:
            return{'amount is':result[0]}
    
    
@app.post('/predictAmountTerm')
async def calcAmountTerm(data:loanData):
    amount = calcAmount(data)
    print(amount.values())
    passToModel = float(list(amount.values())[0])
    if passToModel == 0:
        return{'client is not eligile amount is': -1}
    result = amountTermML.predict([[data.Gender,data.Married,data.selfEmployed,data.Income,data.CoIncome,passToModel,data.creditHistory]])
    print(result)
    if result[0] != 0:
        return{'term is':result[0]}
    