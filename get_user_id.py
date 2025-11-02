"""
Simple script to get user ID from Telegram bot
"""

import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8305397344:AAER-Kpnczu6kPPC_5jfmHs7rKoZVAuAAHE"

async def log_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log user information"""
    user = update.effective_user
    chat = update.effective_chat
    
    print("="*60)
    print("USER INFORMATION:")
    print(f"User ID: {user.id}")
    print(f"Username: @{user.username if user.username else 'N/A'}")
    print(f"First Name: {user.first_name}")
    print(f"Last Name: {user.last_name if user.last_name else 'N/A'}")
    print(f"Chat ID: {chat.id}")
    print("="*60)
    
    await update.message.reply_text(
        f"✅ Ihre User ID: `{user.id}`\n\n"
        f"Diese ID wird jetzt zur Whitelist hinzugefügt!",
        parse_mode='Markdown'
    )

def main():
    """Run the bot"""
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers for all messages
    app.add_handler(MessageHandler(filters.ALL, log_user))
    app.add_handler(CommandHandler("start", log_user))
    
    print("🔍 Waiting for user message...")
    print("Send any message to your bot now!")
    
    app.run_polling()

if __name__ == "__main__":
    main()

