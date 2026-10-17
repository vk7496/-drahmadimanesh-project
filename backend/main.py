from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Dr. Ahmadi-Manesh Wallet API")

# اجازه دسترسی فرانت‌اند به بک‌اند
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# دیتابیس آزمایشی در حافظه
user_db = {
    "user_id": 1,
    "name": "مخاطب ویژه معجزه ذهن",
    "wallet_balance": 1000000
}

merchant_db = {
    "CAFE_SUCCESS": "کافه راه موفقیت",
    "REST_VICTORY": "رستوران ایرانیان موفق"
}

class PaymentRequest(BaseModel):
    merchant_code: str
    amount: int

@app.get("/api/user")
def get_user_info():
    return user_db

@app.post("/api/pay")
def pay_at_merchant(data: PaymentRequest):
    if data.merchant_code not in merchant_db:
        raise HTTPException(status_code=400, detail="کافه یا مرکز خرید معتبر نیست!")
    
    if user_db["wallet_balance"] < data.amount:
        raise HTTPException(status_code=400, detail="موجودی کیف پول کافی نیست!")
    
    user_db["wallet_balance"] -= data.amount
    return {
        "status": "success",
        "message": f"پرداخت با موفقیت در {merchant_db[data.merchant_code]} انجام شد.",
        "new_balance": user_db["wallet_balance"]
    }
