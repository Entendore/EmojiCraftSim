#!/usr/bin/env python3
"""Pygame Emoji Crafting/Building/Mining/Farming/Combat Simulator"""

import pygame, sys, os, json, math, random, time, struct, array
import numpy as np
from collections import defaultdict

# ─── Constants ───────────────────────────────────────────────────────────────
SW, SH = 1200, 800
TILE = 40
MW, MH = 100, 75
FPS = 60
FONT_PATH = '/usr/share/fonts/truetype/emoji/NotoColorEmoji.ttf'
SAVE_FILE = os.path.join(os.getcwd(), 'craft_valley_save.json')

# ─── Terrain Definitions ────────────────────────────────────────────────────
TERRAIN_EMOJIS = {
    'grass':'🌿','dirt':'🟫','stone':'🪨','deep_stone':'⬛','bedrock':'⬛',
    'water':'🌊','sand':'🏖️','tree':'🌲','bush':'🌳','flower':'🌸',
    'snow_grass':'❄️','ice':'🧊','cactus':'🌵','mushroom':'🍄',
    'coal_ore':'⬛','iron_ore':'🟤','gold_ore':'🟡','diamond_ore':'💎',
    'copper_ore':'🟠','ruby_ore':'🔴','emerald_ore':'🟢',
    'farm_tilled':'🟫','farm_planted':'🌱','farm_growing':'🌾',
    'farm_ready':'🌽','planks':'🪵','cobble':'🪨','brick':'🧱',
    'furnace':'🔥','chest':'📦','craft_table':'🔨','torch':'🔦',
    'fence':'🏚️','farm_plot':'🌾','ladder':'🪜','glass':'🪟',
    'bookshelf':'📚','bed':'🛏️','door':'🚪','wall_stone':'🏛️',
    'wall_wood':'🪵','tower':'🗼','bridge_wood':'🌉','bridge_stone':'🌉',
    'well':'🪣','shop':'🏪','anvil':'⚒️','cauldron':'🫕',
    'armor_stand':'🛡️','sign':'🪧','loom':'🧵',
}

PLACEABLE = {
    'planks','cobble','brick','furnace','chest','craft_table','torch',
    'fence','farm_plot','ladder','glass','bookshelf','bed','door',
    'wall_stone','wall_wood','tower','bridge_wood','bridge_stone',
    'well','shop','anvil','cauldron','armor_stand','sign','loom',
}

MINEABLE = {
    'grass','dirt','stone','deep_stone','sand','tree','bush','flower',
    'snow_grass','ice','cactus','mushroom','coal_ore','iron_ore',
    'gold_ore','diamond_ore','copper_ore','ruby_ore','emerald_ore',
    'farm_tilled','farm_planted','farm_growing','farm_ready',
}

# ─── Item Definitions ───────────────────────────────────────────────────────
ITEM_EMOJIS = {
    'wood':'🪵','stone':'🪨','dirt':'🟫','sand':'🏖️','coal':'⬛',
    'iron_ore':'🟤','gold_ore':'🟡','diamond':'💎','copper':'🟠',
    'ruby':'🔴','emerald':'🟢','planks':'🪵','stick':'🥢',
    'cobble':'🪨','brick':'🧱','torch':'🔦','fence':'🏚️',
    'chest':'📦','craft_table':'🔨','furnace':'🔥','ladder':'🪜',
    'glass':'🪟','bookshelf':'📚','bed':'🛏️','door':'🚪',
    'wood_pick':'⛏️','stone_pick':'⛏️','iron_pick':'⛏️',
    'gold_pick':'⛏️','diamond_pick':'⛏️','copper_pick':'⛏️',
    'wood_axe':'🪓','stone_axe':'🪓','iron_axe':'🪓',
    'gold_axe':'🪓','diamond_axe':'🪓','copper_axe':'🪓',
    'wood_sword':'🗡️','stone_sword':'🗡️','iron_sword':'🗡️',
    'gold_sword':'🗡️','diamond_sword':'🗡️',
    'iron_armor':'🛡️','diamond_armor':'🛡️','shield':'🛡️',
    'bread':'🍞','apple':'🍎','cooked_meat':'🍖','mushroom_stew':'🍲',
    'golden_apple':'✨','iron_ingot':'⚙️','gold_ingot':'🪙',
    'copper_ingot':'🟠','brick_item':'🧱','diamond_gem':'💎',
    'seed':'🌱','wheat':'🌾','flower_item':'🌸','cactus_item':'🌵',
    'snowball':'❄️','ice_item':'🧊','leather':'🟫',
    'bark':'🪵','resin':'🟡','stone_brick':'🏛️',
    'rope':'🪢','bucket':'🪣','iron_bar':'⚙️',
    'wall_stone_item':'🏛️','wall_wood_item':'🪵',
    'bridge_item':'🌉','tower_item':'🗼',
    'well_item':'🪣','shop_item':'🏪','anvil_item':'⚒️',
    'cauldron_item':'🫕','loom_item':'🧵','sign_item':'🪧',
    'armor_stand_item':'🛡️',
}

ITEM_NAMES = {
    'wood':'Wood','stone':'Stone','dirt':'Dirt','sand':'Sand','coal':'Coal',
    'iron_ore':'Iron Ore','gold_ore':'Gold Ore','diamond':'Diamond','copper':'Copper',
    'ruby':'Ruby','emerald':'Emerald','planks':'Planks','stick':'Stick',
    'cobble':'Cobblestone','brick':'Brick','torch':'Torch','fence':'Fence',
    'chest':'Chest','craft_table':'Crafting Table','furnace':'Furnace',
    'ladder':'Ladder','glass':'Glass','bookshelf':'Bookshelf','bed':'Bed',
    'door':'Door','wood_pick':'Wood Pickaxe','stone_pick':'Stone Pickaxe',
    'iron_pick':'Iron Pickaxe','gold_pick':'Gold Pickaxe',
    'diamond_pick':'Diamond Pickaxe','copper_pick':'Copper Pickaxe',
    'wood_axe':'Wood Axe','stone_axe':'Stone Axe','iron_axe':'Iron Axe',
    'gold_axe':'Gold Axe','diamond_axe':'Diamond Axe',
    'copper_axe':'Copper Axe','wood_sword':'Wood Sword',
    'stone_sword':'Stone Sword','iron_sword':'Iron Sword',
    'gold_sword':'Gold Sword','diamond_sword':'Diamond Sword',
    'iron_armor':'Iron Armor','diamond_armor':'Diamond Armor',
    'shield':'Shield','bread':'Bread','apple':'Apple',
    'cooked_meat':'Cooked Meat','mushroom_stew':'Mushroom Stew',
    'golden_apple':'Golden Apple','iron_ingot':'Iron Ingot',
    'gold_ingot':'Gold Ingot','copper_ingot':'Copper Ingot',
    'brick_item':'Brick','diamond_gem':'Diamond Gem',
    'seed':'Seed','wheat':'Wheat','flower_item':'Flower',
    'cactus_item':'Cactus','snowball':'Snowball','ice_item':'Ice',
    'leather':'Leather','bark':'Bark','resin':'Resin',
    'stone_brick':'Stone Brick','rope':'Rope','bucket':'Bucket',
    'iron_bar':'Iron Bar','wall_stone_item':'Stone Wall',
    'wall_wood_item':'Wood Wall','bridge_item':'Bridge',
    'tower_item':'Tower','well_item':'Well','shop_item':'Shop',
    'anvil_item':'Anvil','cauldron_item':'Cauldron',
    'loom_item':'Loom','sign_item':'Sign','armor_stand_item':'Armor Stand',
}

# ─── Tool Effectiveness ─────────────────────────────────────────────────────
# v3: pickaxes now have area bonuses and ore-specific bonuses
TOOL_EFFECTIVENESS = {
    'wood_pick':  {'stone':2,'deep_stone':2,'coal_ore':2,'iron_ore':1.5,'gold_ore':1,'copper_ore':1.5,'diamond_ore':0.5,'ruby_ore':0.5,'emerald_ore':0.5,'ice':1},
    'stone_pick': {'stone':3,'deep_stone':2,'coal_ore':3,'iron_ore':2.5,'gold_ore':1.5,'copper_ore':2,'diamond_ore':0.7,'ruby_ore':0.7,'emerald_ore':0.7,'ice':1.5},
    'iron_pick':  {'stone':4,'deep_stone':3,'coal_ore':4,'iron_ore':4,'gold_ore':2.5,'copper_ore':3,'diamond_ore':1.5,'ruby_ore':1.5,'emerald_ore':1.5,'ice':2},
    'copper_pick':{'stone':3,'deep_stone':2,'coal_ore':3,'iron_ore':2,'gold_ore':2,'copper_ore':4,'diamond_ore':1,'ruby_ore':1,'emerald_ore':1,'ice':1.5},
    'gold_pick':  {'stone':5,'deep_stone':4,'coal_ore':5,'iron_ore':5,'gold_ore':5,'copper_ore':5,'diamond_ore':3,'ruby_ore':3,'emerald_ore':3,'ice':3},
    'diamond_pick':{'stone':6,'deep_stone':5,'coal_ore':6,'iron_ore':6,'gold_ore':6,'copper_ore':6,'diamond_ore':6,'ruby_ore':6,'emerald_ore':6,'ice':4},
    'wood_axe':   {'tree':2,'bush':2,'cactus':1},
    'stone_axe':  {'tree':3,'bush':3,'cactus':1.5},
    'iron_axe':   {'tree':4,'bush':4,'cactus':2},
    'gold_axe':   {'tree':5,'bush':5,'cactus':3},
    'diamond_axe':{'tree':6,'bush':6,'cactus':4},
    'copper_axe': {'tree':3,'bush':3,'cactus':1.5},
}

