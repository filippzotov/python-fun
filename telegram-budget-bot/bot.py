import telebot
from bot_token import BOT_TOKEN
import database as db

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    """Send a welcome message when the command /start is issued."""
    bot.send_message(
        message.chat.id,
        "Welcome to BudgetBot! Type /help for instructions on how to use the bot.",
    )


@bot.message_handler(commands=["help"])
def help_command(message):
    """Send a message with instructions on how to use the bot."""
    help_text = """
    BudgetBot allows you to track your expenses and manage your budget.
    Here are the available commands:
    /start - Start the bot and get a welcome message.
    /help - Show this help message.
    /create - create user profile, use in the format: /create <budget>
    /delete - delete yourself from database
    /addexpense - Add a new expense in the format: /addexpense <amount> <description>.
    /viewexpenses - View your current expenses.
    """
    bot.send_message(message.from_user.id, help_text)


@bot.message_handler(commands=["create"])
def create_user(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    message_text = message.text.split()
    if len(message_text) == 2 and message_text[1].isdigit():
        amount = int(message_text[1])
        if db.user_exists(session, user_id):
            bot.send_message(message.chat.id, "User already exist")

        else:
            db.add_user(session, user_id, user_name, amount)
            bot.send_message(message.chat.id, f"User created: {user_name} - {amount}")
    else:
        bot.send_message(
            message.chat.id,
            "Invalid format! Please use: /create <amount>",
        )


@bot.message_handler(commands=["addexpense"])
def add_expenses(message):
    """Add a new expense."""
    user_id = message.from_user.id
    message_text = message.text.split()
    if len(message_text) >= 3 and message_text[1].isdigit():
        amount = int(message_text[1])
        description = " ".join(message_text[2:])
        if db.user_exists(session, user_id):
            db.add_expense(session, description, user_id, amount)
            bot.send_message(
                message.chat.id, f"Expense added: {amount} - {description}"
            )
        else:
            bot.send_message(
                message.chat.id, f"You need to create user, use /create command"
            )
    else:
        bot.send_message(
            message.chat.id,
            "Invalid format! Please use: /addexpense <amount> <description>",
        )


@bot.message_handler(commands=["viewexpenses"])
def view_expenses(message):
    """View the user's current expenses."""
    user_id = message.from_user.id
    if db.user_exists(session, user_id):
        message_text = db.get_user_expenses(session, user_id)
        budget = db.get_budget(session, user_id)
        money_left = db.get_money_left(session, user_id)
        message_text += f"Budget - {budget}\nMoney left - {money_left}\n"
    else:
        message_text = "No expenses recorded yet."
    bot.send_message(message.chat.id, message_text)


@bot.message_handler(commands=["delete"])
def view_expenses(message):
    user_id = message.from_user.id
    if db.user_exists(session, user_id):
        db.delete_user(session, user_id)
        message_text = "User deleted"
    else:
        message_text = "No such user"
    bot.send_message(message.chat.id, message_text)


global session
session = db.connect_db()
bot.infinity_polling()
