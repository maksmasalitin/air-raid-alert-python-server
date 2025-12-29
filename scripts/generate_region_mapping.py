import re
import json
import subprocess
import os
import sys

# Add parent directory to path to allow importing config and app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models.air_raid_alert_message_parser import AirRaidAlertMessageParser

# Load existing region map
EXISTING_MAP = AirRaidAlertMessageParser.REGION_MAP
KEYWORDS_DIR = 'regions_keywords'

def normalize_oblast_name(name):
    """Converts 'Name Oblast' to 'Name_Oblast' to match keys."""
    # Also handle some common variations if needed
    return name.replace(' ', '_')

def ensure_dir():
    if not os.path.exists(KEYWORDS_DIR):
        os.makedirs(KEYWORDS_DIR)

def load_region_file(region_id):
    filepath = os.path.join(KEYWORDS_DIR, f"{region_id}.yaml")
    if not os.path.exists(filepath):
        return None
    
    data = {'keywords': []}
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    # Simple parser for the requested format
    for line in lines:
        line = line.strip()
        if line.startswith('name:'):
            data['name'] = line.split('name:', 1)[1].strip()
        elif line.startswith('id:'):
            try:
                data['id'] = int(line.split('id:', 1)[1].strip())
            except ValueError:
                pass
        elif line.startswith('-'):
            # It's a list item (keyword)
            keyword = line.lstrip('- ').strip().strip('"\'')
            if keyword:
                data['keywords'].append(keyword)
    return data

def save_region_file(region_id, region_name, keywords):
    filepath = os.path.join(KEYWORDS_DIR, f"{region_id}.yaml")
    
    # Load existing to merge keywords (if file exists but we passed a partial list)
    # Actually, the caller should pass the FULL list or we handle merging here.
    # Let's handle merging here.
    existing = load_region_file(region_id)
    final_keywords = set(keywords)
    if existing:
        final_keywords.update(existing['keywords'])
        # Keep existing name if present, though we expect consistency
        if not region_name and 'name' in existing:
            region_name = existing['name']

    sorted_keywords = sorted(list(final_keywords))
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"name: {region_name}\n")
        f.write(f"id: {region_id}\n")
        f.write("keywords:\n")
        for k in sorted_keywords:
            f.write(f"  - \"{k}\"\n")

def get_oblast_from_vibe(message_text):
    prompt = (
        "Скажи мені в якій це облаті? Дай відповідь у raw json форматі "
        "{<назва_області>: [<назва району 1>, <назва району 2>, ...]}  "
        f"Інформаційне повідомлення: {message_text}"
        "Список областей: ['Вінницька_область','Волинська_область','Дніпропетровська_область','Донецька_область','Житомирська_область','Закарпатська_область','Запорізька_область','ІваноФранківська_область','Київська_область','Кіровоградська_область','Луганська_область','Львівська_область','Миколаївська_область','Одеська_область','Полтавська_область','Рівненська_область','Сумська_область','Тернопільська_область','Харківська_область','Херсонська_область','Хмельницька_область','Черкаська_область','Чернівецька_область','Чернігівська_область']"
    )
    
    try:
        # Use --max-turns 1 or --max-tokens to limit cost if possible, 
        # but -p usually does 1 turn.
        result = subprocess.run(
            ['vibe', '-p', prompt],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout.strip()
        
        # Clean markdown
        if "```json" in output:
            output = output.split("```json")[1].split("```")[0].strip()
        elif "```" in output:
             output = output.split("```")[1].split("```")[0].strip()
            
        return json.loads(output)
    except Exception as e:
        # print(f"  Vibe error: {e}")
        # Sometimes Vibe might fail or return bad JSON.
        return None

def main():
    ensure_dir()
    print("Reading messages.log...")
    try:
        with open('messages.log', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("messages.log not found.")
        return

    raw_messages = content.split('------------------------------')
    hashtag_pattern = re.compile(r'#(\w+)')
    
    # Cache of hashtags we have already assigned to a region
    # to avoid re-querying Vibe for the same tags.
    # We load existing YAMLs first to populate this cache.
    global_mapped_hashtags = set()
    
    # Pre-load existing work
    for region_name, rid in EXISTING_MAP.items():
        data = load_region_file(rid)
        if data:
            for k in data['keywords']:
                # The file stores "#Tag", let's normalize
                global_mapped_hashtags.add(k)
    
    print(f"Loaded {len(global_mapped_hashtags)} existing mapped keywords.")

    count = 0
    total = len(raw_messages)

    for msg in raw_messages:
        count += 1
        msg = msg.strip()
        if not msg:
            continue
            
        found_tags = hashtag_pattern.findall(msg)
        if not found_tags:
            continue
            
        # Add hash prefix
        current_tags_set = {f"#{t}" for t in found_tags}
        
        # Find which tags are NEW
        new_tags = current_tags_set - global_mapped_hashtags
        
        if not new_tags:
            if count % 100 == 0:
                print(f"[{count}/{total}] (Skipping known tags)", flush=True)
            continue
            
        print(f"[{count}/{total}] Analyzing new tags: {new_tags}...", flush=True)
        
        try:
            # Query Vibe
            data = get_oblast_from_vibe(msg)
            if not data:
                print("  -> Vibe failed or returned invalid JSON.", flush=True)
                continue
                
            for oblast_name, raions in data.items():
                normalized_name = normalize_oblast_name(oblast_name)
                
                if normalized_name in EXISTING_MAP:
                    rid = EXISTING_MAP[normalized_name]
                    save_region_file(rid, normalized_name, list(current_tags_set))
                    print(f"  -> Mapped to {normalized_name} ({rid})", flush=True)
                    global_mapped_hashtags.update(current_tags_set)
                else:
                    print(f"  -> Unknown Oblast: {oblast_name}", flush=True)
        except Exception as e:
            print(f"  [ERROR] Failed to process message {count}: {e}", flush=True)
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    main()