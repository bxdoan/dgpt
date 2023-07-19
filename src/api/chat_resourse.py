from src.chat import _get_user_session
from src.utils import make_response, get_logger

logger = get_logger(__name__)


class Chat(object):

    def on_post(self, req, resp):
        body = req.media or (req.context.get('request') or {})
        message: str = body.get('message')
        session_id: str = body.get('session_id')
        chat_session = _get_user_session(session_id)
        try:
            chatgpt_message = chat_session.get_chatgpt_response(message)
            data = {
                'message': chatgpt_message,
                'session_id': chat_session.session_id,
            }
            return make_response(resp, data)
        except Exception as e:
            logger.error(f'Error: {e}')
            data = {
                'message': "I don't know",
                'session_id': None,
            }
            return make_response(resp, data)
