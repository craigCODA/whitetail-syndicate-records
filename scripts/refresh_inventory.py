#!/usr/bin/env python3
"""Regenerate the readable material directory and content inventory."""
from pathlib import Path
import hashlib, json

ROOT = Path(__file__).resolve().parents[1]
GENERATED = {'records/file-inventory.json', 'records/material-directory.md'}
IGNORED_PARTS = {'.git', '__pycache__', 'node_modules'}

def files():
    return sorted(p for p in ROOT.rglob('*') if p.is_file() and not (set(p.relative_to(ROOT).parts) & IGNORED_PARTS) and p.relative_to(ROOT).as_posix() not in GENERATED)

def main():
    materials = json.loads((ROOT/'records/materials.json').read_text())['materials']
    rows = ['# Material directory', '', 'Generated from materials.json. Edit records with scripts/record_material.py, then refresh.', '', '| Area | Material | Status | How created | Used for |', '| --- | --- | --- | --- | --- |']
    clean = lambda value: str(value).replace('|', '/').replace('\n', ' ')
    for m in sorted(materials, key=lambda m: (m['area'], m['path'])):
        rows.append('| '+clean(m['area'])+' | ['+clean(m['title'])+'](../'+m['path']+') | '+clean(m['status'])+' | '+clean(m['how_created'])+' | '+clean(m['used_for'])+' |')
    (ROOT/'records/material-directory.md').write_text('\n'.join(rows)+'\n')
    inventory = [{'path': p.relative_to(ROOT).as_posix(), 'size_bytes': p.stat().st_size, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in files()]
    (ROOT/'records/file-inventory.json').write_text(json.dumps({'schema_version':1, 'excluded_generated_paths':sorted(GENERATED), 'files':inventory}, indent=2)+'\n')
    print(json.dumps({'registered_materials':len(materials), 'inventoried_files':len(inventory)}))

if __name__ == '__main__':
    main()
