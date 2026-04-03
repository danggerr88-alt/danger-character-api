from flask import Flask, jsonify, send_file
import os

app = Flask(__name__)

# Character ID to image filename mapping
character_map = {
    "806": "102000008.png",    # Kla
    "306": "102000006.png",    # Ford
    "906": "101000009.png",    # Paloma
    "2406": "101000016.png",   # Notora
    "1003": "102000009.png",   # Miguel
    "2306": "102000016.png",   # Alvaro
    "6306": "102000042.png",   # Awaken Alvaro
    "7506": "101000053.png",   # Rin
    "1306": "102000010.png",   # Antonio
    "2006": "102000014.png",   # Joseph
    "2106": "101000014.png",   # Shani
    "2806": "101100018.png",   # Kapella
    "7206": "102000051.png",   # Koda
    "7006": "101000049.png",   # Kassie
    "6906": "102000046.png",   # Kairos
    "6806": "102000045.png",   # Ryden
    "6706": "102000044.png",   # Ignis
    "6606": "101000028.png",   # Suzy
    "6506": "101000027.png",   # Sonia
    "6206": "102000041.png",   # Orion
    "6006": "102000040.png",   # Santino
    "5306": "101000026.png",   # Luna
    "5806": "102000039.png",   # Tatsuya
    "5606": "101000025.png",   # Iris
    "5706": "103000003.png",   # J.Biebs's Microchip
    "5506": "102000037.png",   # Homer
    "5406": "102000036.png",   # Kenta
    "5206": "102000034.png",   # Nairi
    "5006": "102000033.png",   # Otho
    "4906": "102000032.png",   # Leon
    "4606": "102000030.png",   # Thiva
    "4706": "102000031.png",   # Dimitri
    "4506": "102000029.png",   # D-bee
    "4306": "102000028.png",   # Maro
    "4006": "102000025.png",   # Skyler
    "4406": "101000022.png",   # Xayne
    "4106": "102000026.png",   # Shirou
    "3806": "103000004.png",   # Chrono's Microchip
    "3506": "101000020.png",   # Dasha
    "3406": "102000022.png",   # K
    "2906": "102000018.png",   # Luqueta
    "206": "101000006.png",    # Kelly
    "1506": "102000012.png",   # Hayato Yagami
    "1406": "101000011.png",   # Moco
    "2606": "101000017.png",   # Steffie
    "606": "101000008.png",    # Misha
    "706": "102000007.png",    # Maxim
    "406": "102000005.png",    # Andrew
    "7106": "101000050.png",   # Lila
    "1106": "101000010.png",   # Caroline
    "1706": "101000012.png",   # Laura
    "1806": "102000013.png",   # Rafael
    "2206": "102000015.png",   # Alok
    "2706": "102000017.png",   # Jota
    "3106": "101000019.png",   # Clu
    "3006": "102200019.png",   # Wolfrahh
    "3306": "103000002.png",   # Jai's Microchip
    "4203": "102000027.png",   # Awaken Andrew
    "4806": "101000023.png",   # Awaken Moco
    "3203": "102000020.png",   # Awaken Hayato
    "2506": "101000015.png",   # Awaken Kelly
    "22016": "102000043.png",  # Awaken Alok
    "506": "101000007.png",    # Nikita
    "1906": "101000013.png",   # A124
    "7406": "102000052.png",   # Oscar
    "1206": "102000011.png",   # Wukong
    "106": "101000005.png",    # Olivia
    "7706": "102000055.png",   # Morse
    "7606": "102000054.png",   # Nero
}

