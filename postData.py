from pydantic import BaseModel

class loanData(BaseModel):
    Gender:int
    Education:int
    creditHistory:float
