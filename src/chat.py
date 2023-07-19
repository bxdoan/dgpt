import time
from typing import List, Dict
import uuid
import requests

from src.config import API_KEY, PREPROCESSING_FILE
from src.constants import MODEL, URL, SYSTEM_PROMPT
from src import utils

logger = utils.get_logger(__name__)


def read_knowledge_base():
    with open(f'{PREPROCESSING_FILE}') as f:
        return f.read()


class Conversation:
    """
    This class represents a conversation with the ChatGPT model.
    It stores the conversation history in the form of a list of
    messages.
    """
    def __init__(self):
        self.conversation_history: List[Dict] = []

    def add_message(self, role, content):
        message = {"role": role, "content": content}
        self.conversation_history.append(message)


class ChatSession:
    """
    Represents a chat session.
    Each session has a unique id to associate it with the user.
    It holds the conversation history
    and provides functionality to get new response from ChatGPT
    for user query.
    """

    def __init__(self):
        self.session_id = str(uuid.uuid4())
        self.conversation = Conversation()
        self.conversation.add_message("system", SYSTEM_PROMPT)
        self.conversation.add_message("user", read_knowledge_base())

    def get_messages(self) -> List[Dict]:
        """
        Return the list of messages from the current conversation
        """
        # Exclude the SYSTEM_PROMPT when returning the history
        if len(self.conversation.conversation_history) == 1:
            return []
        return self.conversation.conversation_history[1:]

    def get_chatgpt_response(self, user_message: str) -> str:
        """
        For the given user_message,
        get the response from ChatGPT
        """
        self.conversation.add_message("user", user_message)
        try:
            chatgpt_response = self._chat_completion_request(
                self.conversation.conversation_history
            )
            chatgpt_message = chatgpt_response.get("content")
            self.conversation.add_message("assistant", chatgpt_message)
            return chatgpt_message
        except Exception as e:
            print(e)
            return "something went wrong"

    def _chat_completion_request(self, messages: List[Dict]):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + API_KEY,
        }
        logger.info(f"History {self.session_id} len {len(messages)}")
        json_data = {
            "model": MODEL,
            "messages": messages,
            "temperature": 0.7
        }
        try:
            response = requests.post(
                URL,
                headers=headers,
                json=json_data,
            )
            res = response.json()
            logger.info(f"ChatCompletion response: {res}")
            return res['choices'][0]['message']
        except Exception as e:
            logger.error(f"Unable to generate ChatCompletion response\nException: {e}")
            return e


chat_sessions: Dict[str, ChatSession] = {}


def _get_user_session(chat_session_id = None) -> ChatSession:
    """
    If a ChatSession exists for the current user return it
    Otherwise create a new session, add it into the session.
    """

    if chat_session_id:
        chat_session = chat_sessions.get(chat_session_id)
        if not chat_session:
            chat_session = ChatSession()
            chat_sessions[chat_session.session_id] = chat_session
    else:
        chat_session = ChatSession()
        chat_sessions[chat_session.session_id] = chat_session
    return chat_session


if __name__ == '__main__':
    cs = ChatSession()
    # Interactive questions and answers
    while True:
        query = input("\nEnter a query: ")
        if query == "exit":
            break
        if query.strip() == "":
            continue

        # Get the answer from the chain
        start = time.time()
        answer = cs.get_chatgpt_response(query)
        end = time.time()

        # Print the result
        print("\n\n> Question:")
        print(query)
        print(f"\n> Answer (took {round(end - start, 2)} s.):")
        print(answer)
