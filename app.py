
import gradio as gr
import requests
import json
import os
from datetime import datetime

# API Configuration
API_URL = "https://api.robocoders.ai"
ACCESS_TOKEN = os.environ.get("ROBOCODERS_API_TOKEN", "your_default_token_here")

# Create session with the API
def create_session():
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(f"{API_URL}/create-session", headers=headers)
    if response.status_code == 200:
        return response.json()["sid"]
    else:
        raise Exception(f"Failed to create session: {response.text}")

# Chat with the selected agent
def chat_with_agent(session_id, agent, prompt):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "sid": session_id,
        "prompt": prompt,
        "agent": agent
    }
    response = requests.post(f"{API_URL}/chat", headers=headers, json=data)
    print("Raw response text:", response.text)  # Debugging raw response
    if response.status_code == 200:
        if response.text.strip() == "":
            raise Exception("Agent returned an empty response.")

        try:
            return response.json()
        except json.JSONDecodeError as e:
            raise Exception(f"JSON decode error: {e} - Response text: {response.text}")
    else:
        raise Exception(f"Failed to chat with agent: {response.text}")

# Initialize chatbot session
class ChatBot:
    def __init__(self):
        self.session_id = create_session()
        self.history = []

    def interact(self, agent, message):
        try:
            response = chat_with_agent(self.session_id, agent, message)
            formatted_response = json.dumps(response, indent=2)
            self.history.append((message, formatted_response))
            return self.history
        except Exception as e:
            error_message = f"Error: {str(e)}"
            print(error_message)  # Log the error
            self.history.append((message, error_message))
            return self.history

    def save_history(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"chat_history_{timestamp}.json"
        with open(filename, "w") as f:
            json.dump(self.history, f, indent=2)
        return filename

# Instantiate the chatbot
chat_bot = ChatBot()

# User Input Function
def user_input(agent, message, history):
    return "", history + [(message, None)]

def format_response(response):
    """
    Formats the agent's response for better readability.
    """
    if not response:
        return "No response received from the agent."

    try:
        message = response.get("message", "No message provided.")
        action = response.get("action", "No action specified.")
        timestamp = response.get("timestamp", "No timestamp available.")
        args = response.get("args", {})

        formatted_message = f"**Agent Message:**\n{message}\n\n"

        if action == "delegate":
            formatted_message += f"**Delegated to:** {args.get('agent', 'Unknown Agent')}\n"
            formatted_message += f"**Reason:** {args.get('thought', 'No reason provided.')}\n"

        elif action == "run":
            formatted_message += f"**Command to Execute:**\n{args.get('command', 'No command provided.')}\n"

        elif action == "run_ipython":
            formatted_message += f"**Python Code to Execute:**\n```python\n{args.get('code', 'No code provided.')}\n```\n"

        formatted_message += f"**Timestamp:** {timestamp}\n"
        if args.get("wait_for_response"):
            formatted_message += "**Waiting for your input...**\n"

        return formatted_message
    except Exception as e:
        return f"Error formatting response: {str(e)}"

def bot_response(agent, history):
    """
    Handles the bot's response and formats it for display.
    """
    user_message = history[-1][0]  # Get the user's message
    try:
        bot_responses = chat_bot.interact(agent, user_message)
        last_response = bot_responses[-1][1]  # Get the latest bot response

        # Check if the response is valid
        if "Error:" in last_response:
            history[-1] = (user_message, last_response)  # Display error directly
        else:
            parsed_response = json.loads(last_response)
            formatted_response = format_response(parsed_response)
            history[-1] = (user_message, formatted_response)
    except json.JSONDecodeError as e:
        error_message = f"Error: Failed to parse the agent's response. Details: {str(e)}"
        history[-1] = (user_message, error_message)
    except Exception as e:
        error_message = f"Error: {str(e)}"
        history[-1] = (user_message, error_message)
    return history

def save_chat_history():
    filename = chat_bot.save_history()
    return f"Chat history saved to {filename}"

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# Robocoders.ai Agent Interaction")
    gr.Markdown("Interact with AI agents to assist with various coding tasks.")
    
    with gr.Row():
        with gr.Column(scale=2):
            agent_selector = gr.Dropdown(
                ["GeneralCodingAgent", "RepoAgent", "FrontEndAgent"], 
                label="Select Agent", 
                value="GeneralCodingAgent"
            )
        with gr.Column(scale=1):
            save_button = gr.Button("Save Chat History")
    
    chatbot_ui = gr.Chatbot(label="Chat with Robocoders Agent", height=400)
    user_msg = gr.Textbox(label="Enter your message", placeholder="Type your message here...")
    
    with gr.Row():
        submit_button = gr.Button("Submit", variant="primary")
        clear_button = gr.Button("Clear Chat")
    
    gr.Markdown("For more information, visit [CABLord's GitHub](https://github.com/CABLord)")
    
    user_msg.submit(user_input, [agent_selector, user_msg, chatbot_ui], [user_msg, chatbot_ui], queue=False).then(
        bot_response, [agent_selector, chatbot_ui], chatbot_ui
    )
    
    submit_button.click(user_input, [agent_selector, user_msg, chatbot_ui], [user_msg, chatbot_ui], queue=False).then(
        bot_response, [agent_selector, chatbot_ui], chatbot_ui
    )
    
    clear_button.click(lambda: None, None, chatbot_ui, queue=False)
    save_button.click(save_chat_history, None, gr.Textbox(label="Save Status"))

# Launch the Gradio app
if __name__ == "__main__":
    demo.launch()
