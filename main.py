import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

BOT_TOKEN = "8894345960:AAE6iepstgfDnhMQlLKe-_L5y-aMXD84BoA"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_text = (
        f"🔥 **WELCOME TO PANELSHOP STORE** 🔥\n\n"
        f"👋 Hello {user.first_name}!\n"
        f"🆔 Your ID: `{user.id}`\n\n"
        f"Niche diye gaye buttons se shop ya balance add karein:"
    )

    keyboard = [
        [
            InlineKeyboardButton("🛒 Shop Now", callback_data="shop"),
            InlineKeyboardButton("💳 Add Balance", callback_data="add_bal"),
        ],
        [
            InlineKeyboardButton("👤 My Profile", callback_data="profile"),
            InlineKeyboardButton("📜 My Orders", callback_data="orders"),
        ],
        [
            InlineKeyboardButton(
                "📞 Admin Support", url="https://t.me/indsahoofam"
            )
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(
            welcome_text, reply_markup=reply_markup, parse_mode="Markdown"
        )
    elif update.callback_query:
        await update.callback_query.message.edit_text(
            welcome_text, reply_markup=reply_markup, parse_mode="Markdown"
        )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "shop":
        keyboard = [
            [
                InlineKeyboardButton(
                    "⚡ 1 Hour Key - ₹20", callback_data="buy_1h"
                )
            ],
            [
                InlineKeyboardButton(
                    "🔥 24 Hour Key - ₹100", callback_data="buy_24h"
                )
            ],
            [InlineKeyboardButton("⬅️ Back", callback_data="main_menu")],
        ]
        await query.message.edit_text(
            "🛒 **SELECT PRODUCT:**\n\nApna desired plan select karein:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )

    elif query.data == "add_bal":
        pay_url = f"https://panelshop-production.up.railway.app/pay?user_id={query.from_user.id}"
        keyboard = [
            [InlineKeyboardButton("📲 Pay via UPI QR", url=pay_url)],
            [InlineKeyboardButton("⬅️ Back", callback_data="main_menu")],
        ]
        await query.message.edit_text(
            "💳 **ADD BALANCE (Auto Gateway)**\n\n"
            "Niche button par click karke Instant Payment karein. Payment complete hote hi balance auto-add ho jayega!",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )

    elif query.data == "profile":
        profile_text = (
            f"👤 **YOUR PROFILE**\n\n"
            f"• Name: {query.from_user.first_name}\n"
            f"• ID: `{query.from_user.id}`\n"
            f"• Wallet Balance: ₹0.00\n"
        )
        keyboard = [[InlineKeyboardButton("⬅️ Back", callback_data="main_menu")]]
        await query.message.edit_text(
            profile_text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )

    elif query.data == "main_menu":
        await start(update, context)


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
