# Simple WhatsApp Bot in Python for Beginners

This repository contains a basic WhatsApp bot written in Python, ideal for developers who are just starting out. The bot responds to various commands with text messages and images. With straightforward setup steps and detailed comments in the code, this bot is designed to help beginners understand API integration with WhatsApp.

## Getting Started

Follow these steps to set up and run the bot:

### Prerequisites

1. **Get Your API Token**
   - Obtain an API token from [Whapi.Cloud](https://whapi.cloud) and place it in `.env`.

2. **Set Up Webhook URL**
   - Get a webhook URL to receive incoming messages. If you need help with setting up the webhook, refer to our knowledge base article [Where to Find the Webhook URL](https://support.whapi.cloud/help-desk/receiving/webhooks/where-to-find-the-webhook-url).
   - We recommend using a local environment for testing, such as **NGROK**, to expose a local server to the internet.
1. **Download Ngrok** from the official website and extract it.
2. Open the terminal and navigate to the folder where Ngrok is stored.
3. Run `./ngrok http PORT_NUMBER`, replacing `PORT_NUMBER` with the port your Express server is running on locally.
Now you should have a public URL that you can use as a URL for your webhook.
   - Set your webhook URL in the **channel settings** on the Whapi.Cloud dashboard.
  
3. **Setting Up Your Bot**
Follow these steps to get the bot running:
- Navigate to the directory containing the bot’s files: `cd /path/to/bot`
- Install the required dependencies: `pip install -r requirements.txt`
- Run the bot: `python index.py`

   
For more detailed instructions on setup and configuration, you can watch our tutorial video on [YouTube](https://youtu.be/GhsRJBXztoc).

***

## Script Overview

This bot's script contains helpful comments throughout, making it easy to understand the flow and how each function works. Here's a breakdown of the main parts:

- **`files/`**: Stores media files, such as images, that the bot sends.
- **`.env`**: Contains configuration variables like the API token and base URL.
- **`index.py`**: The main Python script where the bot’s logic resides.
- **`requirements.txt`**: Lists all necessary Python packages.

### Main Logic

This is where the primary logic of the bot resides. It:
- Filters incoming messages (only non-outgoing messages are processed).
- Extracts the sender's phone number and the text content of the message.
- Uses a switch statement to respond with different messages or images based on the command received.

### Additional Information

Each function is commented to make it easier for beginners to understand how the bot works step by step. Should you have any questions or need further assistance, our support team is available and ready to help.

Happy coding!

