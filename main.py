from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from allocations import calculate_allocations
app = FastAPI()

# only for localdedv!
origins = [
    "http://localhost:3000",
]

# only for localdedv!
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Investor(BaseModel):
    name: str
    average_amount: int
    requested_amount: int
    
class InvestorList(BaseModel):
    investor_amounts: list[Investor]
    allocation_amount: int

@app.post("/calculate")
async def calculate(data: InvestorList, isComplexCalc: Union[bool, None] = None):
    formatted_data = {
        "allocation_amount": data.allocation_amount,
        "investor_amounts": [{"name": investor.name, "average_amount": investor.average_amount, "requested_amount": investor.requested_amount} for investor in data.investor_amounts]
    }
    res = calculate_allocations(formatted_data, isComplexCalc or False)
    return {"result": res}
