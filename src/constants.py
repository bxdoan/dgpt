
MODEL = 'gpt-3.5-turbo-16k'
URL = f"https://api.openai.com/v1/chat/completions"
SYSTEM_PROMPT = """
    You are a helpful AI assistant. You answer the user's queries.
    NEVER make up an answer.
    If you don't know the answer,
    just respond with "I don't know".
"""