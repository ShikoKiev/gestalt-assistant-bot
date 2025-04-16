import logging
import os

from plugin_manager import PluginManager
from openai_helper import OpenAIHelper, default_max_tokens, are_functions_available
from telegram_bot import ChatGPTTelegramBot


def main():
    # Setup logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)

    # Check if the required environment variables are set
    required_values = ['TELEGRAM_BOT_TOKEN', 'OPENAI_API_KEY']
    missing_values = [value for value in required_values if os.environ.get(value) is None]
    if len(missing_values) > 0:
        logging.error(f'Missing required environment variables: {", ".join(missing_values)}')
        exit(1)

    # Setup configurations
    model = os.environ.get('OPENAI_MODEL', 'gpt-4o')
    functions_available = are_functions_available(model=model)
    max_tokens_default = default_max_tokens(model=model)
    openai_config = {
        'api_key': os.environ['OPENAI_API_KEY'],
        'show_usage': os.environ.get('SHOW_USAGE', 'false').lower() == 'true',
        'stream': os.environ.get('STREAM', 'true').lower() == 'true',
        'proxy': os.environ.get('PROXY', None) or os.environ.get('OPENAI_PROXY', None),
        'max_history_size': int(os.environ.get('MAX_HISTORY_SIZE', 15)),
        'max_conversation_age_minutes': int(os.environ.get('MAX_CONVERSATION_AGE_MINUTES', 180)),
        'assistant_prompt': os.environ.get('ASSISTANT_PROMPT', 'You are a helpful assistant.'),
        'max_tokens': int(os.environ.get('MAX_TOKENS', max_tokens_default)),
        'n_choices': int(os.environ.get('N_CHOICES', 1)),
        'temperature': float(os.environ.get('TEMPERATURE', 1.0)),
        'image