# v3: Area mining radius per pickaxe tier
PICK_AREA = {
    'wood_pick':0,'stone_pick':0,'iron_pick':1,'copper_pick':0,
    'gold_pick':1,'diamond_pick':2,
}

# v3: Ore bonus drops (extra items when mining with matching tool tier)
ORE_BONUSES = {
    'diamond_ore': {'diamond_pick': 2, 'gold_pick': 1},
    'ruby_ore': {'diamond_pick': 2, 'gold_pick': 1},
    'emerald_ore': {'diamond_pick': 2, 'gold_pick': 1},
    'gold_ore': {'gold_pick': 2, 'iron_pick': 1, 'diamond_pick': 2},
    'iron_ore': {'iron_pick': 2, 'diamond_pick': 2},
    'copper_ore': {'copper_pick': 2, 'iron_pick': 1, 'diamond_pick': 2},
}

# v3: Axe connected felling support
AXE_FELLING = {
    'wood_axe': False, 'stone_axe': False, 'copper_axe': False,
    'iron_axe': True, 'gold_axe': True, 'diamond_axe': True,
}

DURABILITY = {
    'wood_pick':60,'stone_pick':120,'iron_pick':200,'copper_pick':150,
    'gold_pick':30,'diamond_pick':500,
    'wood_axe':60,'stone_axe':120,'iron_axe':200,'copper_axe':150,
    'gold_axe':30,'diamond_axe':500,
    'wood_sword':80,'stone_sword':150,'iron_sword':250,
    'gold_sword':40,'diamond_sword':600,
    'iron_armor':300,'diamond_armor':800,'shield':200,
}

WEAPON_DAMAGE = {
    'wood_sword':3,'stone_sword':5,'iron_sword':7,
    'gold_sword':4,'diamond_sword':10,
}

ARMOR_DEFENSE = {'iron_armor':3,'diamond_armor':6,'shield':2}
FOOD_HEAL = {'bread':2,'apple':1,'cooked_meat':5,'mushroom_stew':4,'golden_apple':10}

# ─── Recipes ─────────────────────────────────────────────────────────────────
RECIPES = [
    # Basic
    ('planks', 4, {'wood':1}),
    ('stick', 4, {'planks':2}),
    ('craft_table', 1, {'planks':4}),
    ('chest', 1, {'planks':8}),
    ('furnace', 1, {'cobble':8}),
    ('torch', 4, {'stick':1,'coal':1}),
    ('ladder', 3, {'stick':7}),
    ('fence', 3, {'stick':3,'planks':2}),
    ('door', 1, {'planks':6}),
    ('sign', 3, {'planks':6,'stick':1}),
    # v3 new basic
    ('rope', 2, {'stick':2,'leather':1}),
    ('bucket', 1, {'iron_ingot':3}),
    ('bookshelf', 1, {'planks':6,'stick':3}),
    ('bed', 1, {'planks':3,'leather':3}),
    ('glass', 4, {'sand':4,'coal':1}),
    # Tools - Pickaxes
    ('wood_pick', 1, {'planks':3,'stick':2}),
    ('stone_pick', 1, {'cobble':3,'stick':2}),
    ('iron_pick', 1, {'iron_ingot':3,'stick':2}),
    ('copper_pick', 1, {'copper_ingot':3,'stick':2}),
    ('gold_pick', 1, {'gold_ingot':3,'stick':2}),
    ('diamond_pick', 1, {'diamond':3,'stick':2}),
    # Tools - Axes
    ('wood_axe', 1, {'planks':3,'stick':2}),
    ('stone_axe', 1, {'cobble':3,'stick':2}),
    ('iron_axe', 1, {'iron_ingot':3,'stick':2}),
    ('copper_axe', 1, {'copper_ingot':3,'stick':2}),
    ('gold_axe', 1, {'gold_ingot':3,'stick':2}),
    ('diamond_axe', 1, {'diamond':3,'stick':2}),
    # Weapons
    ('wood_sword', 1, {'planks':2,'stick':1}),
    ('stone_sword', 1, {'cobble':2,'stick':1}),
    ('iron_sword', 1, {'iron_ingot':2,'stick':1}),
    ('gold_sword', 1, {'gold_ingot':2,'stick':1}),
    ('diamond_sword', 1, {'diamond':2,'stick':1}),
    # Armor
    ('iron_armor', 1, {'iron_ingot':8}),
    ('diamond_armor', 1, {'diamond':8}),
    ('shield', 1, {'iron_ingot':6,'leather':2}),
    # Food
    ('bread', 3, {'wheat':3}),
    ('mushroom_stew', 1, {'mushroom':3,'bowl_item':1}),
    ('golden_apple', 1, {'apple':1,'gold_ingot':1}),
    # v3 Buildings
    ('wall_stone_item', 4, {'cobble':4,'stone_brick':2}),
    ('wall_wood_item', 4, {'planks':4,'stick':2}),
    ('bridge_item', 1, {'planks':8,'rope':2,'iron_bar':2}),
    ('tower_item', 1, {'stone_brick':16,'planks':8,'iron_bar':4}),
    ('well_item', 1, {'stone_brick':8,'rope':2,'bucket':1}),
    ('shop_item', 1, {'planks':16,'glass':4,'sign':1}),
    ('anvil_item', 1, {'iron_ingot':8,'iron_bar':4}),
    ('cauldron_item', 1, {'iron_ingot':7}),
    ('loom_item', 1, {'planks':6,'stick':4,'rope':2}),
    ('armor_stand_item', 1, {'planks':6,'stick':3,'iron_bar':2}),
    ('stone_brick', 4, {'cobble':4}),
    ('iron_bar', 2, {'iron_ingot':1}),
    ('bowl_item', 1, {'planks':3}),
]

SMELTING_RECIPES = {
    'iron_ore': ('iron_ingot', 1, 8),
    'gold_ore': ('gold_ingot', 1, 10),
    'copper': ('copper_ingot', 1, 6),
    'sand': ('glass', 1, 4),
    'cobble': ('stone_brick', 1, 6),
    'raw_meat': ('cooked_meat', 1, 5),
}

TERRAIN_DROPS = {
    'grass':('dirt',1),'dirt':('dirt',1),'stone':('stone',1),'deep_stone':('stone',1),
    'sand':('sand',1),'tree':('wood',2),'bush':('wood',1),'flower':('flower_item',1),
    'snow_grass':('snowball',1),'ice':('ice_item',1),'cactus':('cactus_item',1),
    'mushroom':('mushroom',1),'coal_ore':('coal',2),'iron_ore':('iron_ore',1),
    'gold_ore':('gold_ore',1),'diamond_ore':('diamond',1),'copper_ore':('copper',1),
    'ruby_ore':('ruby',1),'emerald_ore':('emerald',1),
    'farm_ready':('wheat',2),'farm_ready_2':('seed',1),
}

BUILDING_PLACE_MAP = {
    'wall_stone_item':'wall_stone','wall_wood_item':'wall_wood',
    'bridge_item':'bridge_wood','tower_item':'tower',
    'well_item':'well','shop_item':'shop',
    'anvil_item':'anvil','cauldron_item':'cauldron',
    'loom_item':'loom','sign_item':'sign','armor_stand_item':'armor_stand',
}

# ─── Achievements ────────────────────────────────────────────────────────────
ACHIEVEMENTS = {
    'first_mine': ('First Dig!','Mined your first block','⛏️'),
    'first_craft': ('Crafty!','Crafted your first item','🔨'),
    'first_build': ('Builder','Placed your first building','🏗️'),
    'iron_tools': ('Iron Age','Crafted an iron tool','⚙️'),
    'diamond_tools': ('Diamond Age','Crafted a diamond tool','💎'),
    'full_armor': ('Armored Up','Equipped full armor','🛡️'),
    'night_survive': ('Night Owl','Survived until dawn','🌙'),
    'enemy_slain': ('Warrior','Defeated an enemy','⚔️'),
    'area_mine': ('Demolition!','Used area mining','💥'),
    'tree_feller': ('Timber!','Felled a connected tree','🌲'),
    'master_builder': ('Architect','Built 20 buildings','🏛️'),
    'farmer': ('Green Thumb','Harvested a crop','🌾'),
    'well_digger': ('Well Done','Built a well','🪣'),
    'shop_keeper': ('Open for Business','Built a shop','🏪'),
}

# ─── Noise & World Gen ──────────────────────────────────────────────────────
def fbm(x, y, seed=0, octaves=4, lacunarity=2.0, gain=0.5):
    """Fractional Brownian Motion noise."""
    val = 0.0; amp = 1.0; freq = 1.0; mx = 0.0
    for o in range(octaves):
        s = seed + o * 1000
        n = hash((int(x*freq*1000+s), int(y*freq*1000+s))) % 10000 / 10000.0
        val += amp * (n * 2 - 1)
        mx += amp; amp *= gain; freq *= lacunarity
    return val / mx

