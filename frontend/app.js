const API_URL = "";

function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('active');
    document.getElementById('overlay').classList.toggle('active');
}

async function fetchUser() {
    try {
        const res = await fetch(`${API_URL}/api/user`);
        const data = await res.json();
        
        document.getElementById('balance').innerText = data.wallet_balance.toLocaleString() + " تومان";
        document.getElementById('sidebarUserName').innerText = data.name;
        document.getElementById('sidebarBalance').innerText = data.wallet_balance.toLocaleString() + " تومان";
    } catch (e) {
        console.error("خطا در دریافت اطلاعات کاربر:", e);
    }
}

async function topupWallet() {
    const amount = prompt("مبلغ شارژ مورد نظر را به تومان وارد کنید:", "50000");
    if (!amount) return;

    try {
        const res = await fetch(`${API_URL}/api/wallet/topup`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ amount: parseInt(amount) })
        });

        const result = await res.json();
        if (res.ok && result.payment_url) {
            window.location.href = result.payment_url;
        } else {
            alert("خطا: " + (result.detail || "مشکل در درگاه پرداخت"));
        }
    } catch (e) {
        alert("خطا در ارتباط با سرور پرداخت!");
    }
}

function startScanner() {
    const html5QrCode = new Html5Qrcode("reader");
    html5QrCode.start(
        { facingMode: "environment" },
        { fps: 10, qrbox: 200 },
        async (qrCodeMessage) => {
            html5QrCode.stop();
            processPayment(qrCodeMessage);
        },
        (errorMessage) => { }
    ).catch(err => {
        alert("خطا در دسترسی به دوربین گوشی!");
    });
}

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
            fetchUser();
        } else {
            alert("خطا: " + result.detail);
        }
    } catch (error) {
        alert("ارتباط با سرور برقرار نشد!");
    }
}

fetchUser();
