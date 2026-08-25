#!/usr/bin/env python3
"""Extract Chinese ingredients and steps from the HTML file."""
import json, re

HTML_PATH = '/opt/data/workspace/projects/recipes-app/index.html'

with open(HTML_PATH, 'r') as f:
    content = f.read()

match = re.search(r'const RECIPES = (\[.*?\]);', content, re.DOTALL)
recipes = json.loads(match.group(1))
print(f"Total recipes: {len(recipes)}")

# Find the specific ingredients block between 'const specific = {' and the closing '};'
ing_start = content.find("const specific = {\n    '蒜蓉蒸排骨':")
if ing_start == -1:
    ing_start = content.find("const specific = {\n")
ing_block = content[ing_start:ing_start+20000]
# Find the closing };
ing_end = ing_block.find("\n};")
ing_block = ing_block[:ing_end+3]
print(f"Inging block length: {len(ing_block)}")

zh_ing = {}
for m in re.finditer(r"    '(.+?)': \[(.+?)\],?\n", ing_block):
    key = m.group(1)
    vals = [v.strip() for v in re.findall(r"'(.+?)'", m.group(2))]
    zh_ing[key] = vals

print(f"ZH ingredients: {len(zh_ing)}")

# Steps block
stp_start = content.find("const specific = {\n    '蒜蓉蒸排骨': ['豬排骨洗淨")
if stp_start == -1:
    stp_start = content.find("function generateSteps")
    stp_start = content.find("const specific = {", stp_start)
stp_block = content[stp_start:stp_start+30000]
stp_end = stp_block.find("\n  };")
stp_block = stp_block[:stp_end+4]
print(f"Steps block length: {len(stp_block)}")

zh_stp = {}
for m in re.finditer(r"    '(.+?)': \[(.+?)\],?\n", stp_block):
    key = m.group(1)
    vals = [v.strip() for v in re.findall(r"'(.+?)'", m.group(2))]
    zh_stp[key] = vals

print(f"ZH steps: {len(zh_stp)}")

# Save for later use
with open('/opt/data/workspace/zh_ing.json', 'w') as f:
    json.dump(zh_ing, f, ensure_ascii=False)
with open('/opt/data/workspace/zh_stp.json', 'w') as f:
    json.dump(zh_stp, f, ensure_ascii=False)

# Print all recipe names that DON'T have specific ingredients
recipe_names = [r['zh'] for r in recipes]
missing_ing = [n for n in recipe_names if n not in zh_ing]
missing_stp = [n for n in recipe_names if n not in zh_stp]
print(f"\nRecipes missing specific ingredients: {len(missing_ing)}")
print(f"Recipes missing specific steps: {len(missing_stp)}")
print("\nFirst 10 missing ingredients:", missing_ing[:10])
print("First 10 missing steps:", missing_stp[:10])