def generate_world(seed=None):
    if seed is None:
        seed = random.randint(0, 999999)
    world = []
    for y in range(MH):
        row = []
        for x in range(MW):
            if x == 0 or y == 0 or x == MW-1 or y == MH-1:
                row.append('bedrock'); continue
            e = fbm(x, y, seed, 4)
            m = fbm(x, y, seed+1000, 3)
            t = fbm(x, y, seed+2000, 3)
            if e < -0.3:
                row.append('water')
            elif e < -0.15:
                row.append('sand')
            elif m > 0.3:
                if t < -0.2:
                    row.append('mushroom')
                elif random.random() < 0.08:
                    row.append('flower')
                else:
                    row.append('bush' if random.random() < 0.15 else 'grass')
            elif t < -0.3:
                if random.random() < 0.06:
                    row.append('tree')
                else:
                    row.append('snow_grass')
            elif t > 0.4:
                if random.random() < 0.05:
                    row.append('cactus')
                else:
                    row.append('sand')
            elif random.random() < 0.08:
                row.append('tree')
            elif e < 0.15:
                row.append('grass')
            elif e < 0.3:
                row.append('stone' if random.random() < 0.7 else 'grass')
            elif e < 0.5:
                ore_r = random.random()
                if ore_r < 0.03: row.append('diamond_ore')
                elif ore_r < 0.08: row.append('ruby_ore')
                elif ore_r < 0.13: row.append('emerald_ore')
                elif ore_r < 0.25: row.append('gold_ore')
                elif ore_r < 0.40: row.append('iron_ore')
                elif ore_r < 0.50: row.append('copper_ore')
                elif ore_r < 0.60: row.append('coal_ore')
                else: row.append('stone')
            elif e < 0.7:
                ore_r = random.random()
                if ore_r < 0.05: row.append('diamond_ore')
                elif ore_r < 0.12: row.append('ruby_ore')
                elif ore_r < 0.20: row.append('emerald_ore')
                elif ore_r < 0.35: row.append('gold_ore')
                elif ore_r < 0.50: row.append('iron_ore')
                elif ore_r < 0.65: row.append('copper_ore')
                elif ore_r < 0.75: row.append('coal_ore')
                else: row.append('deep_stone')
            else:
                row.append('deep_stone')
        world.append(row)
    return world, seed

# ─── Sound System ────────────────────────────────────────────────────────────
has_sound = False
def init_sound():
    global has_sound
    try:
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        has_sound = True
    except Exception:
        has_sound = False

def _make_stereo(wave):
    if wave.ndim == 1:
        return np.column_stack([wave, wave])
    return wave

def make_sound(freqs, duration=0.12, vol=0.15):
    if not has_sound: return None
    try:
        sr = 44100; n = int(sr * duration)
        t = np.arange(n) / sr
        phase = np.cumsum(freqs / sr) * 2 * np.pi
        w = np.sin(phase) * vol
        w = np.clip(w * (1 - t/duration), -1, 1)
        w = (w * 32767).astype(np.int16)
        w = _make_stereo(w)
        return pygame.sndarray.make_sound(w)
    except Exception:
        return None

# ─── Particle System ─────────────────────────────────────────────────────────
class Particle:
    __slots__ = ['x','y','vx','vy','life','max_life','color','emoji']
    def __init__(self, x, y, vx, vy, life, color=(200,200,200), emoji=None):
        self.x=x; self.y=y; self.vx=vx; self.vy=vy
        self.life=life; self.max_life=life; self.color=color; self.emoji=emoji

# ─── Enemy Class ─────────────────────────────────────────────────────────────
class Enemy:
    def __init__(self, x, y, etype='slime'):
        self.x=x; self.y=y; self.etype=etype
        self.max_hp=10; self.hp=10; self.damage=2; self.speed=1.0
        self.color=(0,200,0); self.emoji='🟢'; self.xp=5
        self.knockback_x=0; self.knockback_y=0
        self.kb_timer=0
        self.loot = {}
        if etype == 'slime':
            self.max_hp=12; self.hp=12; self.damage=2; self.speed=0.8
            self.color=(0,220,0); self.emoji='🟢'; self.xp=5
            self.loot = {'leather':1}
        elif etype == 'zombie':
            self.max_hp=25; self.hp=25; self.damage=5; self.speed=0.6
            self.color=(100,150,100); self.emoji='🧟'; self.xp=12
            self.loot = {'iron_ore':1}
        elif etype == 'goblin':
            self.max_hp=18; self.hp=18; self.damage=4; self.speed=1.2
            self.color=(150,100,50); self.emoji='👺'; self.xp=10
            self.loot = {'gold_ore':1}
        elif etype == 'skeleton':
            self.max_hp=20; self.hp=20; self.damage=6; self.speed=0.9
            self.color=(220,220,220); self.emoji='💀'; self.xp=15
            self.loot = {'coal':2,'bone':1}

    def update(self, px, py, dt=1):
        if self.kb_timer > 0:
            self.kb_timer -= 1
            self.x += self.knockback_x * 0.5
            self.y += self.knockback_y * 0.5
            self.knockback_x *= 0.7; self.knockback_y *= 0.7
            return
        dx = px - self.x; dy = py - self.y
        dist = math.sqrt(dx*dx + dy*dy)
        if dist < 0.1: dist = 0.1
        if dist < 25:
            self.x += (dx/dist) * self.speed * dt
            self.y += (dy/dist) * self.speed * dt

