import csv

from discord import Colour

def load_store(file_name):
    store_file = None
    try:
        store_file = open(f"./{file_name}", 'r')
    except FileNotFoundError:
        return [], False
    
    reader = csv.reader(store_file)
    header = next(reader)
    data = []
    for row in reader:
        imageUrl = row[0]
        manifestId = int(row[1])
        name = row[2]
        rarity = row[3]
        storeCategory = row[4]
        vBucks = int(row[5])
        data.append({header[0]: imageUrl, header[1]: manifestId, header[2]: name, header[3]: rarity, header[4]: storeCategory, header[5]: vBucks})

    return data, True

def save_store(store):
	with open('./store.csv', 'w') as store_file:
		fields = ['imageUrl', 'manifestId', 'name', 'rarity', 'storeCategory', 'vBucks']
		writer = csv.DictWriter(store_file, fieldnames=fields)
		writer.writeheader()
		writer.writerows(store)
		store_file.close()

def compare_store(api_store, saved_store):
	for item in api_store:
		if item not in saved_store:
			return False

	return True

def correct_rarities(item):
	if item['name'] == "Dark Glyph" or item['name'] == "Dark Bomber" or item['name'] == "Thunder Crash" or item["name"] == "Dark Tricera Ops" or item['name'] == "Dark Rex" or item['name'] == "Dark Dino Bones":
		return "Dark Series"
	
	marval_x_force = ["Unstoppable Force", "Domino", "Cable", "Psi-blade", "Probability Dagger", "Psylocke", "Psi-Rider"]
	
	star_wars = ["Vibro-scythe", "Sith Trooper", "Rey", "Dark Side", "Rey's Quarterstaff", "Kylo Ren", "First Order Tie Fighter", "Riot Control Baton", "Resistance Thumbs Up", "Y-Wing", "Traitor!"]
	
	if item['name'] == "Marshmello":
		return "Icon Series"

	if item['rarity'] == "Handmade" or item["rarity"] == "uncommon":
		return "Uncommon"
	elif item['rarity'] == "starwars" or item['name'] in star_wars:
		return "Star Wars Series"
	elif item['rarity'] == 'marvel' or item['name'] in marval_x_force:
		return "Marvel Series"
	elif item['rarity'] == "Sturdy" or item["rarity"] == "rare":
		return "Rare"
	elif item['rarity'] == "Quality" or item['rarity'] == "epic":
		return "Epic"
	elif item['rarity'] == "Fine" or item['rarity'] == "legendary":
		return "Legendary"
	elif item['rarity'] == "dark":
		return "Dark Series"
	elif item['rarity'] == "shadow":
		return "Shadow Series"
	else:
		return item['rarity']

# Corrects names for items that were not hotfixed
def correct_names(name):
	if name == "Set_05_AA":
		return "Full Tilt"
	elif name == "Set_02_BA":
		return "Traveler Bundle"
	elif name == "Set_02_AA":
		return "Team Space"
	elif name == "Set_03_FA":
		return "Putrid Playmaker"
	elif name == "Set_03_GA":
		return "Fatal Finisher"
	elif name == "Set_03_EA":
		return "Decaying Dribbler"
	elif name == "Set_03_HA":
		return "Crypt Crosser"
	elif name == "Set_03_DA":
		return "Soulless Sweeper"
	elif name == "Set_03_BA":
		return "Midfield Monstrosity"
	elif name == "Set_03_CA":
		return "Burial Threat"
	elif name == "Set_03_AA":
		return "Sinister Striker"
	else:
		return name

# Correction for Zombie soccer skins
def correct_price(item):
	item_names = ["Set_03_AA", "Set_03_CA", "Set_03_BA", "Set_03_DA", "Set_03_HA", "Set_03_EA", "Set_03_GA", "Set_03_FA"]
	if item['name'] in item_names:
		return 1200
	elif item['name'] == "Dragacorn" or item['name'] == "Ravenpool" or item['name'] == "Psylocke":
		return 1500
	else:
		return item['vBucks']

# Sets the color for the item shop item
def set_rarity_color(item):
	rarity = correct_rarities(item)

	if rarity == "Dark Series":
		return Colour.dark_purple()
	if rarity in ["starwars", "Star Wars Series"]:
		return Colour.from_rgb(255, 255, 0)
	elif rarity == "marvel" or rarity == "Marvel Series":
		return Colour.red()
	elif rarity == "Icon Series":
		return Colour.teal()
	elif rarity == "Uncommon":
		return Colour.green()
	elif rarity == "Rare":
		return Colour.blue()
	elif rarity == "Epic":
		return Colour.purple()
	elif rarity == "Legendary":
		return Colour.gold()
	else:
		return Colour.light_grey()