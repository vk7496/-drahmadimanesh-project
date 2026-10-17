from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI(title="Dr. Ahmadi-Manesh Wallet API")

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

# تنظیمات درگاه زرین‌پال (آزمایشی Sandbox)
ZARINPAL_MERCHANT = "00000000-0000-0000-0000-000000000000" # کد تست
ZP_REQ_URL = "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
ZP_START_PAY = "https://sandbox.zarinpal.com/pg/StartPay/"
ZP_VERIFY_URL = "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
CALLBACK_URL = "http://127.0.0.1:8000/api/wallet/verify"

class PaymentRequest(BaseModel):
    merchant_code: str
    amount: int

class TopUpRequest(BaseModel):
    amount: int

@app.get("/api/user")
def get_user_info():
    return user_db

# ۱. درخواست شارژ کیف پول و اتصال به زرین‌پال
@app.post("/api/wallet/topup")
def request_wallet_topup(data: TopUpRequest):
    if data.amount < 1000:
        raise HTTPException(status_code=400, detail="حداقل مبلغ شارژ ۱,۰۰۰ تومان است.")
    
    req_data = {
        "merchant_id": ZARINPAL_MERCHANT,
        "amount": data.amount * 10, # تبدیل تومان به ریال برای زرین‌پال
        "callback_url": CALLBACK_URL,
        "description": "شارژ کیف پول باشگاه اعضای معجزه ذهن",
    }
    
    try:
        response = requests.post(ZP_REQ_URL, json=req_data, timeout=10)
        res_json = response.json()
        
        if res_json.get("data") and res_json["data"].get("code") == 100:
            authority = res_json["data"]["authority"]
            return {
                "status": "success",
                "payment_url": f"{ZP_START_PAY}{authority}"
            }
        else:
            raise HTTPException(status_code=400, detail="خطا در ایجاد درگاه پرداخت.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="خطا در ارتباط با درگاه بانکی.")

# ۲. تایید پرداخت زرین‌پال (Callback)
@app.get("/api/wallet/verify")
def verify_wallet_topup(Authority: str, Status: str):
    if Status == "OK":
        # در حالت واقعی مبلغ از بانک استعلام می‌شود، اینجا برای دمو کیف پول را شارژ می‌کنیم
        user_db["wallet_balance"] += 50000 # مبلغ تستی اضافه شده
        return {"status": "success", "message": "شارژ کیف پول با موفقیت انجام شد!", "new_balance": user_db["wallet_balance"]}
    else:
        return {"status": "failed", "message": "پرداخت توسط کاربر لغو شد یا با خطا مواجه گردید."}

# ۳. کسر از کیف پول در کافه‌ها
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
