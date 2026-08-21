import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- CONFIGURATION ---
BOT_TOKEN = "8894345960:AAE6iepstgfDnhMQlLKe-_L5y-aMXD84BoA"
ADMIN_ID = 5691234567  # Yadi zaroorat ho toh apna sahi Telegram ID yahan daal lena

# Razorpay API Credentials
RAZORPAY_KEY_ID = "rzp_test_TSGmCyNHDUE4BX"
RAZORPAY_KEY_SECRET = "KYh5h2TxUtFSME0Znso3NZms"

# Plan Details & Prices
PLANS = {
    "1h": {"name": "1 Hour", "price": 33.00},
    "3h": {"name": "3 Hours", "price": 67.50},
    "6h": {"name": "6 Hours", "price": 108.00},
    "12h": {"name": "12 Hours", "price": 216.00},
    "1d": {"name": "1 Day", "price": 432.00},
    "2d": {"name": "2 Days", "price": 864.00},
    "3d": {"name": "3 Days", "price": 1275.00},
    "5d": {"name": "5 Days", "price": 2100.00},
    "7d": {"name": "7 Days", "price": 2700.00}
}

# Database Setup
def init_db():
    conn = sqlite3.connect('store.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, name TEXT)')
    conn.commit()
    conn.close()

init_db()

# --- HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    conn = sqlite3.connect('store.db')
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO users VALUES (?, ?)', (user.id, user.first_name))
    conn.commit()
    conn.close()

    text = (
        "🔥 **BALA MOD APK** 🔥\n"
        "📱 **NON-ROOT**\n"
        "✅ **MAIN ID SAFE**\n\n"
        f"👋 Welcome, {user.first_name}!\n\n🚀 Click Shop Now to Start!"
    )
    keyboard = [
        [InlineKeyboardButton("🛍️ Shop Now", callback_data="shop")],
        [InlineKeyboardButton("👤 Profile", callback_data="profile"), InlineKeyboardButton("💬 Support", callback_data="support")]
    ]
    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "shop":
        keyboard = [
            [InlineKeyboardButton("⏰ 1 Hour — ₹33.00", callback_data="buy_1h")],
            [InlineKeyboardButton("⏰ 3 Hours — ₹67.50", callback_data="buy_3h")],
            [InlineKeyboardButton("⏰ 6 Hours — ₹108.00", callback_data="buy_6h")],
            [InlineKeyboardButton("⏰ 12 Hours — ₹216.00", callback_data="buy_12h")],
            [InlineKeyboardButton("📅 1 Day — ₹432.00", callback_data="buy_1d")],
            [InlineKeyboardButton("📅 2 Days — ₹864.00", callback_data="buy_2d")],
            [InlineKeyboardButton("📅 3 Days — ₹1275.00", callback_data="buy_3d")],
            [InlineKeyboardButton("📅 5 Days — ₹2100.00", callback_data="buy_5d")],
            [InlineKeyboardButton("📅 7 Days — ₹2700.00", callback_data="buy_7d")],
            [InlineKeyboardButton("🔙 Back", callback_data="main")]
        ]
        await query.edit_message_text("📦 **INDIAN PRICE LIST 🇮🇳**\n\nSelect your plan:", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("buy_"):
        plan_key = data.split("_")[1]
        if plan_key in PLANS:
            p_info = PLANS[plan_key]
            text = f"💳 **PAYMENT DETAILS**\n\nPlan: {p_info['name']}\nAmount: ₹{p_info['price']}\n\n*Click below once you are ready.*"
            keyboard = [
                [InlineKeyboardButton("✅ I Have Paid", callback_data=f"paid_{plan_key}")], 
                [InlineKeyboardButton("🔙 Back", callback_data="shop")]
            ]
            await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("paid_"):
        plan_key = data.split("_")[1]
        plan_name = PLANS[plan_key]["name"] if plan_key in PLANS else plan_key
        user = query.from_user
        await query.edit_message_text("⏳ Payment request received. Admin verify kar raha hai, wait karein.")
        
        # Admin ko notification bhejo
        admin_text = f"🔔 **NEW PAYMENT ALERT**\n\nUser: {user.first_name}\nID: `{user.id}`\nPlan: {plan_name}\n\nKey bhejne ke liye niche command use karein:\n`/sendkey {user.id} <KEY>`"
        await context.bot.send_message(chat_id=ADMIN_ID, text=admin_text, parse_mode="Markdown")

    elif data == "profile":
        await query.edit_message_text(f"👤 Your ID: `{query.from_user.id}`\nBalance: ₹0.00", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="main")]]))

    elif data == "support":
        await query.edit_message_text("💬 Contact Admin: @nageshsahoo01", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="main")]]))

    elif data == "main":
        await start(update, context)

# Admin Command: /sendkey <user_id> <key>
async def send_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /sendkey <user_id> <key>")
        return

    user_id = context.args[0]
    key = context.args[1]
    
    try:
        await context.bot.send_message(chat_id=user_id, text=f"🎉 **Payment Verified!**\n\n🔑 Your Key: `{key}`\n\nEnjoy BALA MOD!", parse_mode="Markdown")
        await update.message.reply_text(f"✅ Key delivered to {user_id}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("sendkey", send_key))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()

if __name__ == "__main__":
    main()
