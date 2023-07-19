import time
from typing import List, Dict
import uuid
import requests

from src.config import HOME_REPO, API_KEY, MAX_TOKENS
from src.constants import MODEL, URL, SYSTEM_PROMPT


def read_knowledge_base():
    with open(f'{HOME_REPO}/tmp/knowledge_base.txt') as f:
        return f.read()


def chat_with_chatgpt(prompt=''):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    json_payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": read_knowledge_base()},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": MAX_TOKENS,
        "temperature": 0.7,
    }
    res = requests.post(URL, headers=headers, json=json_payload).json()
    if "error" in res:
        return res["error"]['message']
    return res['choices'][0]['message']['content']


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
        json_data = {"model": MODEL,
                     "messages": messages,
                     "temperature": 0.7}
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=json_data,
            )
            return response.json()["choices"][0]["message"]
        except Exception as e:
            print("Unable to generate ChatCompletion response")
            print(f"Exception: {e}")
            return e


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
