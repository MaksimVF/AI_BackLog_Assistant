


"""
Telegram Bot for AI Backlog Assistant
"""

import logging
import os
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Telegram Bot Token (replace with your actual token)
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', 'YOUR_TELEGRAM_BOT_TOKEN_HERE')

def start(update: Update, context: CallbackContext) -> None:
    """Send a welcome message when the command /start is issued."""
    update.message.reply_text(
        'Welcome to AI Backlog Assistant Bot!\n\n'
        'Available commands:\n'
        '/start - Show this welcome message\n'
        '/help - Show help information\n'
        '/status - Get system status\n'
        '/upload - Upload a document for analysis\n'
        '/notifications - Manage your notifications\n'
    )

def help_command(update: Update, context: CallbackContext) -> None:
    """Send help information."""
    update.message.reply_text(
        'Help information:\n\n'
        'This bot helps you manage your backlog and get recommendations.\n\n'
        'Commands:\n'
        '/start - Welcome message\n'
        '/help - This help information\n'
        '/status - Check system status\n'
        '/upload - Upload documents\n'
        '/notifications - Manage notifications\n'
    )

def status(update: Update, context: CallbackContext) -> None:
    """Send system status."""
    update.message.reply_text(
        'System Status:\n'
        '✅ Online\n'
        '📊 Processing: 5 tasks\n'
        '⏳ Last update: 2 minutes ago'
    )

def upload(update: Update, context: CallbackContext) -> None:
    """Handle file upload."""
    update.message.reply_text(
        'Please upload a file for analysis.\n'
        'Supported formats:\n'
        '📄 Documents: PDF, DOCX, TXT, CSV\n'
        '🎥 Videos: MP4, AVI, MOV\n'
        '🎧 Audio: MP3, WAV, OGG'
    )

def handle_document(update: Update, context: CallbackContext) -> None:
    """Handle incoming documents, videos, and audio files."""
    message = update.message
    file_id = None
    file_name = "unknown"
    file_size = 0
    mime_type = "application/octet-stream"
    file_type = "📄 Document"

    # Handle different message types
    if message.document:
        doc = message.document
        file_id = doc.file_id
        file_name = doc.file_name
        file_size = doc.file_size
        mime_type = doc.mime_type
        if mime_type.startswith('video/'):
            file_type = "🎥 Video"
        elif mime_type.startswith('audio/'):
            file_type = "🎧 Audio"

    elif message.video:
        vid = message.video
        file_id = vid.file_id
        file_name = f"video_{vid.file_id}.mp4"
        file_size = vid.file_size
        mime_type = "video/mp4"
        file_type = "🎥 Video"

    elif message.audio:
        aud = message.audio
        file_id = aud.file_id
        file_name = f"audio_{aud.file_id}.mp3"
        file_size = aud.file_size
        mime_type = "audio/mpeg"
        file_type = "🎧 Audio"

    if file_id:
        # Download the file
        file = context.bot.get_file(file_id)
        file_path = f'downloads/{file_name}'
        file.download(file_path)

        update.message.reply_text(
            f'File received:\n'
            f'{file_type} Name: {file_name}\n'
            f'📏 Size: {file_size} bytes\n'
            f'⏳ Processing...'
        )

        # Integrate with the pipeline system
        try:
            from pipelines.main_pipeline_coordinator import MainPipelineCoordinator

            # Create a pipeline coordinator
            coordinator = MainPipelineCoordinator()

            # Process the document through the pipeline
            result = coordinator.process_end_to_end(
                document_id=f"telegram_{file_id}",
                raw_content=file_path,
                metadata={
                    'source': 'telegram',
                    'file_name': file_name,
                    'file_size': file_size,
                    'mime_type': mime_type,
                    'file_type': file_type,
                    'user_id': update.effective_user.id,
                    'chat_id': update.effective_chat.id
                }
            )

            # Prepare response based on pipeline results
            response_text = _format_pipeline_results(result)

            # Send the response
            context.job_queue.run_once(
                lambda ctx: ctx.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=response_text
                ),
                when=2,  # Send response after processing
                context=update.effective_chat.id
            )

        except Exception as e:
            error_msg = f"❌ Error processing document: {str(e)}"
            update.message.reply_text(error_msg)
    else:
        update.message.reply_text('Please send a valid file.')

def notifications(update: Update, context: CallbackContext) -> None:
    """Manage notifications."""
    update.message.reply_text(
        'Notification settings:\n\n'
        'Current status: ✅ Enabled\n\n'
        'To disable notifications, use /notifications disable\n'
        'To enable notifications, use /notifications enable'
    )

def notifications_disable(update: Update, context: CallbackContext) -> None:
    """Disable notifications."""
    update.message.reply_text('❌ Notifications disabled')

def notifications_enable(update: Update, context: CallbackContext) -> None:
    """Enable notifications."""
    update.message.reply_text('✅ Notifications enabled')

def _format_pipeline_results(result: dict) -> str:
    """Format pipeline results for Telegram response."""
    try:
        # Extract key information from pipeline results
        modality = result.get('modality', 'unknown')
        intent = result.get('intent', 'unknown')
        entities = result.get('entities', {})
        recommendations = result.get('recommendations', [])

        # Build response text
        response = "✅ Analysis complete!\n\n"
        response += f"📋 **Document Analysis**\n"
        response += f"🔍 Modality: {modality}\n"
        response += f"🎯 Intent: {intent}\n"

        if entities:
            response += "\n🏷️ **Key Entities**\n"
            for entity_type, entity_values in entities.items():
                if isinstance(entity_values, list):
                    response += f"{entity_type}: {', '.join(entity_values[:3])}\n"
                else:
                    response += f"{entity_type}: {entity_values}\n"

        if recommendations:
            response += "\n💡 **Recommendations**\n"
            for i, rec in enumerate(recommendations, 1):
                response += f"{i}. {rec}\n"
        else:
            response += "\n💡 **Recommendations**\n"
            response += "No specific recommendations generated."

        return response

    except Exception as e:
        return f"❌ Error formatting results: {str(e)}"

def error(update: Update, context: CallbackContext) -> None:
    """Log errors caused by updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("upload", upload))
    app.add_handler(CommandHandler("notifications", notifications))
    app.add_handler(CommandHandler("notifications_disable", notifications_disable))
    app.add_handler(CommandHandler("notifications_enable", notifications_enable))

    # Register message handlers
    app.add_handler(MessageHandler(filters.DOCUMENT, handle_document))
    app.add_handler(MessageHandler(filters.VIDEO, handle_document))
    app.add_handler(MessageHandler(filters.AUDIO, handle_document))

    # Register error handler
    app.add_error_handler(error)

    # Create downloads directory if it doesn't exist
    os.makedirs('downloads', exist_ok=True)

    # Start the Bot
    logger.info("Starting Telegram Bot...")
    app.run_polling()

if __name__ == '__main__':
    main()



