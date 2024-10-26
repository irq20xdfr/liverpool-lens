# Liverpool Product Search Assistant

This tool allows users to search for products in the Liverpool store using images and voice inputs. It leverages advanced AI technologies to provide a seamless and intuitive shopping experience.

## Features

1. **Image-based Search**: Upload an image of a product, and the tool will analyze it to find similar items in Liverpool's catalog.

2. **Voice-based Search**: Speak your product description or query, and the tool will convert it to text for searching.

3. **WhatsApp Integration**: Interact with the search tool directly through WhatsApp for convenience.

## How It Works

1. **Image Search**:
   - Send an image to the WhatsApp bot.
   - The image is processed using OpenAI's GPT-4 vision model to generate a description.
   - The description is used to search for similar products on Liverpool's website.

2. **Voice Search**:
   - Send a voice message to the WhatsApp bot.
   - The audio is transcribed using the Whisper AI model.
   - The transcribed text is used to search for products on Liverpool's website.

3. **Results**:
   - The bot responds with a link to the search results on Liverpool's website.

## Technologies Used

- Node.js with Venom-bot for WhatsApp interaction
- Python for backend processing
- OpenAI's GPT-4 for image description
- Whisper AI for speech-to-text conversion
- Liverpool's search API for product lookup

## Setup

(Include setup instructions here, such as environment variables, dependencies, etc.)

## Usage

1. Add the WhatsApp bot number to your contacts.
2. Send an image or voice message of the product you're looking for.
3. Receive a link to Liverpool's search results for similar products.

## Note

This tool is designed to enhance the shopping experience by providing an easy way to search for products using visual and audio inputs. It does not guarantee exact matches but aims to find similar or related products based on the provided input.
