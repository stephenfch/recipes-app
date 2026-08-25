#!/usr/bin/env python3
"""Add English names to all 247 recipes and update UI for trilingual display."""
import re
import json

# English names for recipes 1-155 (from task description)
EN_NAMES_1_155 = {
    1: "Steamed Pork Ribs with Garlic",
    2: "Kyoto-style Sweet and Sour Spare Ribs",
    3: "Braised Beef Brisket with Tomato and Potato",
    4: "Honey Glazed Char Siu (BBQ Pork)",
    5: "Bitter Melon Stir-fried with Beef",
    6: "Chicken Wings Braised in Chu Hou Paste",
    7: "Black Pepper Beef Tenderloin",
    8: "Korean Gochujang Grilled Pork Neck",
    9: "Lemongrass Coconut Curry Chicken",
    10: "Steamed Grass Carp with Black Bean Sauce",
    11: "Steamed Prawns with Garlic",
    12: "Fried Dace with Black Bean Sauce and Lettuce",
    13: "Ginger Scallion Stir-fried Crab",
    14: "XO Sauce Stir-fried Shrimp",
    15: "Mirin Pan-fried Salmon",
    16: "Steamed Fish with Preserved Lemon",
    17: "Oyster Sauce Lettuce",
    18: "Garlic Stir-fried Chinese Broccoli",
    19: "Dried Shrimp Stir-fried Cabbage",
    20: "Cold Cucumber Salad",
    21: "Wood Ear Mushroom with Celery and Lily Bulb",
    22: "Water Spinach with Chili and Fermented Tofu",
    23: "Hairy Melon and Clam Soup",
    24: "Winter Melon and Barley Soup",
    25: "Tomato and Potato Soup",
    26: "Seaweed and Egg Drop Soup",
    27: "Black-eyed Pea, Peanut and Pork Bone Soup",
    28: "Singapore Fried Vermicelli",
    29: "Yangzhou Fried Rice",
    30: "Soy Sauce Fried Noodles",
    31: "Chinese Sausage Clay Pot Rice",
    32: "Beef Brisket Noodle Soup",
    33: "Tomato and Egg Stir-fry",
    34: "Bitter Melon and Egg Stir-fry",
    35: "Homestyle Tofu",
    36: "Steamed Egg Custard",
    37: "Mapo Tofu",
    38: "Steamed Grass Carp with Ginger and Scallion",
    39: "Steamed Minced Pork with Salted Egg",
    40: "Soy Sauce Braised Chicken Thigh",
    41: "Dry-Fried Green Beans",
    42: "Dried Vegetable, North-south Almond Pork Bone Soup",
    43: "Chu Hou Paste Braised Beef Short Ribs with Potato",
    44: "Pan-fried Beef and Shredded Potato Pancake",
    45: "Thai-style Grilled Pork Neck",
    46: "Creamy Tomato Prawn Spaghetti",
    47: "Cheese Baked Broccoli",
    48: "Korean Bibimbap",
    49: "Salted Egg Yolk Chicken Wings",
    50: "Yuzu Honey Chicken Wings",
    51: "Red Date Fish Maw Steamed Milk",
    52: "Chicken and Egg Rice Bowl (Oyakodon)",
    53: "Garlic Beef Dice Rice Bowl",
    54: "Tomato Braised Pork Soft Bone",
    55: "Steamed Egg with Conpoy (Dried Scallop)",
    56: "Pan-fried Corn Chicken Patty",
    57: "Pan-fried Lotus Root and Pork Patty",
    58: "Stuffed Eggplant (Dragon Style)",
    59: "Mouth-watering Chicken Wings (Sichuan Style)",
    60: "Spaghetti Carbonara",
    61: "Easy Rice Cooker Black Pepper Tomato Beef Rice",
    62: "String Bean, Potato Braised Spare Ribs",
    63: "Fermented Tofu Carbonara",
    64: "Olive Meat Minced Fried Rice",
    65: "Thai-style Salmon Steak",
    66: "Ginger Scallion Cooked Oysters",
    67: "Enoki Mushroom Pork Roll",
    68: "Conpoy and Pork Bone Congee",
    69: "Cold Sesame Okra and Tofu",
    70: "Garlic Cheese Herb Potato Wedges",
    71: "Cordyceps Flower, Chicken Feet and Conch Soup",
    72: "Corn, Chestnut and Lean Pork Soup",
    73: "Sichuan Peppercorn Shrimp",
    74: "Steamed Baby Abalone with Dried Tangerine Peel",
    75: "Cordyceps Fish Maw and Conch Soup",
    76: "Scallion Oil Pork Chop",
    77: "Cold Spicy Cat Ear Mushroom and Cucumber",
    78: "Triangle Rice Ball (Onigiri)",
    79: "Tofu, Water Chestnut and Minced Pork Patty",
    80: "Double Snow Fungus, Peach Resin and Papaya Dessert",
    81: "Apple and Hawthorn Chicken Wings",
    82: "Pumpkin, Lily Bulb and Lean Pork Congee",
    83: "Chinese Sausage Stir-fried Vegetables",
    84: "Ginger Pork Yakiniku (Shogayaki)",
    85: "Dried Vegetable, Dried Oyster and Carrot Soup",
    86: "Japanese Black Sesame Vegetable Rice Ball",
    87: "Broccoli Stir-fried Beef",
    88: "Red Bean, Winter Melon and Lotus Root Spare Rib Soup",
    89: "Korean Beef Kimbap",
    90: "Korean Beef Rice Bowl",
    91: "Salmon and Seaweed Miso Soup",
    92: "Fresh Tomato Salmon Farfalle Salad",
    93: "No-oven Peach Tomato Pork Chop Rice",
    94: "Red Date, Huai Shan, Lily Bulb and Goji Chicken Soup",
    95: "Mushroom Spinach White Sauce Pasta",
    96: "Pumpkin Lily Bulb Millet Congee",
    97: "Fresh Chinese Yam Stir-fried with Lean Pork",
    98: "Osmanthus Peach Resin Triple White Dessert",
    99: "Hericium Mushroom, Papaya, Peanut and Sea Coconut Spare Rib Soup",
    100: "Tomato Sauce Prawns",
    101: "Chestnut and Red Date Braised Chicken Wings",
    102: "Night-blooming Cereus, Fig, Pear, Carrot and Lean Pork Soup",
    103: "Vegetable Fried Instant Noodles",
    104: "Chili Fermented Tofu Chinese Broccoli and Fresh Squid",
    105: "Japanese Pork Floss Rice Ball",
    106: "Korean Kimchi Salmon Flaked Fried Rice",
    107: "Japanese Beef Rice Bowl (Gyudon)",
    108: "Multigrain Chicken and Chinese Sausage Clay Pot Rice",
    109: "Kimchi Tofu Pot",
    110: "Taiwanese Braised Pork Rice with Quinoa Vegetable Rice",
    111: "Lemon and Job's Tears Water",
    112: "Potato Braised Chicken Wings",
    113: "Soy Sauce Chicken Wings",
    114: "Hairy Melon, Dried Octopus and Chicken Feet Soup",
    115: "Tomato Tofu Fresh Fish Soup",
    116: "Sweet and Sour Onion Pork Chop",
    117: "Tomato Sauce Pan-fried Prawns",
    118: "Japanese Teriyaki Chicken",
    119: "Bitter Melon, Black-eyed Pea and Spare Rib Soup",
    120: "Sesame Shredded Chicken",
    121: "Bitter Melon, Soybean, Fig and Pork Bone Soup",
    122: "Garlic Olive Oil Spaghetti (Aglio e Olio)",
    123: "Sea Coconut Corn and Carrot Soup",
    124: "Fermented Tofu Steamed Chicken",
    125: "Fresh Chinese Yam and Lotus Seed Spare Rib Soup",
    126: "Conpoy and Chicken Congee",
    127: "Lily Bud and Wood Ear Steamed Spare Ribs",
    128: "Shiitake Mushroom Steamed Minced Pork",
    129: "White Radish Braised Chicken Wings",
    130: "Fresh Tomato Braised Chicken",
    131: "Seaweed Tofu Meatball Soup",
    132: "Century Egg and Lean Pork Congee",
    133: "Minced Pork Steamed Egg",
    134: "Conpoy and Enoki Mushroom Spinach",
    135: "Swiss Chicken Wings (HK Style Sweet Soy)",
    136: "Korean Spicy Pork Rice Bowl",
    137: "Mustard Green Pork Slice Tofu Soup",
    138: "Simple Pan-fried Salmon",
    139: "Cashew and Asparagus Stir-fried Chicken",
    140: "Healthy Napa Cabbage Tofu Soup",
    141: "Chinese Mini Egg Omelette with Minced Pork",
    142: "Steamed Grass Carp Belly with Preserved Mustard",
    143: "Smooth Tomato Egg Macaroni",
    144: "Wasabi Shredded Chicken Sheet Noodles",
    145: "Korean Kimchi Fried Rice",
    146: "Coconut Curry Braised Chicken",
    147: "Cheese Avocado Baked Tortilla",
    148: "Cucumber Stir-fried Chicken",
    149: "Shiitake Mushroom Braised Spare Ribs",
    150: "Plum Sauce Steamed Spare Ribs",
    151: "Lotus Root Braised Spare Ribs",
    152: "Kimchi Pork Congee",
    153: "Soy Sauce Chicken (Light Soy Version)",
    154: "Farm-style Stir-fried Pork",
    155: "Dongpo Eggplant",
}