# ─── Main Game Class ─────────────────────────────────────────────────────────
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SW, SH))
        pygame.display.set_caption('Craft Valley v3 - Enhanced Mining & Building')
        self.clock = pygame.time.Clock()
        self.emoji_font = pygame.font.Font(FONT_PATH, 64)
        self.ui_font = pygame.font.Font('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 16)
        self.ui_font_lg = pygame.font.Font('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 22)
        self.ui_font_sm = pygame.font.Font('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)

        init_sound()
        self.snd_mine = make_sound([440, 330, 220], 0.1, 0.12)
        self.snd_place = make_sound([330, 440, 550], 0.1, 0.12)
        self.snd_craft = make_sound([440, 550, 660, 880], 0.2, 0.15)
        self.snd_hit = make_sound([200, 150, 100], 0.08, 0.1)
        self.snd_eat = make_sound([300, 400, 350, 450], 0.15, 0.1)
        self.snd_ach = make_sound([523, 659, 784, 1047], 0.4, 0.12)

        self.emoji_cache = {}
        self.world = None; self.seed = 0
        self.generate_world()
        self.px = MW // 2; self.py = MH // 2
        self.px_f = float(self.px); self.py_f = float(self.py)
        self.cam_x = 0.0; self.cam_y = 0.0

        self.inventory = defaultdict(int)
        self.hotbar = ['wood_pick','wood_axe','wood_sword','bread','torch','planks','','','']
        self.hotbar_sel = 0
        self.durability = {}

        self.hp = 20; self.max_hp = 20
        self.hunger = 20; self.max_hunger = 20
        self.xp = 0; self.level = 1; self.xp_next = 50
        self.armor_slot = None; self.shield_slot = None
        self.damage_cooldown = 0

        self.show_craft = False; self.show_inv = False
        self.show_chest = False; self.chest_pos = None; self.chest_inv = defaultdict(int)
        self.show_furnace = False; self.furnace_pos = None
        self.furnace_input = None; self.furnace_fuel = None; self.furnace_timer = 0
        self.show_map = False
        self.minimap_surf = None; self.minimap_dirty = True

        self.particles = []; self.dmg_numbers = []
        self.crack_anim = {}  # (tx,ty) -> timer

        self.enemies = []; self.spawn_timer = 0
        self.day_time = 0.0; self.day_length = 3600
        self.weather = 'clear'; self.weather_timer = random.randint(600, 1800)
        self.weather_particles = []

        self.achievements = set()
        self.ach_popup = None; self.ach_timer = 0
        self.build_count = 0

        # v3: Charged mining
        self.charge_start = 0; self.is_charging = False; self.max_charge = 60
        # v3: Connected tree felling
        self.felling_set = set()
        # v3: Bark peeling
        self.bark_count = 0
        # v3: Leaves decay
        self.leaves_decay = []  # [(x,y,timer), ...]
        # v3: Farm plots track
        self.farm_timers = {}  # (x,y) -> grow_timer
        # v3: Water source for well
        self.well_water = {}  # (x,y) -> True

        self.frame = 0; self.running = True
        self.keys_held = set()

    def generate_world(self):
        self.world, self.seed = generate_world()
        self.minimap_dirty = True

    def get_emoji_surf(self, emoji_char, size=None):
        if size is None: size = TILE - 6
        key = (emoji_char, size)
        if key not in self.emoji_cache:
            raw = self.emoji_font.render(emoji_char, True, (0,0,0))
            if raw.get_width() > 0 and raw.get_height() > 0:
                self.emoji_cache[key] = pygame.transform.smoothscale(raw, (size, size))
            else:
                s = pygame.Surface((size, size)); s.fill((100,100,100))
                self.emoji_cache[key] = s
        return self.emoji_cache[key]

    def play(self, snd):
        if snd and has_sound:
            try: snd.play()
            except: pass

    # ─── Inventory ───────────────────────────────────────────────────────
    def add_item(self, item, count=1):
        self.inventory[item] += count
        # Auto-add to empty hotbar slot
        if item not in self.hotbar:
            for i in range(len(self.hotbar)):
                if self.hotbar[i] == '':
                    self.hotbar[i] = item; break

    def remove_item(self, item, count=1):
        if self.inventory[item] >= count:
            self.inventory[item] -= count
            if self.inventory[item] <= 0:
                del self.inventory[item]
            # Clean hotbar
            for i in range(len(self.hotbar)):
                if self.hotbar[i] == item and self.inventory.get(item, 0) <= 0:
                    self.hotbar[i] = ''
            return True
        return False

    def has_items(self, items):
        return all(self.inventory.get(k, 0) >= v for k, v in items.items())

    def get_held(self):
        return self.hotbar[self.hotbar_sel] if self.hotbar_sel < len(self.hotbar) else ''

    def get_defense(self):
        d = 0
        if self.armor_slot and self.armor_slot in self.inventory:
            d += ARMOR_DEFENSE.get(self.armor_slot, 0)
        if self.shield_slot and self.shield_slot in self.inventory:
            d += ARMOR_DEFENSE.get(self.shield_slot, 0)
        return d

    def get_damage(self):
        held = self.get_held()
        return WEAPON_DAMAGE.get(held, 1)

    def use_durability(self, tool):
        if tool in DURABILITY:
            if tool not in self.durability:
                self.durability[tool] = DURABILITY[tool]
            self.durability[tool] -= 1
            if self.durability[tool] <= 0:
                self.remove_item(tool, 1)
                del self.durability[tool]
                if self.get_held() == tool:
                    self.hotbar[self.hotbar_sel] = ''

    # ─── Mining (v3 Enhanced) ────────────────────────────────────────────
    def mine_tile(self, tx, ty, tool=None, charge_mult=1.0):
        if tx < 0 or ty < 0 or tx >= MW or ty >= MH:
            return
        terrain = self.world[ty][tx]
        if terrain == 'bedrock':
            return
        if terrain not in MINEABLE and terrain not in TERRAIN_DROPS:
            return

        # Check tool effectiveness (v3: charge multiplier boosts eff)
        eff = 1
        if tool and tool in TOOL_EFFECTIVENESS:
            eff = TOOL_EFFECTIVENESS[tool].get(terrain, 0.5) * charge_mult

        # Calculate hits needed (v3: charged mining bonus)
        base_hits = max(1, int(3 / eff))
        key = (tx, ty)
        if key not in self.crack_anim:
            self.crack_anim[key] = 0
        self.crack_anim[key] += eff

        if self.crack_anim[key] >= base_hits:
            self.crack_anim.pop(key, None)
            self.do_mine(tx, ty, terrain, tool, eff)
            return True
        return False

    def do_mine(self, tx, ty, terrain, tool, eff):
        """Execute the actual tile break and loot."""
        # v3: Check for area mining
        area = 0
        if tool and tool in PICK_AREA:
            area = PICK_AREA[tool]

        tiles_mined = [(tx, ty)]

        # v3: Area mining - mine surrounding tiles too
        if area > 0:
            for dy in range(-area, area+1):
                for dx in range(-area, area+1):
                    if dx == 0 and dy == 0: continue
                    nx, ny = tx+dx, ty+dy
                    if 0 <= nx < MW and 0 <= ny < MH:
                        nt = self.world[ny][nx]
                        if nt in MINEABLE and nt != 'bedrock':
                            tiles_mined.append((nx, ny))

        all_mined_count = len(tiles_mined)
        for mx, my in tiles_mined:
            t = self.world[my][mx]
            if t in TERRAIN_DROPS:
                drop, cnt = TERRAIN_DROPS[t]

                # v3: Ore bonus drops
                bonus = 0
                if tool and t in ORE_BONUSES:
                    bonus_map = ORE_BONUSES[t]
                    if tool in bonus_map:
                        bonus = bonus_map[tool]

                total = cnt + bonus
                self.add_item(drop, total)

                # v3: Bark from trees with axe
                if t == 'tree' and tool and 'axe' in tool:
                    if random.random() < 0.4:
                        self.add_item('bark', 1)
                    if random.random() < 0.15:
                        self.add_item('resin', 1)
                    # v3: Connected tree felling
                    if tool in AXE_FELLING and AXE_FELLING[tool]:
                        self.fell_connected_trees(mx, my)

            self.world[my][mx] = 'dirt'
            self.minimap_dirty = True

            # Particles
            for _ in range(3):
                self.particles.append(Particle(
                    mx*TILE+TILE//2, my*TILE+TILE//2,
                    random.uniform(-2,2), random.uniform(-3,-0.5),
                    random.randint(15,30), (180,160,140)))

        # v3: Achievement for area mining
        if all_mined_count > 1:
            self.unlock('area_mine')

        # v3: Achievement for tree felling
        if len(self.felling_set) > 2:
            self.unlock('tree_feller')

        self.use_durability(tool) if tool else None
        self.play(self.snd_mine)

        # XP
        xp_gain = all_mined_count
        if tool and ('pick' in tool or 'axe' in tool):
            xp_gain += all_mined_count
        self.add_xp(xp_gain)

    def fell_connected_trees(self, tx, ty):
        """v3: Recursively find and fell connected tree tiles."""
        visited = set()
        stack = [(tx, ty)]
        max_fell = 12  # Limit to prevent massive chain reactions
        count = 0
        while stack and count < max_fell:
            cx, cy = stack.pop()
            if (cx, cy) in visited: continue
            if cx < 1 or cy < 1 or cx >= MW-1 or cy >= MH-1: continue
            visited.add((cx, cy))
            t = self.world[cy][cx]
            if t == 'tree':
                self.world[cy][cx] = 'dirt'
                self.add_item('wood', 2)
                if random.random() < 0.3:
                    self.add_item('bark', 1)
                count += 1
                self.minimap_dirty = True
                for _ in range(2):
                    self.particles.append(Particle(
                        cx*TILE+TILE//2, cy*TILE+TILE//2,
                        random.uniform(-2,2), random.uniform(-3,-0.5),
                        random.randint(15,25), (139,90,43)))
                # Check 4 neighbors for more trees
                for dx, dy in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(1,-1),(-1,1),(1,1)]:
                    nx, ny = cx+dx, cy+dy
                    if (nx, ny) not in visited and 0 <= nx < MW and 0 <= ny < MH:
                        if self.world[ny][nx] == 'tree':
                            stack.append((nx, ny))
        self.felling_set = visited

    # ─── Placing & Interacting ───────────────────────────────────────────
    def place_tile(self, tx, ty):
        if tx < 1 or ty < 1 or tx >= MW-1 or ty >= MH-1: return False
        if self.world[ty][tx] not in ('dirt','grass','sand','farm_tilled'): return False

        held = self.get_held()
        terrain = None
        if held in PLACEABLE:
            terrain = held
        elif held in BUILDING_PLACE_MAP:
            terrain = BUILDING_PLACE_MAP[held]
        elif held == 'torch':
            terrain = 'torch'
        elif held == 'farm_plot':
            terrain = 'farm_plot'
        elif held == 'seed':
            if self.world[ty][tx] == 'dirt' or self.world[ty][tx] == 'farm_tilled':
                self.world[ty][tx] = 'farm_planted'
                self.farm_timers[(tx,ty)] = 0
                self.remove_item('seed', 1)
                self.unlock('farmer')
                self.play(self.snd_place)
                return True
            return False
        elif held == 'bucket':
            # Collect water if near water
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    wx, wy = tx+dx, ty+dy
                    if 0 <= wx < MW and 0 <= wy < MH and self.world[wy][wx] == 'water':
                        self.add_item('water_bucket', 1)
                        self.remove_item('bucket', 1)
                        self.play(self.snd_place)
                        return True
            return False
        else:
            return False

        if terrain:
            self.world[ty][tx] = terrain
            self.remove_item(held, 1)
            self.build_count += 1
            self.minimap_dirty = True
            self.play(self.snd_place)
            self.unlock('first_build')
            if self.build_count >= 20:
                self.unlock('master_builder')
            # v3: Well creates nearby water
            if terrain == 'well':
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        wx, wy = tx+dx, ty+dy
                        if 0 <= wx < MW and 0 <= wy < MH:
                            if self.world[wy][wx] == 'dirt':
                                self.world[wy][wx] = 'water'
                                self.well_water[(wx,wy)] = True
                self.unlock('well_digger')
            elif terrain == 'shop':
                self.unlock('shop_keeper')
            return True
        return False

    def interact_tile(self, tx, ty):
        if tx < 0 or ty < 0 or tx >= MW or ty >= MH: return
        t = self.world[ty][tx]
        if t == 'chest':
            self.show_chest = True; self.chest_pos = (tx, ty)
            self.show_craft = False; self.show_inv = False; self.show_furnace = False
        elif t == 'craft_table':
            self.show_craft = True
            self.show_inv = False; self.show_chest = False; self.show_furnace = False
        elif t == 'furnace':
            self.show_furnace = True; self.furnace_pos = (tx, ty)
            self.show_craft = False; self.show_inv = False; self.show_chest = False
        elif t == 'farm_tilled' and self.inventory.get('seed', 0) > 0:
            self.world[ty][tx] = 'farm_planted'
            self.farm_timers[(tx,ty)] = 0
            self.remove_item('seed', 1)
            self.play(self.snd_place)
        elif t == 'bed':
            self.hp = self.max_hp; self.hunger = min(self.hunger + 5, self.max_hunger)
        elif t == 'anvil':
            # Anvil: repair held tool to full durability
            held = self.get_held()
            if held in DURABILITY and held in self.durability:
                self.durability[held] = DURABILITY[held]
                self.play(self.snd_craft)
        elif t == 'well':
            self.hunger = min(self.hunger + 3, self.max_hunger)
        elif t == 'shop':
            # Shop: trade 10 wheat for 1 golden apple
            if self.inventory.get('wheat', 0) >= 10:
                self.remove_item('wheat', 10)
                self.add_item('golden_apple', 1)
                self.play(self.snd_craft)

    def do_craft(self, recipe_idx, count=1):
        if recipe_idx >= len(RECIPES): return
        result, qty, ingredients = RECIPES[recipe_idx]
        for _ in range(count):
            if not self.has_items(ingredients): break
            for k, v in ingredients.items():
                self.remove_item(k, v)
            self.add_item(result, qty)
            if result in DURABILITY:
                self.durability[result] = DURABILITY[result]
        self.play(self.snd_craft)
        self.unlock('first_craft')
        # Check iron/diamond tool achievements
        if 'iron' in result and ('pick' in result or 'axe' in result or 'sword' in result):
            self.unlock('iron_tools')
        if 'diamond' in result and ('pick' in result or 'axe' in result or 'sword' in result):
            self.unlock('diamond_tools')

    def do_smelt(self):
        if not self.furnace_input: return
        if self.furnace_input not in SMELTING_RECIPES: return
        result, qty, fuel_needed = SMELTING_RECIPES[self.furnace_input]
        if self.furnace_timer > 0:
            self.furnace_timer -= 1
            if self.furnace_timer <= 0:
                self.remove_item(self.furnace_input, 1)
                self.add_item(result, qty)
                self.furnace_input = None
                self.play(self.snd_craft)

    def start_smelt(self, item):
        if item in SMELTING_RECIPES and self.inventory.get(item, 0) > 0:
            self.furnace_input = item
            _, _, fuel = SMELTING_RECIPES[item]
            self.furnace_timer = fuel

    # ─── Combat ──────────────────────────────────────────────────────────
    def attack(self):
        held = self.get_held()
        dmg = self.get_damage()
        # Direction from keys
        dx, dy = 0, 0
        if 'w' in self.keys_held: dy = -1
        if 's' in self.keys_held: dy = 1
        if 'a' in self.keys_held: dx = -1
        if 'd' in self.keys_held: dx = 1
        if dx == 0 and dy == 0: dx = 1  # Default right
        ax = self.px + dx * 1.5; ay = self.py + dy * 1.5
        for e in self.enemies:
            dist = math.sqrt((e.x - ax)**2 + (e.y - ay)**2)
            if dist < 2.0:
                e.hp -= dmg
                e.knockback_x = dx * 5
                e.knockback_y = dy * 5
                e.kb_timer = 10
                self.play(self.snd_hit)
                self.dmg_numbers.append([e.x*TILE, e.y*TILE-10, str(dmg), 40, (255,50,50)])
                self.use_durability(held)
                if e.hp <= 0:
                    for item, cnt in e.loot.items():
                        self.add_item(item, cnt)
                    self.add_xp(e.xp)
                    self.unlock('enemy_slain')
        # Also use durability for swords
        if held in WEAPON_DAMAGE:
            self.use_durability(held)

    # ─── Farm Growth ─────────────────────────────────────────────────────
    def update_farms(self):
        keys_to_update = list(self.farm_timers.keys())
        for (fx, fy) in keys_to_update:
            if 0 <= fx < MW and 0 <= fy < MH:
                t = self.world[fy][fx]
                if t == 'farm_planted':
                    self.farm_timers[(fx, fy)] += 1
                    if self.farm_timers[(fx, fy)] > 300:
                        self.world[fy][fx] = 'farm_growing'
                elif t == 'farm_growing':
                    self.farm_timers[(fx, fy)] += 1
                    if self.farm_timers[(fx, fy)] > 600:
                        self.world[fy][fx] = 'farm_ready'
                        self.farm_timers.pop((fx, fy), None)

    # ─── Day/Night & Weather ─────────────────────────────────────────────
    def get_sky_color(self):
        t = (self.day_time % self.day_length) / self.day_length
        if t < 0.25:  # Dawn
            f = t / 0.25
            return (int(40+140*f), int(40+160*f), int(80+120*f))
        elif t < 0.5:  # Day
            return (180, 200, 240)
        elif t < 0.65:  # Dusk
            f = (t - 0.5) / 0.15
            return (int(180-100*f), int(200-120*f), int(240-120*f))
        else:  # Night
            return (30, 30, 60)

    def is_night(self):
        t = (self.day_time % self.day_length) / self.day_length
        return t >= 0.65 or t < 0.1

    def update_weather(self):
        self.weather_timer -= 1
        if self.weather_timer <= 0:
            self.weather = random.choice(['clear','clear','rain','storm','snow','clear'])
            self.weather_timer = random.randint(600, 1800)
        if self.weather in ('rain', 'storm', 'snow'):
            for _ in range(3 if self.weather == 'storm' else 1):
                wx = random.randint(0, SW)
                wy = random.randint(-20, 0)
                c = (100,100,255) if self.weather != 'snow' else (220,220,255)
                self.weather_particles.append([wx, wy, random.uniform(3,7), random.uniform(1,3), c])
        # Update weather particles
        new_wp = []
        for wp in self.weather_particles:
            wp[1] += wp[3]
            wp[0] += wp[2] * 0.3
            if wp[1] < SH + 20:
                new_wp.append(wp)
        self.weather_particles = new_wp[-500:]  # Limit

    # ─── Enemy Spawning ──────────────────────────────────────────────────
    def update_enemies(self):
        if self.is_night():
            self.spawn_timer += 1
            if self.spawn_timer > 120 and len(self.enemies) < 8:
                self.spawn_timer = 0
                angle = random.uniform(0, 2*math.pi)
                dist = random.uniform(15, 25)
                ex = self.px + math.cos(angle)*dist
                ey = self.py + math.sin(angle)*dist
                ex = max(1, min(MW-2, int(ex)))
                ey = max(1, min(MH-2, int(ey)))
                if self.world[ey][ex] not in ('water','bedrock'):
                    etype = random.choice(['slime','zombie','goblin','skeleton'])
                    self.enemies.append(Enemy(ex, ey, etype))
        for e in self.enemies[:]:
            e.update(self.px, self.py)
            # Check collision with player
            dx = e.x - self.px; dy = e.y - self.py
            dist = math.sqrt(dx*dx + dy*dy)
            if dist < 1.0 and self.damage_cooldown <= 0:
                dmg = max(1, e.damage - self.get_defense())
                self.hp -= dmg
                self.damage_cooldown = 30
                self.dmg_numbers.append([self.px*TILE, self.py*TILE-20, str(dmg), 40, (255,0,0)])
                self.play(self.snd_hit)
            # Remove dead enemies
            if e.hp <= 0:
                self.enemies.remove(e)
            # Remove far enemies
            elif dist > 40:
                self.enemies.remove(e)

    # ─── XP & Level ──────────────────────────────────────────────────────
    def add_xp(self, amount):
        self.xp += amount
        while self.xp >= self.xp_next:
            self.xp -= self.xp_next
            self.level += 1
            self.xp_next = int(self.xp_next * 1.5)
            self.max_hp += 2
            self.hp = min(self.hp + 2, self.max_hp)

    # ─── Achievements ────────────────────────────────────────────────────
    def unlock(self, key):
        if key not in self.achievements and key in ACHIEVEMENTS:
            self.achievements.add(key)
            name, desc, emoji = ACHIEVEMENTS[key]
            self.ach_popup = (name, desc, emoji)
            self.ach_timer = 180
            self.play(self.snd_ach)

    # ─── Particles ───────────────────────────────────────────────────────
    def update_particles(self):
        new_p = []
        for p in self.particles:
            p.x += p.vx; p.y += p.vy; p.vy += 0.1; p.life -= 1
            if p.life > 0: new_p.append(p)
        self.particles = new_p[-300:]
        new_d = []
        for d in self.dmg_numbers:
            d[1] -= 1; d[3] -= 1
            if d[3] > 0: new_d.append(d)
        self.dmg_numbers = new_d

    # ─── Save/Load ───────────────────────────────────────────────────────
    def save_game(self):
        data = {
            'seed': self.seed, 'world': self.world,
            'px': self.px, 'py': self.py,
            'hp': self.hp, 'max_hp': self.max_hp,
            'hunger': self.hunger, 'max_hunger': self.max_hunger,
            'xp': self.xp, 'level': self.level, 'xp_next': self.xp_next,
            'inventory': dict(self.inventory),
            'hotbar': self.hotbar, 'hotbar_sel': self.hotbar_sel,
            'durability': self.durability,
            'armor_slot': self.armor_slot, 'shield_slot': self.shield_slot,
            'day_time': self.day_time, 'weather': self.weather,
            'achievements': list(self.achievements),
            'build_count': self.build_count,
            'farm_timers': {f"{k[0]},{k[1]}": v for k, v in self.farm_timers.items()},
        }
        try:
            with open(SAVE_FILE, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Save failed: {e}")

    def load_game(self):
        if not os.path.exists(SAVE_FILE): return False
        try:
            with open(SAVE_FILE, 'r') as f:
                data = json.load(f)
            self.seed = data['seed']; self.world = data['world']
            self.px = data['px']; self.py = data['py']
            self.px_f = float(self.px); self.py_f = float(self.py)
            self.hp = data['hp']; self.max_hp = data.get('max_hp', 20)
            self.hunger = data['hunger']; self.max_hunger = data.get('max_hunger', 20)
            self.xp = data['xp']; self.level = data['level']; self.xp_next = data.get('xp_next', 50)
            self.inventory = defaultdict(int, data['inventory'])
            self.hotbar = data['hotbar']; self.hotbar_sel = data['hotbar_sel']
            self.durability = data.get('durability', {})
            self.armor_slot = data.get('armor_slot'); self.shield_slot = data.get('shield_slot')
            self.day_time = data.get('day_time', 0)
            self.weather = data.get('weather', 'clear')
            self.achievements = set(data.get('achievements', []))
            self.build_count = data.get('build_count', 0)
            ft = data.get('farm_timers', {})
            self.farm_timers = {(int(k.split(',')[0]), int(k.split(',')[1])): v for k, v in ft.items()}
            self.minimap_dirty = True
            return True
        except Exception as e:
            print(f"Load failed: {e}")
            return False

    # ─── Drawing ─────────────────────────────────────────────────────────
    def world_to_screen(self, wx, wy):
        return (int(wx * TILE - self.cam_x), int(wy * TILE - self.cam_y))

    def draw_world(self):
        sky = self.get_sky_color()
        self.screen.fill(sky)

        # Stars at night
        if self.is_night():
            random.seed(42)
            for _ in range(60):
                sx = random.randint(0, SW)
                sy = random.randint(0, SH//2)
                br = 150 + int(50 * math.sin(self.frame * 0.05 + sx))
                self.screen.set_at((sx, sy), (br, br, br))
            random.seed()

        # Calculate visible range
        sx_start = max(0, int(self.cam_x // TILE) - 1)
        sy_start = max(0, int(self.cam_y // TILE) - 1)
        sx_end = min(MW, sx_start + SW // TILE + 3)
        sy_end = min(MH, sy_start + SH // TILE + 3)

        for ty in range(sy_start, sy_end):
            for tx in range(sx_start, sx_end):
                terrain = self.world[ty][tx]
                emoji = TERRAIN_EMOJIS.get(terrain, '⬜')
                scr_x, scr_y = self.world_to_screen(tx, ty)
                if -TILE < scr_x < SW + TILE and -TILE < scr_y < SH + TILE:
                    surf = self.get_emoji_surf(emoji)
                    self.screen.blit(surf, (scr_x + 3, scr_y + 3))

                    # Torch glow
                    if terrain == 'torch':
                        glow = pygame.Surface((TILE*3, TILE*3), pygame.SRCALPHA)
                        glow.fill((255, 200, 50, 25))
                        self.screen.blit(glow, (scr_x - TILE, scr_y - TILE))

                    # Water wave
                    if terrain == 'water':
                        alpha = int(128 + 40 * math.sin(self.frame * 0.05 + tx * 0.5))
                        ws = pygame.Surface((TILE, TILE), pygame.SRCALPHA)
                        ws.fill((50, 100, 255, alpha))
                        self.screen.blit(ws, (scr_x, scr_y))

                    # Farm bobbing
                    if terrain == 'farm_ready':
                        off = int(2 * math.sin(self.frame * 0.08 + tx))
                        self.screen.blit(surf, (scr_x + 3, scr_y + 3 + off))

                    # Crack overlay
                    if (tx, ty) in self.crack_anim:
                        pct = self.crack_anim[(tx, ty)]
                        cs = pygame.Surface((TILE, TILE), pygame.SRCALPHA)
                        n_cracks = int(pct)
                        for i in range(min(n_cracks, 5)):
                            cx = random.Random(tx*100+ty+i).randint(5, TILE-5)
                            cy = random.Random(ty*100+tx+i).randint(5, TILE-5)
                            pygame.draw.line(cs, (0,0,0,150), (TILE//2, TILE//2), (cx, cy), 2)
                        self.screen.blit(cs, (scr_x, scr_y))

        # Night darkness overlay
        if self.is_night():
            dark = pygame.Surface((SW, SH), pygame.SRCALPHA)
            dark.fill((0, 0, 30, 100))
            # Light around player
            psx, psy = self.world_to_screen(self.px, self.py)
            for r in range(5, 0, -1):
                pygame.draw.circle(dark, (0,0,0,0), (psx+TILE//2, psy+TILE//2), r*TILE)
            self.screen.blit(dark, (0, 0))

        # Draw enemies
        for e in self.enemies:
            esx, esy = self.world_to_screen(e.x, e.y)
            if -TILE < esx < SW+TILE and -TILE < esy < SH+TILE:
                es = self.get_emoji_surf(e.emoji)
                self.screen.blit(es, (esx+3, esy+3))
                # HP bar
                bar_w = TILE - 4
                hp_pct = e.hp / e.max_hp
                pygame.draw.rect(self.screen, (80,0,0), (esx+2, esy-6, bar_w, 4))
                pygame.draw.rect(self.screen, (0,200,0), (esx+2, esy-6, int(bar_w*hp_pct), 4))

        # Draw player
        psx, psy = self.world_to_screen(self.px, self.py)
        player_emoji = '🧑'
        if self.frame % 30 < 15 and (self.keys_held & {'w','a','s','d'}):
            player_emoji = '🚶'
        ps = self.get_emoji_surf(player_emoji)
        self.screen.blit(ps, (psx+3, psy+3))

        # v3: Charge indicator
        if self.is_charging:
            charge_pct = (self.frame - self.charge_start) / self.max_charge
            charge_pct = min(charge_pct, 1.0)
            bar_len = int(TILE * charge_pct)
            color = (int(255*charge_pct), int(255*(1-charge_pct)), 0)
            pygame.draw.rect(self.screen, color, (psx, psy-10, bar_len, 4))

        # Draw particles
        for p in self.particles:
            px_s, py_s = self.world_to_screen(p.x/TILE, p.y/TILE)
            alpha = int(255 * p.life / p.max_life)
            ps2 = pygame.Surface((4,4), pygame.SRCALPHA)
            ps2.fill((*p.color, alpha))
            self.screen.blit(ps2, (px_s, py_s))

        # Draw damage numbers
        for d in self.dmg_numbers:
            dx_s, dy_s = self.world_to_screen(d[0]/TILE, d[1]/TILE)
            alpha = int(255 * d[3] / 40)
            txt = self.ui_font.render(d[2], True, d[4])
            txt.set_alpha(alpha)
            self.screen.blit(txt, (dx_s, dy_s))

        # Weather particles
        for wp in self.weather_particles:
            if self.weather == 'snow':
                pygame.draw.circle(self.screen, wp[4], (int(wp[0]), int(wp[1])), 2)
            else:
                pygame.draw.line(self.screen, wp[4],
                    (int(wp[0]), int(wp[1])), (int(wp[0]+1), int(wp[1]+wp[3])), 1)

        # Lightning
        if self.weather == 'storm' and random.random() < 0.005:
            flash = pygame.Surface((SW, SH), pygame.SRCALPHA)
            flash.fill((255, 255, 255, 100))
            self.screen.blit(flash, (0, 0))

    def draw_hotbar(self):
        bar_w = len(self.hotbar) * 44 + 8
        bar_x = (SW - bar_w) // 2
        bar_y = SH - 52
        bg = pygame.Surface((bar_w, 48), pygame.SRCALPHA)
        bg.fill((0, 0, 0, 160))
        self.screen.blit(bg, (bar_x, bar_y))
        for i, item in enumerate(self.hotbar):
            x = bar_x + 4 + i * 44
            y = bar_y + 4
            if i == self.hotbar_sel:
                pygame.draw.rect(self.screen, (255, 215, 0), (x-2, y-2, 40, 40), 2)
            pygame.draw.rect(self.screen, (60, 60, 60), (x, y, 36, 36))
            if item and item in ITEM_EMOJIS:
                es = self.get_emoji_surf(ITEM_EMOJIS[item], 30)
                self.screen.blit(es, (x+3, y+3))
                cnt = self.inventory.get(item, 0)
                if cnt > 0:
                    ct = self.ui_font_sm.render(str(cnt), True, (255,255,255))
                    self.screen.blit(ct, (x+26-ct.get_width(), y+24))
            # Durability bar
            if item and item in self.durability:
                max_d = DURABILITY.get(item, 100)
                pct = self.durability[item] / max_d
                dc = (0,255,0) if pct > 0.5 else (255,255,0) if pct > 0.2 else (255,0,0)
                pygame.draw.rect(self.screen, dc, (x, y+34, int(36*pct), 2))

        # v3: Show current tool info at bottom
        held = self.get_held()
        if held:
            name = ITEM_NAMES.get(held, held)
            info_parts = [name]
            if held in PICK_AREA and PICK_AREA[held] > 0:
                r = PICK_AREA[held]
                info_parts.append(f"Area: {r*2+1}x{r*2+1}")
            if held in AXE_FELLING and AXE_FELLING[held]:
                info_parts.append("Felling: ON")
            if held in TOOL_EFFECTIVENESS:
                info_parts.append("Hold LMB to charge")
            info_txt = " | ".join(info_parts)
            it = self.ui_font_sm.render(info_txt, True, (200, 200, 200))
            self.screen.blit(it, (bar_x, bar_y - 18))

    def draw_hud(self):
        # HP bar
        pygame.draw.rect(self.screen, (60,0,0), (10, 10, 200, 16))
        pygame.draw.rect(self.screen, (200,30,30), (10, 10, int(200*self.hp/self.max_hp), 16))
        ht = self.ui_font.render(f"HP: {self.hp}/{self.max_hp}", True, (255,255,255))
        self.screen.blit(ht, (15, 10))
        # Hunger bar
        pygame.draw.rect(self.screen, (60,40,0), (10, 30, 200, 16))
        pygame.draw.rect(self.screen, (200,150,30), (10, 30, int(200*self.hunger/self.max_hunger), 16))
        ht2 = self.ui_font.render(f"Hunger: {self.hunger}/{self.max_hunger}", True, (255,255,255))
        self.screen.blit(ht2, (15, 30))
        # XP / Level
        lt = self.ui_font.render(f"Lv.{self.level}  XP: {self.xp}/{self.xp_next}", True, (255,255,100))
        self.screen.blit(lt, (10, 52))
        # Day time
        t = (self.day_time % self.day_length) / self.day_length
        period = "Night" if self.is_night() else "Day"
        dt_txt = self.ui_font.render(f"{period} | Weather: {self.weather} | Seed: {self.seed}", True, (200,200,200))
        self.screen.blit(dt_txt, (10, 72))
        # Controls hint
        hints = "WASD:Move | LMB:Mine/Attack | RMB:Place | E:Interact | C:Craft | I:Inv | F:Eat | M:Map | F5:Save F9:Load"
        ht3 = self.ui_font_sm.render(hints, True, (150,150,150))
        self.screen.blit(ht3, (10, SH - 70))
        # Defense
        df = self.get_defense()
        if df > 0:
            dt2 = self.ui_font.render(f"DEF: {df}", True, (100,200,255))
            self.screen.blit(dt2, (220, 10))
        # Achievement popup
        if self.ach_timer > 0:
            self.ach_timer -= 1
            if self.ach_popup:
                name, desc, emoji = self.ach_popup
                ap_w = 300; ap_x = (SW - ap_w)//2
                ap_y = 100 - max(0, (180 - self.ach_timer)) * 2
                if ap_y < -60: ap_y = -60
                ap_bg = pygame.Surface((ap_w, 50), pygame.SRCALPHA)
                ap_bg.fill((0, 0, 0, 180))
                self.screen.blit(ap_bg, (ap_x, ap_y))
                at = self.ui_font.render(f"{emoji} Achievement: {name}", True, (255, 215, 0))
                self.screen.blit(at, (ap_x+10, ap_y+5))
                at2 = self.ui_font_sm.render(desc, True, (200, 200, 200))
                self.screen.blit(at2, (ap_x+10, ap_y+28))

    def draw_minimap(self):
        if not self.show_map: return
        mm_w, mm_h = 200, 150
        mm_x, mm_y = SW - mm_w - 10, 10
        if self.minimap_dirty or self.minimap_surf is None:
            self.minimap_surf = pygame.Surface((mm_w, mm_h))
            for my in range(MH):
                for mx in range(MW):
                    t = self.world[my][mx]
                    c = {
                        'grass':(34,139,34),'dirt':(139,90,43),'stone':(128,128,128),
                        'water':(30,80,200),'sand':(210,180,100),'tree':(0,100,0),
                        'bedrock':(40,40,40),'snow_grass':(200,220,240),'ice':(150,200,255),
                    }.get(t, (100,100,100))
                    px = int(mx * mm_w / MW)
                    py = int(my * mm_h / MH)
                    pw = max(1, int(mm_w / MW) + 1)
                    ph = max(1, int(mm_h / MH) + 1)
                    self.minimap_surf.fill(c, (px, py, pw, ph))
            self.minimap_dirty = False
        self.screen.blit(self.minimap_surf, (mm_x, mm_y))
        # Player dot
        pdx = int(self.px * mm_w / MW)
        pdy = int(self.py * mm_h / MH)
        pygame.draw.circle(self.screen, (255, 50, 50), (mm_x + pdx, mm_y + pdy), 3)
        # Border
        pygame.draw.rect(self.screen, (200, 200, 200), (mm_x, mm_y, mm_w, mm_h), 1)

    def draw_crafting_panel(self):
        if not self.show_craft: return
        pw, ph = 500, 500
        px_p, py_p = (SW - pw) // 2, (SH - ph) // 2
        bg = pygame.Surface((pw, ph), pygame.SRCALPHA)
        bg.fill((20, 20, 30, 230))
        self.screen.blit(bg, (px_p, py_p))
        pygame.draw.rect(self.screen, (100, 100, 150), (px_p, py_p, pw, ph), 2)
        title = self.ui_font_lg.render("Crafting Table", True, (255, 215, 0))
        self.screen.blit(title, (px_p + 10, py_p + 5))

        self.craft_rects = []
        y_off = 35
        for i, (result, qty, ingredients) in enumerate(RECIPES):
            if y_off + 28 > ph - 40: break
            can = self.has_items(ingredients)
            color = (40, 60, 40) if can else (40, 40, 40)
            rx = px_p + 5; ry = py_p + y_off
            rect = pygame.Rect(rx, ry, pw - 10, 26)
            self.craft_rects.append((rect, i))
            if can:
                pygame.draw.rect(self.screen, color, rect)
            # Result
            name = ITEM_NAMES.get(result, result)
            emoji = ITEM_EMOJIS.get(result, '❓')
            es = self.get_emoji_surf(emoji, 18)
            self.screen.blit(es, (rx + 3, ry + 4))
            txt_color = (200, 255, 200) if can else (150, 150, 150)
            rt = self.ui_font_sm.render(f"{name} x{qty}", True, txt_color)
            self.screen.blit(rt, (rx + 22, ry + 5))
            # Ingredients
            ing_parts = []
            for k, v in ingredients.items():
                kn = ITEM_NAMES.get(k, k)
                have = self.inventory.get(k, 0)
                c = (150, 255, 150) if have >= v else (255, 100, 100)
                ing_parts.append((f"{kn}:{have}/{v}", c))
            ix = rx + 180
            for part, c in ing_parts:
                it = self.ui_font_sm.render(part, True, c)
                self.screen.blit(it, (ix, ry + 5))
                ix += it.get_width() + 10
            y_off += 28

        # Craft All button
        self.craft_all_rect = pygame.Rect(px_p + pw - 110, py_p + ph - 35, 100, 28)
        pygame.draw.rect(self.screen, (60, 100, 60), self.craft_all_rect)
        ca_t = self.ui_font.render("Craft All", True, (255, 255, 255))
        self.screen.blit(ca_t, (self.craft_all_rect.x + 15, self.craft_all_rect.y + 5))

    def draw_inventory_panel(self):
        if not self.show_inv: return
        pw, ph = 450, 500
        px_p, py_p = (SW - pw) // 2, (SH - ph) // 2
        bg = pygame.Surface((pw, ph), pygame.SRCALPHA)
        bg.fill((20, 20, 30, 230))
        self.screen.blit(bg, (px_p, py_p))
        pygame.draw.rect(self.screen, (100, 100, 150), (px_p, py_p, pw, ph), 2)
        title = self.ui_font_lg.render("Inventory", True, (255, 215, 0))
        self.screen.blit(title, (px_p + 10, py_p + 5))

        # Armor/Shield slots
        self.inv_slot_rects = {}
        y = py_p + 35
        for slot_name in ['armor_slot', 'shield_slot']:
            item = getattr(self, slot_name, None)
            rect = pygame.Rect(px_p + 10, y, 36, 36)
            self.inv_slot_rects[slot_name] = rect
            pygame.draw.rect(self.screen, (60, 60, 80), rect)
            if item and item in ITEM_EMOJIS:
                es = self.get_emoji_surf(ITEM_EMOJIS[item], 28)
                self.screen.blit(es, (rect.x + 4, rect.y + 4))
            label = "Armor" if slot_name == 'armor_slot' else "Shield"
            lt = self.ui_font_sm.render(label, True, (180, 180, 180))
            self.screen.blit(lt, (rect.x + 40, rect.y + 10))
            y += 42

        # Items list
        items_sorted = sorted(self.inventory.items(), key=lambda x: ITEM_NAMES.get(x[0], x[0]))
        y += 5
        for item, count in items_sorted:
            if y + 22 > py_p + ph - 10: break
            emoji = ITEM_EMOJIS.get(item, '❓')
            name = ITEM_NAMES.get(item, item)
            es = self.get_emoji_surf(emoji, 16)
            self.screen.blit(es, (px_p + 15, y + 2))
            it = self.ui_font_sm.render(f"{name}: {count}", True, (200, 200, 200))
            self.screen.blit(it, (px_p + 35, y + 3))
            y += 22

    def draw_chest_panel(self):
        if not self.show_chest: return
        pw, ph = 400, 400
        px_p, py_p = (SW - pw) // 2, (SH - ph) // 2
        bg = pygame.Surface((pw, ph), pygame.SRCALPHA)
        bg.fill((30, 20, 10, 230))
        self.screen.blit(bg, (px_p, py_p))
        pygame.draw.rect(self.screen, (150, 100, 50), (px_p, py_p, pw, ph), 2)
        title = self.ui_font_lg.render("Chest", True, (255, 200, 100))
        self.screen.blit(title, (px_p + 10, py_p + 5))

        y = py_p + 35
        self.chest_item_rects = []
        for item, count in sorted(self.chest_inv.items()):
            if count <= 0: continue
            if y + 22 > py_p + ph - 40: break
            emoji = ITEM_EMOJIS.get(item, '❓')
            name = ITEM_NAMES.get(item, item)
            rect = pygame.Rect(px_p + 5, y, pw - 10, 22)
            self.chest_item_rects.append((rect, item))
            es = self.get_emoji_surf(emoji, 16)
            self.screen.blit(es, (px_p + 10, y + 2))
            it = self.ui_font_sm.render(f"{name}: {count}  [Click to take 1]", True, (200, 200, 200))
            self.screen.blit(it, (px_p + 30, y + 3))
            y += 24

    def draw_furnace_panel(self):
        if not self.show_furnace: return
        pw, ph = 350, 300
        px_p, py_p = (SW - pw) // 2, (SH - ph) // 2
        bg = pygame.Surface((pw, ph), pygame.SRCALPHA)
        bg.fill((30, 15, 10, 230))
        self.screen.blit(bg, (px_p, py_p))
        pygame.draw.rect(self.screen, (200, 100, 50), (px_p, py_p, pw, ph), 2)
        title = self.ui_font_lg.render("Furnace", True, (255, 150, 50))
        self.screen.blit(title, (px_p + 10, py_p + 5))

        y = py_p + 40
        self.furnace_rects = []
        for item, (result, qty, fuel) in SMELTING_RECIPES.items():
            if self.inventory.get(item, 0) <= 0: continue
            rect = pygame.Rect(px_p + 5, y, pw - 10, 24)
            self.furnace_rects.append((rect, item))
            is_current = self.furnace_input == item
            c = (80, 50, 20) if is_current else (40, 30, 15)
            pygame.draw.rect(self.screen, c, rect)
            name = ITEM_NAMES.get(item, item)
            rname = ITEM_NAMES.get(result, result)
            t = self.ui_font_sm.render(f"{name} -> {rname} x{qty}", True, (255, 200, 150))
            self.screen.blit(t, (px_p + 10, y + 4))
            if is_current and self.furnace_timer > 0:
                pct = 1.0 - self.furnace_timer / fuel
                pygame.draw.rect(self.screen, (255, 100, 0), (px_p + pw - 110, y + 8, int(100*pct), 10))
            y += 28

        if self.furnace_input:
            t2 = self.ui_font.render(f"Smelting: {ITEM_NAMES.get(self.furnace_input, '')}", True, (255, 200, 100))
            self.screen.blit(t2, (px_p + 10, py_p + ph - 35))

    # ─── Main Loop ───────────────────────────────────────────────────────
    def handle_events(self):
        mouse_held = pygame.mouse.get_pressed()[0]
        rmb_held = pygame.mouse.get_pressed()[2]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.keys_held.add(event.unicode.lower() if event.unicode.isalpha() else event.key)
                if event.key == pygame.K_ESCAPE:
                    self.show_craft = False; self.show_inv = False
                    self.show_chest = False; self.show_furnace = False
                    self.show_map = False
                elif event.key == pygame.K_c:
                    self.show_craft = not self.show_craft
                    self.show_inv = False; self.show_chest = False; self.show_furnace = False
                elif event.key == pygame.K_i:
                    self.show_inv = not self.show_inv
                    self.show_craft = False; self.show_chest = False; self.show_furnace = False
                elif event.key == pygame.K_m:
                    self.show_map = not self.show_map
                elif event.key == pygame.K_f:
                    # Eat food
                    for food in ['golden_apple','cooked_meat','mushroom_stew','bread','apple']:
                        if self.inventory.get(food, 0) > 0:
                            heal = FOOD_HEAL.get(food, 1)
                            self.hp = min(self.hp + heal, self.max_hp)
                            self.hunger = min(self.hunger + heal, self.max_hunger)
                            self.remove_item(food, 1)
                            self.play(self.snd_eat)
                            break
                elif event.key == pygame.K_F5:
                    self.save_game()
                elif event.key == pygame.K_F9:
                    self.load_game()
                elif event.key == pygame.K_e:
                    # Interact with facing tile
                    dx, dy = 0, 0
                    if 'w' in self.keys_held: dy = -1
                    if 's' in self.keys_held: dy = 1
                    if 'a' in self.keys_held: dx = -1
                    if 'd' in self.keys_held: dx = 1
                    if dx == 0 and dy == 0: dx = 1
                    self.interact_tile(self.px + dx, self.py + dy)
                # Hotbar number keys
                elif event.key in range(pygame.K_1, pygame.K_1 + 9):
                    idx = event.key - pygame.K_1
                    if idx < len(self.hotbar):
                        self.hotbar_sel = idx
            elif event.type == pygame.KEYUP:
                ch = event.unicode.lower() if event.unicode.isalpha() else event.key
                self.keys_held.discard(ch)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if event.button == 1:  # Left click
                    # Check UI panels first
                    if self.show_craft and hasattr(self, 'craft_rects'):
                        for rect, idx in self.craft_rects:
                            if rect.collidepoint(mx, my):
                                self.do_craft(idx); break
                        if hasattr(self, 'craft_all_rect') and self.craft_all_rect.collidepoint(mx, my):
                            for idx in range(len(RECIPES)):
                                self.do_craft(idx, 99)
                    elif self.show_chest and hasattr(self, 'chest_item_rects'):
                        for rect, item in self.chest_item_rects:
                            if rect.collidepoint(mx, my):
                                if self.chest_inv.get(item, 0) > 0:
                                    self.chest_inv[item] -= 1
                                    self.add_item(item, 1)
                                break
                    elif self.show_furnace and hasattr(self, 'furnace_rects'):
                        for rect, item in self.furnace_rects:
                            if rect.collidepoint(mx, my):
                                self.start_smelt(item); break
                    elif self.show_inv and hasattr(self, 'inv_slot_rects'):
                        for slot_name, rect in self.inv_slot_rects.items():
                            if rect.collidepoint(mx, my):
                                held = self.get_held()
                                current = getattr(self, slot_name, None)
                                if held in ARMOR_DEFENSE or held in ('iron_armor','diamond_armor','shield'):
                                    setattr(self, slot_name, held)
                                elif current:
                                    setattr(self, slot_name, None)
                    else:
                        # Start charging for mining
                        self.is_charging = True
                        self.charge_start = self.frame
                elif event.button == 3:  # Right click - place
                    wx = int((mx + self.cam_x) / TILE)
                    wy = int((my + self.cam_y) / TILE)
                    dx = abs(wx - self.px); dy = abs(wy - self.py)
                    if dx + dy <= 6:
                        self.place_tile(wx, wy)
                elif event.button == 4:  # Scroll up
                    self.hotbar_sel = (self.hotbar_sel - 1) % len(self.hotbar)
                elif event.button == 5:  # Scroll down
                    self.hotbar_sel = (self.hotbar_sel + 1) % len(self.hotbar)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.is_charging = False

        # Continuous mining while LMB held
        if mouse_held and not self.show_craft and not self.show_inv and not self.show_chest and not self.show_furnace:
            mx, my = pygame.mouse.get_pos()
            wx = int((mx + self.cam_x) / TILE)
            wy = int((my + self.cam_y) / TILE)
            dx = abs(wx - self.px); dy = abs(wy - self.py)
            if dx + dy <= 6:
                tool = self.get_held()
                if tool and ('pick' in tool or 'axe' in tool):
                    # v3: Charge bonus - longer hold = more effective mining
                    charge_mult = 1.0
                    if self.is_charging:
                        charge_frames = self.frame - self.charge_start
                        charge_mult = 1.0 + min(charge_frames / self.max_charge, 1.0) * 1.0
                    self.mine_tile(wx, wy, tool, charge_mult)
                else:
                    self.mine_tile(wx, wy, tool)

                # Attack with sword-like weapons
                held = self.get_held()
                if held in WEAPON_DAMAGE:
                    if self.frame % 15 == 0:
                        self.attack()
            self.unlock('first_mine')

    def update(self):
        # Player movement
        speed = 0.08
        if 'w' in self.keys_held: self.py_f -= speed
        if 's' in self.keys_held: self.py_f += speed
        if 'a' in self.keys_held: self.px_f -= speed
        if 'd' in self.keys_held: self.px_f += speed
        # Clamp
        self.px_f = max(1, min(MW-2, self.px_f))
        self.py_f = max(1, min(MH-2, self.py_f))
        # Check walkable
        ntx, nty = int(self.px_f), int(self.py_f)
        t = self.world[nty][ntx] if 0 <= ntx < MW and 0 <= nty < MH else 'bedrock'
        if t not in ('water', 'bedrock'):
            self.px = ntx; self.py = nty
        else:
            self.px_f = float(self.px); self.py_f = float(self.py)

        # Camera
        target_cx = self.px * TILE - SW // 2 + TILE // 2
        target_cy = self.py * TILE - SH // 2 + TILE // 2
        self.cam_x += (target_cx - self.cam_x) * 0.1
        self.cam_y += (target_cy - self.cam_y) * 0.1

        # Hunger drain
        if self.frame % 300 == 0:
            self.hunger = max(0, self.hunger - 1)
            if self.hunger <= 0:
                self.hp = max(0, self.hp - 1)
        # Regen with food
        if self.hunger > 15 and self.frame % 60 == 0:
            self.hp = min(self.hp + 1, self.max_hp)

        # Damage cooldown
        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1

        # Death / respawn
        if self.hp <= 0:
            self.hp = self.max_hp; self.hunger = self.max_hunger
            self.px = MW // 2; self.py = MH // 2
            self.px_f = float(self.px); self.py_f = float(self.py)
            # Drop some items
            for item in list(self.inventory.keys())[:5]:
                self.remove_item(item, self.inventory[item] // 2)

        # Day/night
        self.day_time += 1
        if int(self.day_time) % self.day_length == 0 and self.day_time > 0:
            self.unlock('night_survive')

        # Weather
        self.update_weather()

        # Enemies
        self.update_enemies()

        # Farms
        self.update_farms()

        # Particles
        self.update_particles()

        # Furnace
        if self.show_furnace and self.furnace_input:
            self.do_smelt()

        # Minimap update
        if self.frame % 120 == 0:
            self.minimap_dirty = True

        self.frame += 1

    def draw(self):
        self.draw_world()
        self.draw_hotbar()
        self.draw_hud()
        self.draw_minimap()
        self.draw_crafting_panel()
        self.draw_inventory_panel()
        self.draw_chest_panel()
        self.draw_furnace_panel()
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()

# ─── Entry Point ─────────────────────────────────────────────────────────────
if __name__ == '__main__':
    game = Game()
    game.run()