import os
import discord
from discord.ext import commands
from discord.commands import Option
from discord import option
import io
import tempfile
from PIL import Image
from moviepy.editor import VideoFileClip
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.default()
client = commands.Bot(command_prefix="!", intents=intents)
loading = "<a:loading:970301436174929930>"
failed = "<:failed:885201221953126501>"

@client.event
async def on_ready():
    print(f'Logged in as {client.user}!')


async def update_progress(message, progress_text):
    await message.edit(content=progress_text)


def crop_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    width, height = image.size
    new_height = int(height - (height * 0.1))
    cropped_image = image.crop((0, 0, width, new_height))
    cropped_bytes = io.BytesIO()
    cropped_image.save(cropped_bytes, format="PNG")
    cropped_bytes.seek(0)
    return cropped_bytes

def crop_video(video_bytes):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video:
        temp_video.write(video_bytes)
        temp_video.flush()
        video_clip = VideoFileClip(temp_video.name)
        current_height = video_clip.size[1]
        new_height = int(current_height - (current_height * 0.1))
        cropped_clip = video_clip.crop(y1=0, y2=new_height)
        
        # Save cropped video to a temporary file
        temp_cropped_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
        temp_cropped_file.close()  # Close to get the file path
        cropped_clip.write_videofile(temp_cropped_file.name, codec="libx264", audio_codec="aac")

        # Read the temporary file back as BytesIO
        with open(temp_cropped_file.name, 'rb') as f:
            cropped_bytes = io.BytesIO(f.read())

        # Clean up temporary files
        os.unlink(temp_cropped_file.name)
        os.unlink(temp_video.name)

        return cropped_bytes
    
def crop_gif(gif_bytes):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.gif') as temp_gif:
        temp_gif.write(gif_bytes)
        temp_gif.flush()
        gif_clip = VideoFileClip(temp_gif.name)
        current_height = gif_clip.size[1]
        new_height = int(current_height - (current_height * 0.1))
        cropped_clip = gif_clip.crop(y1=0, y2=new_height)
        
        # Save cropped gif to a temporary file
        temp_cropped_file = tempfile.NamedTemporaryFile(delete=False, suffix='.gif')
        temp_cropped_file.close()  # Close to get the file path
        cropped_clip.write_gif(temp_cropped_file.name, fps=gif_clip.fps)

        # Read the temporary file back as BytesIO
        with open(temp_cropped_file.name, 'rb') as f:
            cropped_bytes = io.BytesIO(f.read())

        # Clean up temporary files
        os.unlink(temp_cropped_file.name)
        os.unlink(temp_gif.name)

        return cropped_bytes

@client.slash_command(
    name="cropmedia",
    description="Crops 10% of an image, video, or GIF",
    guild_ids=[1139525602483916800]
)
@option(
    "attachment",
    discord.Attachment,
    description="A file to attach to the message",
    required=True,
)
async def crop_media(ctx: discord.ApplicationContext, attachment: discord.Attachment):
    await ctx.respond(f"{loading} Processing...")
    media_bytes = await attachment.read()
    media_filename = attachment.filename.lower()

    if media_filename.endswith((".png", ".jpg", ".jpeg")):
        await ctx.interaction.edit_original_response(content=f"{loading} Image detected, cropping...")
        cropped_bytes = crop_image(media_bytes)
    elif media_filename.endswith((".mp4", ".mov", ".avi")):
        await ctx.interaction.edit_original_response(content=f"{loading} Video detected, cropping...")
        cropped_bytes = crop_video(media_bytes)
    elif media_filename.endswith(".gif"):
        await ctx.interaction.edit_original_response(content=f"{loading} GIF detected, cropping...")
        cropped_bytes = crop_gif(media_bytes)
    else:
        await ctx.interaction.edit_original_response(content=f"{failed} Unsupported file format for cropping.")
        return

    await ctx.interaction.edit_original_response(content=f"✅ Processing done. Uploading cropped media...")
    await ctx.send(f"<@{ctx.user.id}>", file=discord.File(cropped_bytes, filename=f"cropped_media.{media_filename}"))
    #await ctx.interaction.response.delete()

# Run the bot with your token
client.run(os.getenv("TOKEN"))

