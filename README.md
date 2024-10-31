# Kapwing Logo Remover

This Discord bot, **KapwingLogoRemover**, helps remove watermarks from media files exported from [Kapwing](https://www.kapwing.com) by automatically cropping off 10% from the bottom of the image, video, or GIF. Kapwing is an online platform for creating and editing videos, images, and GIFs, widely used for generating social media content with easy-to-use tools and features. However, it often places a watermark on exported media unless you subscribe to a premium plan.

> **Note:** When exporting a project from Kapwing, add a **10% padding** at the bottom of your media to ensure that the watermark is fully removed when cropped by this bot.

## Features

- **Automatic Cropping**: Detects and crops 10% from the bottom of an image, video, or GIF.
- **Supported Formats**:
  - Images: `.png`, `.jpg`, `.jpeg`
  - Videos: `.mp4`, `.mov`, `.avi`
  - GIFs: `.gif`
- **User Feedback**: Provides real-time progress updates on media processing.

## Installation

### Requirements

- Python 3.x
- `py-cord` library (for Discord bot functionality)
- `moviepy` library (for video and GIF processing)
- `Pillow` library (for image handling)
- `dotenv` library (for loading the Discord bot token from environment variables)

### Setup

1. Clone this repository.
2. Install the required packages:
   ```bash
   pip install pycord moviepy pillow python-dotenv
   ```
3. Create a `.env` file in the root directory and add your Discord bot token:
   ```
   TOKEN=your_bot_token_here
   ```
4. Run the bot:
   ```bash
   python bot.py
   ```

### Usage

Upload an image, video, or GIF to the bot with the `/cropmedia` command. The bot will automatically crop 10% from the bottom of the media file and return the edited version.

