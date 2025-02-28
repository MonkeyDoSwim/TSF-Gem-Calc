import discord
from discord.ext import commands

# Define intents
intents = discord.Intents.default()  # Use the default intents (you can adjust based on your needs)
intents.message_content = True  # Enable message content intent

# Create the bot instance with intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Define the channel ID where you want to send the messages
# Replace this with the actual channel ID you copied earlier
CHANNEL_ID = 1344200978785763380  # Replace with your channel ID

@bot.event
async def on_ready():
    print(f'Bot logged in as {bot.user}')

    # Send a message when the bot is online
    channel = bot.get_channel(CHANNEL_ID)  # Fetch the channel by ID
    if channel:
        await channel.send(f'{bot.user} is online and ready to calculate gem damage!')

@bot.command(name='gem')  # Changed the command name from 'gemdmg' to 'gem'
async def gem_damage(ctx):

    # Send a message before starting the inputs
    await ctx.send("Welcome to Damage Calculator Version 1.0.0. This bot only calculates gem damage of a certain color gem Ex: Shredder's Purple Gems or Miz's Yellow Gems.\n\n Please also allow for an error in the gem damage of ± ~8000 (the higher the number is the less accurate this will be. But you will still get a good estimate of the gem damage per gem).\n\n Make sure you follow the prompts and enter the correct values for what it is asking, otherwise you might end up with a different number. Thanks!\n\n")

    # Ask user for inputs one by one
    await ctx.send("\n\nPlease input the base damage for your gem :")
    base_damage_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
    base_damage = float(base_damage_msg.content)

    await ctx.send("Please input the trainer boost (as a percentage, e.g., 80 for 80%):")
    trainer_boost_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
    trainer_boost = float(trainer_boost_msg.content) / 100  # Convert to decimal

    await ctx.send("Please input the multiply trainer boost (as a percentage, e.g., 60 for 60%):")
    multiply_trainer_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
    multiply_trainer_boost = float(multiply_trainer_msg.content) / 100  # Convert to decimal

    await ctx.send("Please input the strap boost (as a percentage, e.g., 208 for 208%):")
    strap_boost_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
    strap_boost = float(strap_boost_msg.content) / 100  # Convert to decimal

    await ctx.send("Please input the skill plate boost (as a percentage, e.g., 50 for 50%):")
    skill_plate_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
    skill_plate_boost = float(skill_plate_msg.content) / 100  # Convert to decimal

    await ctx.send("Please input the moment boost (as a percentage, e.g., 100 for 100%):")
    moment_boost_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
    moment_boost = float(moment_boost_msg.content) / 100  # Convert to decimal

    await ctx.send("Please input any extra trainer damage (if any, otherwise input 0):")
    trainer_damage_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
    trainer_damage = float(trainer_damage_msg.content)

    # Ask for the "Gem Buff from Moves" (as a percentage, e.g., 50 for 50%)
    await ctx.send("Please input the gem buff from moves (as a percentage, e.g., 50 for 50%):")
    gem_buff_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
    gem_buff = float(gem_buff_msg.content) / 100  # Convert to decimal

    # Step 1: Apply the Moment Boost
    moment_boosted_damage = base_damage + (base_damage * moment_boost)

    # Step 2: Apply Trainer Boost
    trainer_boosted_damage = moment_boosted_damage * (1 + trainer_boost)

    # Step 3: Apply Multiply Trainer Boost (this is applied to base damage)
    multiply_trainer_damage = base_damage * multiply_trainer_boost

    # Step 4: Apply Strap Boost (this is applied to base damage)
    strap_boost_damage = base_damage * strap_boost

    # Step 5: Apply Skill Plate Boost (this is applied to base damage)
    skill_plate_damage = base_damage * skill_plate_boost

    # Step 6: Calculate Total Damage before Gem Buff from Moves
    total_damage_before_buff = trainer_boosted_damage + multiply_trainer_damage + strap_boost_damage + skill_plate_damage + trainer_damage

    # Step 7: Apply Gem Buff from Moves
    total_damage_with_buff = total_damage_before_buff * (1 + gem_buff)

    # Ask for the "Multiply Gem Strength" before calculating the final damage
    await ctx.send("Please input the multiply gem strength (If no multiply gems input 1 otherwise you will get zero as your total):")
    multiply_gem_strength_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
    multiply_gem_strength = float(multiply_gem_strength_msg.content)

    # Step 8: Apply Multiply Gem Strength to the total damage
    final_damage = total_damage_with_buff * multiply_gem_strength

    # Sending result to the specified channel
    try:
        channel = bot.get_channel(CHANNEL_ID)  # Fetch the channel by ID
        if channel:
            await channel.send(f"NOTE: THIS NUMBER DOES NOT TAKE INTO ACCOUNT OPPONENTS GEM DEFENSE\n\n Final Total Gem Damage: {final_damage}")
        else:
            await ctx.send("Error: Channel not found.")
    except Exception as e:
        await ctx.send(f"An error occurred while trying to send the message: {e}")

# Run the bot with your token
bot.run('')  # Replace 'YOUR_BOT_TOKEN' with your bot's token
