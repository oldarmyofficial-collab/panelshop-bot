
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "8894345960:AAE6iepstgfDnhMQlLKe-_L5y-aMXD84BoA"
ADMIN_USERNAME = "nageshsahoo01" # Apna Telegram username yahan sahi daalein
UPI_ID = "nageshsahoo01@upi"

# Admin check function
def is_admin(username):
    return username == ADMIN_USERNAME

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = (f"🔥 **BALA MOD APK STORE** 🔥\n"
            f"👋 Hello {user.first_name}!\n"
            f"🆔 Your ID: `{user.id}`\n\n"
            f"Niche diye gaye buttons se shop ya account manage karein:")
    
    keyboard = [
        [InlineKeyboardButton("🛒 Shop Now", callback_data="shop"), InlineKeyboardButton("💬 Admin Support", url=f"https://t.me/{ADMIN_USERNAME}")],
    ]
    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    
    if data == "shop":
        keyboard = [
            [InlineKeyboardButton("⏰ 1 Hour — ₹33.00", callback_data="buy_1h"), InlineKeyboardButton("⏰ 3 Hours — ₹67.50", callback_data="buy_3h")],
            [InlineKeyboardButton("📅 1 Day — ₹432.00", callback_data="buy_1d")],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu")]
        ]
        await query.edit_message_text("🛒 **Choose duration:**", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("buy_"):
        price = "33.00" if "1h" in data else "67.50" if "3h" in data else "432.00"
        text = (f"💰 **Amount to Pay:** ₹{price}\n"
                f"📲 **UPI ID:** `{UPI_ID}`\n\n"
                f"Payment karne ke baad screenshot aur UTR mujhe (@{ADMIN_USERNAME}) ko bhejen.\n"
                f"Button daba kar confirm karein ki aapne payment kar diya hai.")
        keyboard = [[InlineKeyboardButton("✅ I have paid", callback_data="confirm_pay")], [InlineKeyboardButton("🔙 Back", callback_data="shop")]]
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "confirm_pay":
        await query.edit_message_text("⏳ **Payment received.**\nAdmin verification pending hai. Thodi der wait karein, main aapko key bhej dunga.")

    elif data == "main_menu":
        await start(update, context)

# Admin Command: /sendkey <user_id> <key>
async def send_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.username):
        await update.message.reply_text("❌ Aap Admin nahi hain!")
        return
    
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /sendkey <user_id> <key>")
        return

    user_id = context.args[0]
    key = context.args[1]
    
    try:
        await context.bot.send_message(chat_id=user_id, text=f"🎉 **Payment Verified!**\n\n🔑 **Your Key:** `{key}`\n\nEnjoy using BALA MOD APK!", parse_mode="Markdown")
        await update.message.reply_text(f"✅ Key successfully sent to {user_id}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("sendkey", send_key)) # Admin command register kiya
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()

if __name__ == "__main__":
    main()