# Character ID to display name
character_names = {
    "806": "Kla",
    "306": "Ford",
    "906": "Paloma",
    "2406": "Notora",
    "1003": "Miguel",
    "2306": "Alvaro",
    "6306": "Awaken Alvaro",
    "7506": "Rin",
    "1306": "Antonio",
    "2006": "Joseph",
    "2106": "Shani",
    "2806": "Kapella",
    "7206": "Koda",
    "7006": "Kassie",
    "6906": "Kairos",
    "6806": "Ryden",
    "6706": "Ignis",
    "6606": "Suzy",
    "6506": "Sonia",
    "6206": "Orion",
    "6006": "Santino",
    "5306": "Luna",
    "5806": "Tatsuya",
    "5606": "Iris",
    "5706": "J.Biebs's Microchip",
    "5506": "Homer",
    "5406": "Kenta",
    "5206": "Nairi",
    "5006": "Otho",
    "4906": "Leon",
    "4606": "Thiva",
    "4706": "Dimitri",
    "4506": "D-bee",
    "4306": "Maro",
    "4006": "Skyler",
    "4406": "Xayne",
    "4106": "Shirou",
    "3806": "Chrono's Microchip",
    "3506": "Dasha",
    "3406": "K",
    "2906": "Luqueta",
    "206": "Kelly",
    "1506": "Hayato Yagami",
    "1406": "Moco",
    "2606": "Steffie",
    "606": "Misha",
    "706": "Maxim",
    "406": "Andrew",
    "7106": "Lila",
    "1106": "Caroline",
    "1706": "Laura",
    "1806": "Rafael",
    "2206": "Alok",
    "2706": "Jota",
    "3106": "Clu",
    "3006": "Wolfrahh",
    "3306": "Jai's Microchip",
    "4203": "Awaken Andrew",
    "4806": "Awaken Moco",
    "3203": "Awaken Hayato",
    "2506": "Awaken Kelly",
    "22016": "Awaken Alok",
    "506": "Nikita",
    "1906": "A124",
    "7406": "Oscar",
    "1206": "Wukong",
    "106": "Olivia",
    "7706": "Morse",
    "7606": "Nero",
}

# Reverse mapping: PNG basename (e.g., "102000015") -> display name (e.g., "Alok")
png_basename_to_display = {}
for char_id, filename in character_map.items():
    basename = filename[:-4]  # remove ".png"
    if char_id in character_names:
        png_basename_to_display[basename] = character_names[char_id]

# Additional PNGs that are not in character_map (e.g., primis, nulla)
extra_png_names = {
    "102000004": "primis",
    "101000004": "nulla",
}
png_basename_to_display.update(extra_png_names)

# Directory where PNG images are stored
PNG_DIR = os.path.join(os.path.dirname(__file__), "pngs")

@app.route('/')
def hello():
    return jsonify({"message": "Character API is working! Use /api/<id>"})

@app.route('/api/<id>')
def get_character_image(id):
    # Remove .bin extension if present
    if id.endswith('.bin'):
        id = id[:-4]

    filename = None
    display_name = None

    # Case 1: Character ID (like "806") directly in character_map
    if id in character_map:
        filename = character_map[id]
        display_name = character_names.get(id, id)
    # Case 2: PNG basename (like "102000015") found in reverse mapping
    elif id in png_basename_to_display:
        filename = f"{id}.png"
        display_name = png_basename_to_display[id]
    # Case 3: Skill ID (8-11 digits) - generic fallback
    elif 8 <= len(id) <= 11:
        filename = f"{id}.png"
        display_name = f"Skill_{id}"
    else:
        return jsonify({"error": "Invalid ID format or ID not found"}), 404

    image_path = os.path.join(PNG_DIR, filename)
    if not os.path.exists(image_path):
        return jsonify({"error": f"Image file not found: {filename}"}), 404

    # Send file with friendly download name
    try:
        return send_file(
            image_path,
            mimetype='image/png',
            as_attachment=False,
            download_name=f"{display_name}.png"
        )
    except TypeError:
        # Older Flask compatibility
        return send_file(
            image_path,
            mimetype='image/png',
            as_attachment=False,
            attachment_filename=f"{display_name}.png"
        )

# Vercel ke liye
app = app