# English names for recipes 156-247 (new classic HK dishes)
EN_NAMES_156_247 = {
    156: "Red Fermented Tofu Braised Pork Knuckle",
    157: "Sweet and Sour Pork",
    158: "Steamed Pork Belly with Preserved Vegetables",
    159: "Sweet and Sour Spare Ribs",
    160: "Steamed Minced Pork Patty",
    161: "Stir-fried Pork Liver with Eggs",
    162: "Pork Knuckle Stewed with Ginger",
    163: "Spare Ribs with Fermented Tofu",
    164: "Braised Pork Knuckle in Red Fermented Tofu",
    165: "Braised Pig's Ear",
    166: "Stuffed Pork Stomach with Chicken",
    167: "Stir-fried Pork Liver with Ginger and Scallion",
    168: "Salt Baked Pork Knuckle",
    169: "Stir-fried Pig Blood with Chives",
    170: "Char Siu Fried Rice",
    171: "Ginger and Scallion Beef",
    172: "Beef with Black Bean Sauce and Chili",
    173: "Dry Fried Beef Rice Noodles",
    174: "Satay Beef with Enoki Mushroom in Clay Pot",
    175: "Stir-fried Beef with Celery",
    176: "Beef in Oyster Sauce",
    177: "Pan-fried Salted Beef Tenderloin",
    178: "Steamed Beef Balls",
    179: "Satay Beef",
    180: "Ginger Juice Beef",
    181: "White Cut Chicken",
    182: "Salt Baked Chicken",
    183: "Scallion Oil Chicken",
    184: "Drunken Chicken",
    185: "BBQ Sauce Chicken Wings",
    186: "Lotus Leaf Rice",
    187: "Salt Baked Pigeon",
    188: "Soy Sauce Chicken",
    189: "Steamed Chicken with Fermented Tofu",
    190: "Steamed Egg with Silky Chicken",
    191: "Steamed Fish",
    192: "Ginger Scallion Baked Crab",
    193: "Blanched Prawns",
    194: "Oyster Omelette",
    195: "Salt and Pepper Squid",
    196: "Stir-fried Clams with Black Bean Sauce",
    197: "Garlic Butter Butterfly Prawns",
    198: "Sweet and Sour Fish",
    199: "Ginger Scallion Baked Fish",
    200: "Stir-fried Mussels in Black Bean Sauce",
    201: "Garlic Stir-fried Choy Sum",
    202: "Salted Edamame",
    203: "Water Spinach with Fermented Tofu",
    204: "Fish-fragrant Eggplant Clay Pot",
    205: "Stir-fried Water Spinach with Shrimp Paste",
    206: "Salt Baked Green Beans",
    207: "Stir-fried Choy Sum",
    208: "Poached Choy Sum in Salt Water",
    209: "Garlic Stir-fried Seasonal Vegetables",
    210: "Salt Baked Potatoes",
    211: "Night-blooming Cereus and Pork Bone Soup",
    212: "Dried Vegetable and Almond Pork Bone Soup",
    213: "Kudzu Root and Red Bean Soup",
    214: "Pork Liver Soup with Spinach",
    215: "Pork Stomach Chicken Soup",
    216: "Poached Fish in Oil and Salt Water",
    217: "Kudzu Root and Dace Soup",
    218: "Watercress Pork Bone Soup",
    219: "Hairy Melon, Octopus and Chicken Feet Soup",
    220: "Lotus Root Pork Bone Soup",
    221: "Pig Blood Congee",
    222: "Scholar's Congee (Assorted Offal)",
    223: "Fresh Fish Slice Congee",
    224: "Chicken Congee",
    225: "Teochew Style Congee",
    226: "Crispy Sweet and Sour Spare Ribs",
    227: "Garlic Spare Ribs",
    228: "Soy Sauce Fried Noodles",
    229: "Dry Fried Beef Flat Rice Noodles",
    230: "Singapore Fried Vermicelli",
    231: "Salt Baked Eggs",
    232: "Salt Baked Tofu",
    233: "Scrambled Eggs",
    234: "Pan-fried Eggs",
    235: "Steamed Egg Custard",
    236: "Triangle Rice Ball (Onigiri)",
    237: "Japanese Pork Floss Rice Ball",
    238: "Japanese Black Sesame Vegetable Rice Ball",
    239: "Creamy Tomato Prawn Spaghetti",
    240: "Spaghetti Carbonara",
    241: "Fermented Tofu Carbonara",
    242: "Garlic Olive Oil Spaghetti (Aglio e Olio)",
    243: "Smooth Tomato Egg Macaroni",
    244: "Snow Fungus, Peach Resin and Papaya Dessert",
    245: "Red Date Fish Maw Steamed Milk",
    246: "Osmanthus Peach Resin Triple White Dessert",
    247: "Lemon and Job's Tears Water",
}

