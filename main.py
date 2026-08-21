import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- CONFIGURATION ---
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
ADMIN_ID = 123456789  # Apna Telegram ID yahan daalo (userinfobot se nikalo)
UPI_ID = "nageshsahoo01@upi"

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

    text = f"🏢 — BALA MOD SHOP — 🏢\n\n👋 Welcome, {user.first_name}!\n\n🚀 Click Shop Now to Start!"
    keyboard = [
        [InlineKeyboardButton("🛍️ Shop Now", callback_data="shop")],
        [InlineKeyboardButton("👤 Profile", callback_data="profile"), InlineKeyboardButton("💬 Support", callback_data="support")]
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "shop":
        keyboard = [
            [InlineKeyboardButton("⏰ 1 Hour - ₹33", callback_data="buy_1h")],
            [InlineKeyboardButton("📅 1 Day - ₹432", callback_data="buy_1d")],
            [InlineKeyboardButton("🔙 Back", callback_data="main")]
        ]
        await query.edit_message_text("📦 Select your plan:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("buy_"):
        plan = data.split("_")[1]
        price = "33" if plan == "1h" else "432"
        text = f"💳 **PAYMENT DETAILS**\n\nAmount: ₹{price}\nUPI ID: `{UPI_ID}`\n\n*Payment karne ke baad neeche button dabayein.*"
        keyboard = [[InlineKeyboardButton("✅ I Have Paid", callback_data=f"paid_{plan}")], [InlineKeyboardButton("🔙 Back", callback_data="shop")]]
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("paid_"):
        plan = data.split("_")[1]
        user = query.from_user
        await query.edit_message_text("⏳ Payment request received. Admin verify kar raha hai, wait karein.")
        
        # Admin ko notification bhejo
        admin_text = f"🔔 **NEW PAYMENT ALERT**\n\nUser: {user.first_name}\nID: `{user.id}`\nPlan: {plan}\n\nKey bhejne ke liye niche command use karein:\n`/sendkey {user.id} <KEY>`"
        await context.bot.send_message(chat_id=ADMIN_ID, text=admin_text, parse_mode="Markdown")

    elif data == "profile":
        await query.edit_message_text(f"👤 Your ID: `{query.from_user.id}`\nBalance: $0.00", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="main")]]))

    elif data == "support":
        await query.edit_message_text("💬 Contact Admin: @nageshsahoo01", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="main")]]))

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


