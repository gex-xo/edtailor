# Quick script to verify Russian content structure
import json

files = [
    'educational_content_enhanced_ru.json',
]

for f in files:
    try:
        with open(f'/home/artemis/edtailor/backend/scripts/seed_data/{f}', 'r', encoding='utf-8') as file:
            data = json.load(file)
            print(f"✓ {f}: Valid JSON")
            if 'categories' in data:
                print(f"  - {len(data['categories'])} categories")
            if 'fabrics' in data:
                print(f"  - {len(data['fabrics'])} fabrics")
            if 'garments' in data:
                print(f"  - {len(data['garments'])} garments")
            if 'terms' in data:
                print(f"  - {len(data['terms'])} terms")
    except Exception as e:
        print(f"✗ {f}: {e}")
