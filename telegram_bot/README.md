



# AI Backlog Assistant Telegram Bot

## Overview

This Telegram bot provides a convenient interface for users to interact with the AI Backlog Assistant system. Users can:

- Get system status and information
- Upload documents for analysis
- Receive recommendations and notifications
- Manage notification settings

## Features

### Commands

- `/start` - Show welcome message with available commands
- `/help` - Show help information
- `/status` - Get current system status
- `/upload` - Upload a document for analysis
- `/notifications` - Manage notification settings
- `/notifications_enable` - Enable notifications
- `/notifications_disable` - Disable notifications

### Document Upload

Users can upload documents in various formats (PDF, DOCX, TXT, CSV) for analysis. The bot will:

1. Receive the document
2. Send it for processing through the pipeline system
3. Return recommendations and analysis results

### Notifications

Users can enable/disable notifications and receive updates about:

- New recommendations
- System status changes
- Important events and alerts

## Setup

### Requirements

- Python 3.7+
- `python-telegram-bot` library

### Installation

1. Install the required library:
   ```bash
   pip install python-telegram-bot
   ```

2. Set your Telegram bot token:
   - Create a new bot using BotFather on Telegram
   - Get the API token
   - Set it as an environment variable or replace in the code

### Running the Bot

1. Start the bot:
   ```bash
   python bot.py
   ```

2. Find your bot on Telegram and start a conversation

## Integration with Pipeline System

The bot is designed to integrate with the AI Backlog Assistant pipeline system. When a document is uploaded:

1. The document is saved locally
2. It's processed through the pipeline system
3. Results and recommendations are returned to the user

## Future Enhancements

- Add more detailed analytics commands
- Implement user authentication
- Add support for inline queries
- Integrate with web interface for seamless experience

## License

This project is licensed under the MIT License.

