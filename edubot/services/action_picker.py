""" This module contains the ActionPickerService class."""
#pylint: disable=import-error
import time
import json
import logging
import requests
from django.core.cache import cache
from decouple import config
from users.models import User
from services.action_table import ACTION_TABLE
from services.action_validator import ActionValidator

cache.clear()
print("Cache cleared", cache)




class ActionPickerService(object):
    """
        This class is responsible for picking the correct action to perform.
    """
    def __init__(self, payload):
        """Initialize the action validator."""
        self.action_table = ACTION_TABLE
        self.validator = ActionValidator()
        self.logger = logging.getLogger(__name__)
        self.payload = self.parse_payload(payload)
        self.session = cache.get(self.payload.get('phone_number'))

    def parse_payload(self, incoming_message):
        """Parse the action."""
        oringinal_payload = dict(incoming_message)
        print("PAYLOAD >>>> ", oringinal_payload)
            
        payload =  oringinal_payload['entry'][0]['changes'][0]['value']
        if payload.get('messages'):
            message = payload['messages'][0]
            contact = payload['contacts'][0]
            message_type = message['type']
            username = contact['profile']['name']
            phone_number = contact['wa_id']
            if message_type == "text":
                payload['body'] = message['text']['body']
            elif message_type == "button":
                payload['body'] = message['button']['payload']
            elif message_type == "interactive":
                if message['interactive']['type'] == "button_reply":
                    payload['body'] = message['interactive']['button_reply']['id']
                else:
                    payload['body'] = message['interactive']['list_reply']['id']
            elif message_type == "document":
                headers = {
                    'Authorization': 'Bearer ' + config('CLOUD_API_TOKEN')
                }
                file = requests.request("GET", url=f"https://graph.facebook.com/v15.0/{message['document']['id']}", headers=headers, data={}).json()
                payload['body'] = file.get('url')
                payload['file_name'] = file.get('name')

            payload['username'] = username
            payload['phone_number'] = phone_number
        else:  
            return None
        return payload

    def construct_response(self, response):
        """Construct the response."""
        print(f"Constructing response : ")
        
        if response["body"].get('response_type') == "interactive":
            print("Constructing interactive response : ")
            return {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": response.get('phone_number'),
                "type": "interactive",
                "interactive": json.dumps({
                    "type": "list",
                    "body": {
                        "text": f"{response['body'].get('text')}"
                    },
                    "action": {
                        "button": f"{response['body'].get('menu_name')}",
                        "sections": [
                            {
                                "title": "Select Option",
                                "rows": [
                                    {
                                        "id": item['id'],
                                        "title":  f"{item['name']}",
                                        "description": f"{item['description']}",
                                    } for item in response['body'].get('menu_items')
                                ]
                            }
                        ]
                    }
                })
            }
        
        elif response["body"].get('response_type') == "button":
            chat_response =  {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": response.get('phone_number'),
                "type": "interactive",
                "interactive": {
                    "type": "button",
                    "body": {
                        "text": f"{response['body'].get('text')}"
                    },
                    "action": {
                        "buttons": [
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "back",
                                    "title": "🔙 Back"
                                }
                            },
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "menu" if response["body"].get('menu') is None else f"{response['body'].get('menu')}",
                                    "title": "🏠 Menu" 
                                }
                            }
                        ]
                    }
                }
            }
            if response["body"].get('exclude_back'):
                chat_response["interactive"]["action"]["buttons"].pop(0)
            chat_response["interactive"] = json.dumps(chat_response["interactive"])
            return chat_response
        
        elif response["body"].get('response_type') == "download":
            return {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": response.get('phone_number'),
                "type": "interactive",
                "interactive": json.dumps({
                    "type": "button",
                    "body": {
                        "text": f"{response['body'].get('text')}"
                    },
                    "action": {
                        "buttons": [
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "download",
                                    "title": "📥 Download"
                                }
                            },
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "upload",
                                    "title": "📤 Upload"
                                }
                            }
                        ]
                    }
                })
            }

        elif response["body"].get('response_type') == "document":
            return {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": response.get('phone_number'),
                "type": "document",
                "document": json.dumps({
                    "link": "https://bow-space.com/media/resources/RAND_RR4367.pdf",
                    "caption": response["body"].get('caption'),
                })
            }

        elif response["body"].get('response_type') == "pay_download":
            resp = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": response.get('phone_number'),
                "type": "interactive",
                "interactive": {
                    "type": "button",
                    "body": {
                        "text": f"{response['body'].get('text')}"
                    },
                    "action": {
                        "buttons": [
                            {
                                "type": "reply",
                                "reply": {
                                    "id": f"payment_{response['body'].get('id')}",
                                    "title": "💳 Pay"
                                }
                            },
                            {
                                "type":
                                "reply",
                                "reply": {
                                    "id": f"download_{response['body'].get('id')}",
                                    "title": "📥 Download"
                                }
                            }
                        ]
                    }
                }
            }
            if response["body"].get('exclude_download'):
                resp["interactive"]["action"]["buttons"].pop(1)
            resp["interactive"] = json.dumps(resp["interactive"])
            return resp
        
        elif response["body"].get('response_type') == "pay":
            return {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": response.get('phone_number'),
                "type": "interactive",
                "interactive": json.dumps({
                    "type": "button",
                    "body": {
                        "text": f"{response['body'].get('text')}"
                    },
                    "action": {
                        "buttons": [
                        {
                            "type": "web_url",
                            "url": f"https://bow-space.com/paynow/{response['body'].get('id')}",
                            "title": "PayNow",
                            "webview_height_ratio": "full",
                            "messenger_extensions": True,
                        }
                    ]
                    }
                })
            }
        
        elif response["body"].get('response_type') == "video":
            return {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": response.get('phone_number'),
                "type": "video",
                "video": json.dumps({
                    "link": "https://bow-space.com/media/files/quizz/WhatsApp_Video_2023-01-28_at_06.42.06.mp4",
                    "caption": response["body"].get('text'),
                })
            }
        
        elif response["body"].get('response_type') == "tutorial":
            chat_response =  {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": response.get('phone_number'),
                "type": "interactive",
                "interactive": {
                    "type": "button",
                    "body": {
                        "text": f"{response['body'].get('text')}"
                    },
                    "action": {
                        "buttons": [
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "tutorial_prev",
                                    "title": "🔙 Back"
                                }
                            },
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "tutorial_next",
                                    "title": "🔜 Next"
                                }
                            }
                        ]
                    }
                }
            }
            if response["body"].get('exclude_back'):
                chat_response["interactive"]["action"]["buttons"].pop(0)
            if response["body"].get('exclude_next'):
                chat_response["interactive"]["action"]["buttons"][1]['reply']['id'] = "tutorial_finish"
                chat_response["interactive"]["action"]["buttons"][1]['reply']['title'] = "🏁 Finish"

            chat_response["interactive"] = json.dumps(chat_response["interactive"])
            return chat_response

        elif response["body"].get('response_type') == "image":
            return {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": response.get('phone_number'),
                "type": "image",
                "image": json.dumps({
                    "link": "https://bow-space.com/media/files/quizz/Screenshot_from_2023-01-29_09-13-50.png",
                    "caption": response["body"].get('text'),
                })
            }

        else:
            return {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": response.get('phone_number'),
                "type": "text",
                "text": json.dumps({
                    "preview_url": True,
                    "body":  response['body'].get('text')
                })
            }
            
    def get_action(self):
        """Get the action."""
        state = self.session.get('state') if self.session else None
        if state is None:
            state = "menu"
        return state

    def dispatch_action(self):
        """Dispatch the action."""

        if self.payload.get('body').lower() == "back":
            state = self.go_back()
        else:
            state = "menu" if self.payload.get('body').lower() in ["menu", "hi", "hello", "hie", "reset"] else self.get_action()
        print("Current state : ", state)

        if state == "menu" and not User.objects.filter(
            phone_number=self.payload.get('phone_number')
            ).exists():
            cache.delete(self.payload.get('phone_number'))
            state = "greet"

        print("Current STATE : ", state)
        if isinstance(state, list) and self.payload.get('body').lower() in state:
            print("State is a list")
            state = self.payload.get('body').lower()

        try:
            print("CALLING VALIDATOR :", self.action_table[state]['action_validator'])
            action = self.validator.registry[
                self.action_table[state]['action_validator']
            ](
                phone_number=self.payload.get('phone_number'),
                message=self.payload.get('body'),
                session=self.session,
                payload=self.payload
            )
        except (TypeError, KeyError):
            response = response = {
                "phone_number": self.payload.get('phone_number'),
                "body": {
                    "text": "Sorry, I didn't understand that. That could be an invalid option.\n\n_Please try again._",
                    "response_type": "text",
                   
                }
            }

            self.send_response(self.construct_response(response))
            return

        print("\n\nAction :")

        if action.get("is_valid"):
            next_action = self.action_table[state]['next_action_if_valid']
            response = {
                "phone_number": self.payload.get('phone_number'),
                "body": action.get("message") if action.get("message") else \
                    self.action_table[state]['valid_response'],
                "response_type": "text"
            }
        else:
            next_action = self.action_table[state]['next_action_if_invalid']
            response = {
                "phone_number": self.payload.get('phone_number'),
                "body": action.get('message'),
                "response_type": "text"
            }

        self.session = {
            "state": next_action, 
            "data": cache.get(
                self.payload.get('phone_number')
                ).get('data') if cache.get(self.payload.get('phone_number')) else {}
        }
        print("Next state :", state)
        print("Next action :", next_action)
        self.save_session(self.session)

        chatbot_response=self.construct_response(response)

        response = self.send_response(chatbot_response)

        # print("MESSAGE SENT RECEIPT >>>>||  ", response.json())

        history_payload = {
            "state": state,
            "response_type": action["message"].get('response_type'),
            "prev_response": chatbot_response,
            "data": self.session.get('data', {}),
        }
        self.history(history_payload)
        print("===================================================================================\n\n")
        if action.get('requires_controls') and response.status_code == 200:
            time.sleep(1)
            payload = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": self.payload.get('phone_number'),
                "type": "interactive",
                "interactive": json.dumps({
                    "type": "button",
                    "body": {
                        "text": "_Use control panel for naviation._"
                    },
                    "action": {
                        "buttons": [
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "tutorial_prev",
                                    "title": "🔙 Previous"
                                }
                            },
                            {
                                "type": "reply",
                                "reply": {
                                    "id": "tutorial_next",
                                    "title": "🔜 Forward "
                                }
                            }
                        ]
                    }
                })
            }
            self.send_response(payload)
        return

    def history(self, response):
        """Maintain history of the session."""
        phone_number = self.payload.get('phone_number')
        history = cache.get(f"{phone_number}_history", [])
        if history:
            if len(history)> 5:
                history.pop(0)
            history.append(response)
        else:
            history.append(response)
        cache.set(f"{phone_number}_history", history)
        return

    def go_back(self):
        """Go back to the previous state."""
        phone_number = self.payload.get('phone_number')
        history = cache.get(f"{phone_number}_history", [])
        if history:
            mark = cache.get(f"bookmark_{phone_number}", -2)
            cache.delete(f"bookmark_{phone_number}")
            print("SESSION : ", mark)
            prev_state = history.pop(mark)
            state = prev_state.get('state')
            self.session = {
                "state":state,
                "data": prev_state.get('data')
            }
            self.save_session(self.session)
        return self.session.get('state') if self.session else "menu"

    def send_response(self, response):
        """Send the response."""
        self.logger.info("Sending response : %s", response)
        url = f"https://graph.facebook.com/v15.0/{config('Phone_Number_ID')}/messages"
        response = requests.post(
            url=url,
            data=response,
            headers={'Authorization': f'Bearer {config("CLOUD_API_TOKEN")}'}
        )
        return response

    def save_session(self, session):
        """Save the session."""
        cache.set(self.payload.get('phone_number'), session, timeout=60*60*24*7)
        return session
