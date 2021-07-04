# Stripe Connect Connected Fees

Show total collected fees via Stripe connect.


# How to run locally


## Setup
```
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

## Run
```
. venv/bin/activate
export STRIPE_LIVE_SECRET_KEY=secret #or test key
cd app/app/
uvicorn main:app --reload
```

# Visit api

http://127.0.0.1:8000/docs

