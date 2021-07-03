import stripe
import json
from fastapi import FastAPI
from typing import Optional
import datetime
import os

app = FastAPI()


STRIPE_LIVE_SECRET_KEY = os.getenv("STRIPE_LIVE_SECRET_KEY", None)
stripe.api_key = STRIPE_LIVE_SECRET_KEY


def fetch_application_fees():
    fees = stripe.ApplicationFee.list(limit=100)

    all_fees = []

    for fee in fees.auto_paging_iter():
        all_fees.append(fee)
    with open("application-fees.json", mode="w") as fp:
        fp.write(json.dumps(all_fees))


def load_fees():
    # Load fees
    with open("application-fees.json") as fp:
        return json.loads(fp.read())


def calculate_total_fees_collected(year=None, month=None):
    """Return total fees collected in pennies"""
    total = 0
    fees = load_fees()
    for fee in fees:
        if year and month:
            date = datetime.datetime.fromtimestamp(fee["created"])
            if date.year == year and date.month == month:
                total += fee["amount"]
        else:
            total += fee["amount"]
    return total


@app.get("/")
def read_root():
    fetch_application_fees()
    return load_fees()


@app.get("/total-fees-collected-all-time/")
def total_fees_collected_all_time():
    total = calculate_total_fees_collected()
    return {
        "total-fees-collected": {"in-pennies": total, "in-pounds": total / 100}
    }  # noqa


@app.get("/fees-collected/{year}/{month}")
def fees_by_year_month(year: Optional[int] = None, month: Optional[int] = None):  # noqa
    if year and month:
        total = calculate_total_fees_collected(year=year, month=month)
    else:
        total = calculate_total_fees_collected()
    return {
        "total-fees-collected": {"in-pennies": total, "in-pounds": total / 100}
    }  # noqa
