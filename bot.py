import discord
from discord.ext import commands
from blackjack import BlackjackGame  # Import the game logic
from poker import PokerGame

# Define the necessary intents
intents = discord.Intents.default()
intents.message_content = True

# Initialize the bot with the specified intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Initialize a Blackjack game instance
game = BlackjackGame()
# Initialize a Poker game game instance
poker_game = PokerGame()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def blackjack(ctx):
    game.__init__()  # Reset the game
    game.start_game()
    
    player_hand = game.get_hand_cards(game.player_hand)
    dealer_hand = game.get_hand_cards(game.dealer_hand)
    player_value = game.get_hand_value(game.player_hand)
    
    await ctx.send(f'Your hand: {player_hand} (value: {player_value})')
    await ctx.send(f'Dealer\'s hand: {dealer_hand.split(", ")[0]}, Hidden')

@bot.command()
async def hit(ctx):
    game.hit(game.player_hand)
    player_hand = game.get_hand_cards(game.player_hand)
    player_value = game.get_hand_value(game.player_hand)
    
    if game.is_busted(game.player_hand):
        await ctx.send(f'You hit: {player_hand} (value: {player_value})\nYou busted!')
    else:
        await ctx.send(f'You hit: {player_hand} (value: {player_value})')

@bot.command()
async def stand(ctx):
    while game.get_hand_value(game.dealer_hand) < 17:
        game.hit(game.dealer_hand)
        
    dealer_hand = game.get_hand_cards(game.dealer_hand)
    dealer_value = game.get_hand_value(game.dealer_hand)
    player_value = game.get_hand_value(game.player_hand)
    
    if game.is_busted(game.dealer_hand):
        await ctx.send(f'Dealer\'s hand: {dealer_hand} (value: {dealer_value})\nDealer busted! You win!')
    elif dealer_value > player_value:
        await ctx.send(f'Dealer\'s hand: {dealer_hand} (value: {dealer_value})\nDealer wins!')
    elif dealer_value < player_value:
        await ctx.send(f'Dealer\'s hand: {dealer_hand} (value: {dealer_value})\nYou win!')
    else:
        await ctx.send(f'Dealer\'s hand: {dealer_hand} (value: {dealer_value})\nIt\'s a tie!')

@bot.command(name='startpoker')
async def start_poker(ctx):
    poker_game.__init__()
    await ctx.send('Poker game started! Use !joinpoker to join the game.')

@bot.command(name='joinpoker')
async def join_poker(ctx):
    poker_game.add_player(ctx.author.id)
    await ctx.send(f'{ctx.author.name} has joined the poker game.')

@bot.command(name='dealhole')
async def deal_hole(ctx):
    poker_game.deal_hole_cards()
    for player_id, hand in poker_game.hands.items():
        user = bot.get_user(player_id)
        await user.send(f'Your hand: {hand}')
    await ctx.send('Hole cards dealt. Players have been notified privately.')

@bot.command(name='dealflop')
async def deal_flop(ctx):
    poker_game.deal_flop()
    await ctx.send(f'Flop: {poker_game.get_community_cards()}')

@bot.command(name='dealturn')
async def deal_turn(ctx):
    poker_game.deal_turn()
    await ctx.send(f'Turn: {poker_game.get_community_cards()}')

@bot.command(name='dealriver')
async def deal_river(ctx):
    poker_game.deal_river()
    await ctx.send(f'River: {poker_game.get_community_cards()}')

bot.run('MTI0MTYxMzExMTMxMjc3NzIxNg.GjaSiV.ZVixFDvnhVETnfowHzbRPbTyuE0DyLjcnd9d8Q')
