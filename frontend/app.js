// شارژ آنلاین کیف پول از طریق درگاه زرین‌پال
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
            // انتقال کاربر به درگاه بانک
            window.location.href = result.payment_url;
        } else {
            alert("خطا: " + result.detail);
        }
    } catch (e) {
        alert("خطا در اتصال به درگاه پرداخت!");
    }
}
