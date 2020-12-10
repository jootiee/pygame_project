import os

TILE_SIZE = 64
WIN_SIZE = (16 * TILE_SIZE, 9 * TILE_SIZE)
FPS = 60
GRAVITY = 0.25

WHITE = (255, 255, 255)
BLACK = (0,   0,   0)
BG_COLOR = (76, 81, 109)

current_dir = os.path.dirname(__file__)
assets = os.path.join(current_dir, 'assets')
lvls = os.path.join(current_dir, 'lvls')

CAT = os.path.join(assets, 'cat.png')
PEPEGA = os.path.join(assets, 'pepega.png')
RAT = os.path.join(assets, 'rat.png')
SILVER_COIN = os.path.join(assets, 'silver.png')
GOLD_COIN = os.path.join(assets, 'gold.png')
SPIKE = os.path.join(assets, 'spike.png')
MEDKIT = os.path.join(assets, 'medkit.png')

blocks = os.path.join(assets, 'blocks')
consumable = os.path.join(assets, 'consumables')
char = os.path.join(assets, 'char')

heal = os.path.join(consumable, 'heal')

PLAYER_ASSETS = {'idle': os.path.join(char, 'character.png')}

FOOD = [os.path.join(heal, 'Apple.png'),
        os.path.join(heal, 'AppleWorm.png'),
        os.path.join(heal, 'Avocado.png'),
        os.path.join(heal, 'Bacon.png'),
        os.path.join(heal, 'Beer.png'),
        os.path.join(heal, 'Boar.png'),
        os.path.join(heal, 'Bread.png'),
        os.path.join(heal, 'Brownie.png'),
        os.path.join(heal, 'Bug.png'),
        os.path.join(heal, 'Cheese.png'),
        os.path.join(heal, 'Cherry.png'),
        os.path.join(heal, 'Chicken.png'),
        os.path.join(heal, 'ChickenLeg.png'),
        os.path.join(heal, 'Cookie.png'),
        os.path.join(heal, 'DragonFruit.png'),
        os.path.join(heal, 'Eggplant.png'),
        os.path.join(heal, 'Eggs.png'),
        os.path.join(heal, 'Fish.png'),
        os.path.join(heal, 'FishFillet.png'),
        os.path.join(heal, 'FishSteak.png'),
        os.path.join(heal, 'Grub.png'),
        os.path.join(heal, 'Grub.png'),
        os.path.join(heal, 'Honey.png'),
        os.path.join(heal, 'Honeycomb.png'),
        os.path.join(heal, 'Jam.png'),
        os.path.join(heal, 'Jerky.png'),
        os.path.join(heal, 'Lemon.png'),
        os.path.join(heal, 'Marmalade.png'),
        os.path.join(heal, 'MelonCantaloupe.png'),
        os.path.join(heal, 'MelonHoneydew.png'),
        os.path.join(heal, 'MelonWater.png'),
        os.path.join(heal, 'Moonshine.png'),
        os.path.join(heal, 'Olive.png'),
        os.path.join(heal, 'Onion.png'),
        os.path.join(heal, 'PepperRed.png'),
        os.path.join(heal, 'Pickle.png'),
        os.path.join(heal, 'PickledEggs.png'),
        os.path.join(heal, 'PieApple.png'),
        os.path.join(heal, 'PieLemon.png'),
        os.path.join(heal, 'PiePumpkin.png'),
        os.path.join(heal, 'Pineapple.png'),
        os.path.join(heal, 'Potato.png'),
        os.path.join(heal, 'PotatoRed.png'),
        os.path.join(heal, 'Pretzel.png'),
        os.path.join(heal, 'Ribs.png'),
        os.path.join(heal, 'Rol.png'),
        os.path.join(heal, 'Saki.png'),
        os.path.join(heal, 'PepperGreen.png'),
        os.path.join(heal, 'Peach.png'),
        os.path.join(heal, 'Pepperoni.png'),
        os.path.join(heal, 'Sardines.png'),
        os.path.join(heal, 'Sashimi.png'),
        os.path.join(heal, 'Sausages.png'),
        os.path.join(heal, 'Shrimp.png'),
        os.path.join(heal, 'Steak.png'),
        os.path.join(heal, 'Stein.png'),
        os.path.join(heal, 'Strawberry.png'),
        os.path.join(heal, 'Sushi.png'),
        os.path.join(heal, 'Tart.png'),
        os.path.join(heal, 'Tomato.png'),
        os.path.join(heal, 'Turnip.png'),
        os.path.join(heal, 'Waffles.png'),
        os.path.join(heal, 'Whiskey.png'),
        os.path.join(heal, 'Wine.png')]

coins = os.path.join(consumable, 'coins')
COINS = [os.path.join(coins, 'Coin_Blue.png'),
         os.path.join(coins, 'Coin_Gold.png'),
         os.path.join(coins, 'Coin_Green.png'),
         os.path.join(coins, 'Coin_Purple.png'),
         os.path.join(coins, 'Coin_Red.png')]

LEVELS = [os.path.join(lvls, 'lvl1.txt')]


BLOCK_ASSETS = {'ground': os.path.join(blocks, 'ground.png')}



MAP = {
    'C': COINS[0],
    'B': BLOCK_ASSETS['ground'],
    'S': SPIKE,
    'F': FOOD[0],
}

SOLID_BLOCKS = 'BS'