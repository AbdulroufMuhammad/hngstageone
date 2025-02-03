from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
from typing import Union
from math import sqrt
from datetime import datetime

app = FastAPI()

# Enable CORS (allow all origins, methods, and headers)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def is_prime(num: int) -> bool:
    if num < 2:
        return False
    for i in range(2, int(sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

def is_perfect(num: int) -> bool:
    if num < 1:
        return False
    sum_divisors = 0
    for i in range(1, num // 2 + 1):
        if num % i == 0:
            sum_divisors += i
    return sum_divisors == num

def is_armstrong(num: int) -> bool:
    # Convert number to string
    digits_str = str(num)
    num_digits = len(digits_str)
    
    # Calculate sum of each digit^n
    total = 0
    for d in digits_str:
        total += int(d) ** num_digits
    
    return total == num

def get_digit_sum(num: int) -> int:
    return sum(int(d) for d in str(num))

@app.get("/api/classify-number")
async def classify_number(number: Union[str, None] = None):
    """
    Classifies a given number by checking if it's prime, perfect, Armstrong, odd/even, etc.
    Returns JSON response with the specified fields.
    """

    # 1) Validate the query parameter
    if not number:
        # No "number" query param provided -> 400
        raise HTTPException(status_code=400, detail={
            "number": None,
            "error": True
        })

    # 2) Check if it's a valid integer
    try:
        num = int(number)
    except ValueError:
        # Not a valid integer -> 400
        raise HTTPException(status_code=400, detail={
            "number": number,
            "error": True
        })

    # 3) Perform classification
    prime = is_prime(num)
    perfect = is_perfect(num)
    armstrong = is_armstrong(num)
    digit_sum = get_digit_sum(num)

    # "properties" logic
    properties = []
    if armstrong:
        properties.append("armstrong")
    if num % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")

    # 4) Get fun fact from Numbers API
    fun_fact = "No fact available."
    async with httpx.AsyncClient() as client:
        url = f"http://numbersapi.com/{num}/math?json"
        try:
            resp = await client.get(url)
            data = resp.json()
            if data.get("found"):
                fun_fact = data.get("text", "")
        except Exception:
            # If for any reason the request fails, fallback to a default message
            fun_fact = "Could not retrieve a fun fact at this time."

    # 5) Construct final response
    response_data = {
        "number": num,
        "is_prime": prime,
        "is_perfect": perfect,
        "properties": properties,
        "digit_sum": digit_sum,
        "fun_fact": fun_fact
    }

    return response_data
