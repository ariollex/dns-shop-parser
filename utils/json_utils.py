import json
import os


def json_write(product_id, product_info):
    file_path = os.path.join('output', f'{product_id}.json')
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(product_info, json_file, ensure_ascii=False, indent=4)
