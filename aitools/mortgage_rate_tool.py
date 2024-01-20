import os
import requests
from langchain.agents import tool
from dotenv import load_dotenv


load_dotenv()

X_RAPID_API_KEY = os.getenv("X_RAPID_API_KEY")
X_RAPID_API_HOST = os.getenv("X_RAPID_API_HOST")
MORTGAGE_URL = os.getenv("MORTGAGE_URL")

headers = {"X-RapidAPI-Key": X_RAPID_API_KEY, "X-RapidAPI-Host": X_RAPID_API_HOST}


@tool
def get_current_mortgage_rate(
    loan_amount: float, interest_rate: float, terms: float
) -> float:
    """Returns the computed mortgage rate based on the input values for loan amount, interest rate and terms."""
    querystring = {
        f"loanAmount": {str(loan_amount)},
        "interestRate": {str(interest_rate)},
        "terms": {str(terms)},
    }

    response = requests.get(MORTGAGE_URL, headers=headers, params=querystring)

    result = response.json()

    return result["monthlyPayment"]
