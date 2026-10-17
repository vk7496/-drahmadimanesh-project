const API_URL = "http://127.0.0.1:8000";

// ۱. دریافت اطلاعات کاربر و موجودی از بک‌اند
async function fetchUser() {
    try {
        const res = await fetch(`${API_URL}/api/user`);
        const data = await res.json();
        document.getElementById('userName').innerText = data.name;
        document.getElementById('balance').innerText = data.wallet_balance.toLocaleString() + " تومان";
    } catch (e) {
        document.getElementById('userName').innerText = "خطا در اتصال به سرور بک‌اند!";
    }
}

// ۲. شروع اسکنر دوربین گوشی / لپ‌تاپ
function startScanner() {
    const html5QrCode = new Html5Qrcode("reader");
    html5QrCode.start(
        { facingMode: "environment" }, // استفاده از دوربین پشت
        { fps: 10, qrbox: 250 },
        async (qrCodeMessage) => {
            html5QrCode.stop();
            processPayment(qrCodeMessage);
        },
        (errorMessage) => {
            // خطاهای خواندن فریم‌های دوربین (نیازی به نمایش نیست)
        }
    );
}

// ۳. پردازش پرداخت و کسر از کیف پول
async function processPayment(merchantCode) {
    const amount = prompt("مبلغ فاکتور را وارد کنید (تومان):", "50000");
    if (!amount) return;

    try {
        const res = await fetch(`${API_URL}/api/pay`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                merchant_code: merchantCode,
                amount: parseInt(amount)
            })
        });

        const result = await res.json();

        if (res.ok) {
            alert(result.message);
            document.getElementById('balance').innerText = result.new_balance.toLocaleString() + " تومان";
        } else {
            alert("خطا: " + result.detail);
        }
    } catch (error) {
        alert("ارتباط با سرور برقرار نشد!");
    }
}

// اجرا به محض باز شدن صفحه
fetchUser();
