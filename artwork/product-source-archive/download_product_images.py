from pathlib import Path
import json, re, urllib.request

base = Path(__file__).resolve().parent
manifest = json.loads((base / 'manifest_all.json').read_text(encoding='utf-8'))

def slug(text):
    text = re.sub(r'[^a-zA-Z0-9]+', '-', text.strip()).strip('-').lower()
    return text or 'item'

def download_group(group_name, items):
    outdir = base / 'downloads' / group_name
    outdir.mkdir(parents=True, exist_ok=True)
    for idx, item in enumerate(items, start=1):
        title = slug(item['title'])
        variant = slug(item.get('variant') or 'default')
        ext = '.jpg'
        if '.png' in item['image_url'].lower():
            ext = '.png'
        path = outdir / f"{idx:02d}_{title}__{variant}{ext}"
        print('Downloading', item['title'], '->', path.name)
        urllib.request.urlretrieve(item['image_url'], path)

if __name__ == '__main__':
    download_group('hats-beanies', manifest['hats_beanies'])
    download_group('gear-accessories', manifest['gear_accessories'])
    print('Done.')
