from flask import Flask, jsonify, request, Response
import os

app = Flask(__name__)

# ---------- MAPPINGS ----------
character_map = {
    "806": "102000008.png", "306": "102000006.png", "906": "101000009.png",
    "2406": "101000016.png", "1003": "102000009.png", "2306": "102000016.png",
    "6306": "102000042.png", "7506": "101000053.png", "1306": "102000010.png",
    "2006": "102000014.png", "2106": "101000014.png", "2806": "101100018.png",
    "7206": "102000051.png", "7006": "101000049.png", "6906": "102000046.png",
    "6806": "102000045.png", "6706": "102000044.png", "6606": "101000028.png",
    "6506": "101000027.png", "6206": "102000041.png", "6006": "102000040.png",
    "5306": "101000026.png", "5806": "102000039.png", "5606": "101000025.png",
    "5706": "103000003.png", "5506": "102000037.png", "5406": "102000036.png",
    "5206": "102000034.png", "5006": "102000033.png", "4906": "102000032.png",
    "4606": "102000030.png", "4706": "102000031.png", "4506": "102000029.png",
    "4306": "102000028.png", "4006": "102000025.png", "4406": "101000022.png",
    "4106": "102000026.png", "3806": "103000004.png", "3506": "101000020.png",
    "3406": "102000022.png", "2906": "102000018.png", "206": "101000006.png",
    "1506": "102000012.png", "1406": "101000011.png", "2606": "101000017.png",
    "606": "101000008.png", "706": "102000007.png", "406": "102000005.png",
    "7106": "101000050.png", "1106": "101000010.png", "1706": "101000012.png",
    "1806": "102000013.png", "2206": "102000015.png", "2706": "102000017.png",
    "3106": "101000019.png", "3006": "102200019.png", "3306": "103000002.png",
    "4203": "102000027.png", "4806": "101000023.png", "3203": "102000020.png",
    "2506": "101000015.png", "22016": "102000043.png", "506": "101000007.png",
    "1906": "101000013.png", "7406": "102000052.png", "1206": "102000011.png",
    "106": "101000005.png", "7706": "102000055.png", "7606": "102000054.png",
}

character_names = {
    "806": "Kla", "306": "Ford", "906": "Paloma", "2406": "Notora", "1003": "Miguel",
    "2306": "Alvaro", "6306": "Awaken Alvaro", "7506": "Rin", "1306": "Antonio",
    "2006": "Joseph", "2106": "Shani", "2806": "Kapella", "7206": "Koda", "7006": "Kassie",
    "6906": "Kairos", "6806": "Ryden", "6706": "Ignis", "6606": "Suzy", "6506": "Sonia",
    "6206": "Orion", "6006": "Santino", "5306": "Luna", "5806": "Tatsuya", "5606": "Iris",
    "5706": "J.Biebs's Microchip", "5506": "Homer", "5406": "Kenta", "5206": "Nairi",
    "5006": "Otho", "4906": "Leon", "4606": "Thiva", "4706": "Dimitri", "4506": "D-bee",
    "4306": "Maro", "4006": "Skyler", "4406": "Xayne", "4106": "Shirou", "3806": "Chrono's Microchip",
    "3506": "Dasha", "3406": "K", "2906": "Luqueta", "206": "Kelly", "1506": "Hayato Yagami",
    "1406": "Moco", "2606": "Steffie", "606": "Misha", "706": "Maxim", "406": "Andrew",
    "7106": "Lila", "1106": "Caroline", "1706": "Laura", "1806": "Rafael", "2206": "Alok",
    "2706": "Jota", "3106": "Clu", "3006": "Wolfrahh", "3306": "Jai's Microchip",
    "4203": "Awaken Andrew", "4806": "Awaken Moco", "3203": "Awaken Hayato",
    "2506": "Awaken Kelly", "22016": "Awaken Alok", "506": "Nikita", "1906": "A124",
    "7406": "Oscar", "1206": "Wukong", "106": "Olivia", "7706": "Morse", "7606": "Nero",
}

# Extra PNGs (no character ID)
extra_pngs = {
    "102000004": "Primis",
    "101000004": "Nulla",
    "102000056": "Ray"
}
# Add extra to character_names for listing and reverse mapping
for png_base, name in extra_pngs.items():
    character_names[png_base] = name  # treat PNG basename as "ID" for resolution

# Reverse mapping: name (lowercase) -> ID (character ID or PNG basename)
name_to_id = {}
for cid, name in character_names.items():
    name_to_id[name.lower()] = cid

# Also add original character IDs themselves as name? No need.

# PNG directory
PNG_DIR = os.path.join(os.path.dirname(__file__), "..", "pngs")

def resolve_id(raw_id):
    """Given ID (character ID or PNG basename), return (filename, display_name)"""
    if not raw_id:
        return None, None
    # Remove .bin if present
    if raw_id.endswith('.bin'):
        raw_id = raw_id[:-4]
    
    # Case 1: Character ID (e.g., "806")
    if raw_id in character_map:
        filename = character_map[raw_id]
        display = character_names.get(raw_id, raw_id)
        return filename, display
    
    # Case 2: PNG basename (e.g., "102000004") - includes extra PNGs
    if raw_id in extra_pngs or (raw_id in character_map.values()): 
        # Actually character_map values are filenames, not basenames. We need basename without .png.
        # Better: check if raw_id + ".png" exists? Let's just check if raw_id is a key in extra_pngs or matches any PNG basename from character_map
        # Simpler: try to see if file exists directly
        possible_filename = f"{raw_id}.png"
        if os.path.exists(os.path.join(PNG_DIR, possible_filename)):
            display = character_names.get(raw_id, f"Skill_{raw_id}")
            return possible_filename, display
    
    # Case 3: Skill ID (8-11 digits)
    if 8 <= len(raw_id) <= 11:
        filename = f"{raw_id}.png"
        display = f"Skill_{raw_id}"
        return filename, display
    
    return None, None

@app.route('/image')
def get_image():
    char_id = request.args.get('char_id')
    char_name = request.args.get('char_name')
    
    identifier = None
    if char_id:
        identifier = char_id
    elif char_name:
        # Lookup name in name_to_id (case-insensitive)
        identifier = name_to_id.get(char_name.lower())
        if not identifier:
            return jsonify({"error": f"Character name '{char_name}' not found"}), 404
    else:
        return jsonify({"error": "Missing 'char_id' or 'char_name' parameter"}), 400
    
    filename, display_name = resolve_id(identifier)
    if not filename:
        return jsonify({"error": f"Invalid ID: {identifier}"}), 404
    
    image_path = os.path.join(PNG_DIR, filename)
    if not os.path.exists(image_path):
        return jsonify({"error": f"Image file not found: {filename}"}), 404
    
    with open(image_path, 'rb') as f:
        image_data = f.read()
    
    response = Response(image_data, mimetype='image/png')
    response.headers['Content-Disposition'] = f'inline; filename="{display_name}.png"'
    return response

@app.route('/list')
def list_characters():
    # Return sorted list of character names
    names = sorted(character_names.values())
    return jsonify({"characters": names})

@app.route('/')
def home():
    return jsonify({
        "message": "Character Image API",
        "endpoints": {
            "/image?char_id=<id>": "Get image by character ID (e.g., 806, 102000004)",
            "/image?char_name=<name>": "Get image by character name (e.g., Alok, primis)",
            "/list": "Get list of all character names"
        }
    })

app = app