# Merge all English names
ALL_EN_NAMES = dict(list(EN_NAMES_1_155.items()) + list(EN_NAMES_156_247.items()))

def main():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # === STEP 1: Parse and add "en" field to RECIPES ===
    match = re.search(r'const RECIPES = (\[.*?\]);', content)
    if not match:
        print("ERROR: Could not find RECIPES array")
        return

    recipes = json.loads(match.group(1))
    print(f"Found {len(recipes)} recipes")

    # Add "en" field to each recipe
    missing = []
    for r in recipes:
        rid = r['id']
        if rid in ALL_EN_NAMES:
            r['en'] = ALL_EN_NAMES[rid]
        else:
            r['en'] = r['fil']
            missing.append(rid)

    if missing:
        print(f"WARNING: Missing English names for IDs: {missing}")
    else:
        print("All 247 recipes have English names")

    # Verify all have 'en'
    for r in recipes:
        assert 'en' in r, f"Recipe {r['id']} missing 'en' field"

    # Write back the RECIPES array
    recipes_json = json.dumps(recipes, ensure_ascii=False, separators=(',', ': '))
    old_recipes_str = match.group(0)
    new_recipes_str = "const RECIPES = " + recipes_json + ";"
    content = content.replace(old_recipes_str, new_recipes_str)

    # === STEP 2: Add CSS for card-en and language toggle ===
    card_en_css = (
        ".card-en {\n"
        "  font-size: 0.72rem;\n"
        "  color: #888;\n"
        "  line-height: 1.3;\n"
        "  margin-bottom: 8px;\n"
        "  display: -webkit-box;\n"
        "  -webkit-line-clamp: 2;\n"
        "  -webkit-box-orient: vertical;\n"
        "  overflow: hidden;\n"
        "  font-style: italic;\n"
        "}\n"
        "/* Language toggle */\n"
        ".lang-toggle {\n"
        "  display: flex;\n"
        "  gap: 4px;\n"
        "  padding: 8px 16px;\n"
        "  max-width: 800px;\n"
        "  margin: 0 auto;\n"
        "}\n"
        ".lang-btn {\n"
        "  flex: 1;\n"
        "  padding: 6px 8px;\n"
        "  border: 1.5px solid var(--border);\n"
        "  border-radius: 20px;\n"
        "  background: white;\n"
        "  font-size: 0.75rem;\n"
        "  font-family: inherit;\n"
        "  cursor: pointer;\n"
        "  transition: all 0.2s;\n"
        "  text-align: center;\n"
        "  font-weight: 500;\n"
        "  color: var(--text);\n"
        "  white-space: nowrap;\n"
        "}\n"
        ".lang-btn:hover { border-color: #ccc; background: #f8f8f8; }\n"
        ".lang-btn.active {\n"
        "  background: var(--accent);\n"
        "  color: white;\n"
        "  border-color: var(--accent);\n"
        "}\n"
        ".modal-title .en-subtitle {\n"
        "  font-size: 0.8rem;\n"
        "  color: #888;\n"
        "  font-style: italic;\n"
        "  margin-top: 2px;\n"
        "}\n"
    )

    # Insert before closing </style>
    content = content.replace('</style>', card_en_css + '</style>')

    # === STEP 3: Add language toggle HTML ===
    lang_toggle_html = (
        '<div class="lang-toggle">\n'
        '  <button class="lang-btn active" onclick="setLangMode(\'zhfil\', this)">中+菲</button>\n'
        '  <button class="lang-btn" onclick="setLangMode(\'zhen\', this)">中+英</button>\n'
        '  <button class="lang-btn" onclick="setLangMode(\'all\', this)">中+英+菲</button>\n'
        '</div>\n'
    )
    content = content.replace(
        '<div class="filters">',
        lang_toggle_html + '<div class="filters">'
    )

    # === STEP 4: Update JS ===
    # Add langMode variable
    content = content.replace(
        "let currentSearch = '';",
        "let currentSearch = '';\nlet currentLangMode = 'zhfil';"
    )

    # Add setLangMode function before setCategory
    lang_func = (
        "function setLangMode(mode, btn) {\n"
        "  currentLangMode = mode;\n"
        "  document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('active'));\n"
        "  btn.classList.add('active');\n"
        "  renderRecipes();\n"
        "}\n\n"
    )
    content = content.replace(
        'function setCategory(cat, btn) {',
        lang_func + 'function setCategory(cat, btn) {'
    )

    # Update renderRecipes card body to show English
    old_card_zh = '<div class="card-zh">${escHtml(r.zh)}</div>'
    old_card_fil = '<div class="card-fil">${escHtml(r.fil)}</div>'

    new_card_zh = (
        '<div class="card-zh">${escHtml(r.zh)}</div>\n'
        "          ${currentLangMode !== 'zhfil' ? " + "`<div class=\"card-en\">${escHtml(r.en || r.fil)}</div>` : ''}\n"
        "          ${(currentLangMode === 'all') ? " + "`<div class=\"card-fil\">${escHtml(r.fil)}</div>` : ''}\n"
        "          ${currentLangMode === 'zhfil' ? " + "`<div class=\"card-fil\">${escHtml(r.fil)}</div>` : ''}"
    )

    content = content.replace(
        old_card_zh + "\n          " + old_card_fil,
        new_card_zh
    )

    # Update openRecipeModal to show English name
    old_modal_title = "document.getElementById('modalTitle').textContent = r.zh;\n  document.getElementById('modalSubtitle').textContent = r.fil;"
    new_modal_title = (
        "document.getElementById('modalTitle').textContent = r.zh;\n"
        "  const subtitleEl = document.getElementById('modalSubtitle');\n"
        "  if (currentLangMode === 'zhfil') {\n"
        "    subtitleEl.innerHTML = escHtml(" + "r.fil);\n"
        "  } else if (currentLangMode === 'zhen') {\n"
        "    subtitleEl.innerHTML = escHtml(" + "r.en || " + "r.fil);\n"
        "  } else {\n"
        "    subtitleEl.innerHTML = " + "`<span style=\"font-weight:500\">${escHtml(" + "r.en || " + "r.fil)}</span> \u00b7 ${escHtml(" + "r.fil)}`;\n"
        "  }"
    )

    content = content.replace(old_modal_title, new_modal_title)

    # === STEP 5: Update header subtitle ===
    content = content.replace(
        '<p>155 道家常菜 · Lutong Bahay ng Hong Kong</p>',
        '<p>247 道家常菜 · 247 Home-style Recipes · Lutong Bahay ng Hong Kong</p>'
    )

    # Write the updated file
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\nDone! Updated index.html with {len(recipes)} recipes, all with English names")
    print(f"  CSS: added .card-en and .lang-toggle styles")
    print(f"  HTML: added language toggle buttons")
    print(f"  JS: added langMode state, setLangMode function, trilingual rendering")

if __name__ == '__main__':
    main()
