
---
title: Robocoders.ai Agent Interaction
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 4.44.1
app_file: app.py
pinned: false
---

# Robocoders.ai Agent Interaction

This Hugging Face Space provides an enhanced interface to interact with Robocoders.ai agents. You can select an agent (GeneralCodingAgent, RepoAgent, or FrontEndAgent) and provide a task for the agent to perform.

## Features

- Interactive chat interface with Robocoders.ai agents
- Support for multiple agent types
- Chat history saving functionality
- Improved error handling and user feedback
- Responsive design with Gradio's Soft theme

## How to use

1. Choose an agent from the dropdown menu.
2. Enter your task or question in the text box.
3. Click "Submit" or press Enter to send your request to the selected agent.
4. The agent's response will appear in the chat interface below.
5. Use the "Clear Chat" button to start a new conversation.
6. Click "Save Chat History" to save the current conversation to a JSON file.

## Note

This application uses the Robocoders.ai API to interact with the agents. Make sure you have a valid API token to use this application. Set your API token as an environment variable named `ROBOCODERS_API_TOKEN`.

## Development

To run this project locally:

1. Clone the repository
2. Install the required dependencies: `pip install -r requirements.txt`
3. Set your Robocoders.ai API token: `export ROBOCODERS_API_TOKEN=your_token_here`
4. Run the application: `python app.py`

## Contributing

For more information on contributing to this project or to explore other AI-related projects, please visit [CABLord's GitHub](https://github.com/CABLord).

## License

This project is open-source and available under the MIT License.
