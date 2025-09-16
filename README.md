# Telegram Quote Bot

## Description
This bot sends random quotes to users upon request, allows translation, 
adding to favorites, viewing history, and deleting favorites.  
It also sends a daily random quote to all users at a specified time.

## Bot Commands
- `/start` — welcome message and instructions  
- `/help` — help and guidance  
- `/quote` — get a random quote  
- `/history` — view user's quote history  
- `/show_favorites` — view favorite quotes  

## Daily Broadcast
A daily random quote is sent to all users at 11:11 AM.  
The scheduler runs in a separate thread using the `schedule` module.

## Technologies Used
- pyTelegramBotAPI  
- SQLite (via peewee)  
- python-dotenv  
- schedule  
- aiohttp  
- deep-translator 

## Installation
1. Clone the repository:
bash
git clone <repository_link>
cd <project_folder>
2. (Optional) Create and activate a virtual environment.
3. Install dependencies:
pip install -r requirements.txt
4. Configure the .env file with your bot token and other settings.
5. Run the bot:
The database will be initialized.
Telegram bot commands will be registered.
Daily quote scheduler will start.
Infinite polling will be activated.

