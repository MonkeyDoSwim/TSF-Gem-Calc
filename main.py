import os
import discord 
from discord.ext import commands

# Fetch bot token from environment variables
token = os.getenv('DISCORD_TOKEN')

# Define intents
intents = discord.Intents.default()  # Use the default intents
intents.message_content = True  # Enable message content intent

# Create the bot instance with intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Define the channel ID where you want to send the messages
CHANNEL_ID = 1344200978785763380  # Replace with your channel ID

@bot.event
async def on_ready():
    print(f'Bot logged in as {bot.user}')

    # Send a message when the bot is online
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(f'{bot.user} is online and ready to calculate gem damage!')

@bot.command(name='gem')  
async def gem_damage(ctx):
    # Send a welcome message
    await ctx.send("Welcome to Damage Calculator Version 1.0.0. Please follow the prompts carefully to calculate gem damage.")

    # List of inputs and prompts
    prompts = [
        ("Please input the base damage for your gem:", float),
        ("Please input the trainer boost (percentage, e.g., 80 for 80%):", lambda x: float(x) / 100),
        ("Please input the multiply trainer boost (percentage, e.g., 60 for 60%):", lambda x: float(x) / 100),
        ("Please input the strap boost (percentage, e.g., 208 for 208%):", lambda x: float(x) / 100),
        ("Please input the skill plate boost (percentage, e.g., 50 for 50%):", lambda x: float(x) / 100),
        ("Please input the moment boost (percentage, e.g., 100 for 100%):", lambda x: float(x) / 100),
        ("Please input any extra trainer damage (if any, otherwise input 0):", float),
        ("Please input the gem buff from moves (percentage, e.g., 50 for 50%):", lambda x: float(x) / 100),
        ("Please input the multiply gem strength (If no multiply gems input 1):", float)
    ]

    # Create a dictionary to store inputs
    inputs = {}

    # Loop through the prompts and gather user input
    for prompt, conversion_func in prompts:
        await ctx.send(prompt)
        message = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
        inputs[prompt] = conversion_func(message.content)

    # Calculate the damage
    base_damage = inputs["Please input the base damage for your gem:"]
    moment_boost = inputs["Please input the moment boost (percentage, e.g., 100 for 100%):"]
    trainer_boost = inputs["Please input the trainer boost (percentage, e.g., 80 for 80%):"]
    multiply_trainer_boost = inputs["Please input the multiply trainer boost (percentage, e.g., 60 for 60%):"]
    strap_boost = inputs["Please input the strap boost (percentage, e.g., 208 for 208%):"]
    skill_plate_boost = inputs["Please input the skill plate boost (percentage, e.g., 50 for 50%):"]
    trainer_damage = inputs["Please input any extra trainer damage (if any, otherwise input 0):"]
    gem_buff = inputs["Please input the gem buff from moves (percentage, e.g., 50 for 50%):"]
    multiply_gem_strength = inputs["Please input the multiply gem strength (If no multiply gems input 1):"]

    # Apply the Moment Boost
    moment_boosted_damage = base_damage + (base_damage * moment_boost)

    # Apply Trainer Boost
    trainer_boosted_damage = moment_boosted_damage * (1 + trainer_boost)

    # Apply Multiply Trainer Boost
    multiply_trainer_damage = base_damage * multiply_trainer_boost

    # Apply Strap Boost
    strap_boost_damage = base_damage * strap_boost

    # Apply Skill Plate Boost
    skill_plate_damage = base_damage * skill_plate_boost

    # Calculate Total Damage before Gem Buff
    total_damage_before_buff = trainer_boosted_damage + multiply_trainer_damage + strap_boost_damage + skill_plate_damage + trainer_damage

    # Apply Gem Buff from Moves
    total_damage_with_buff = total_damage_before_buff * (1 + gem_buff)

    # Apply Multiply Gem Strength to the total damage
    final_damage = total_damage_with_buff * multiply_gem_strength

    # Send the result to the specified channel
    try:
        channel = bot.get_channel(CHANNEL_ID)  
        if channel:
            await channel.send(f"NOTE: THIS NUMBER DOES NOT TAKE INTO ACCOUNT OPPONENT'S GEM DEFENSE\n\nFinal Total Gem Damage: {final_damage}")
        else:
            await ctx.send("Error: Channel not found.")
    except Exception as e:
        await ctx.send(f"An error occurred while trying to send the message: {e}")

# Run the bot with your token
bot.run(token)
