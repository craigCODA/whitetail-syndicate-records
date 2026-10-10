#!/usr/bin/env python3
"""Register an existing file, or update its record, and append a dated event."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json

ROOT = Path(__file__).resolve().parents[1]
STATUSES = ['source','draft','awaiting-review','approved','published','historical','unresolved','current']

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path',help='Existing file path relative to this repository')
    for field in ['area','title','how','used-for','source']:
        parser.add_argument('--'+field,required=True)
    parser.add_argument('--status',required=True,choices=STATUSES)
    parser.add_argument('--source-ref',action='append',default=[],help='Existing ID from records/sources.json; repeat for multiple sources')
    args=parser.parse_args()
    rel=Path(args.path)
    if rel.is_absolute() or '..' in rel.parts:
        parser.error('path must be a repository-relative path without parent traversal')
    path=(ROOT/rel).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file():
        parser.error('path must identify an existing file inside the repository')
    source_ids={s['id'] for s in json.loads((ROOT/'records/sources.json').read_text())['sources']}
    if set(args.source_ref)-source_ids:
        parser.error('source-ref must identify a registered source')
    relative=path.relative_to(ROOT).as_posix()
    if relative in {'records/materials.json','records/activity.jsonl','records/file-inventory.json','records/material-directory.md'}:
        parser.error('central registers and generated files are maintained by the scripts')
    db_path=ROOT/'records/materials.json'
    db=json.loads(db_path.read_text())
    previous=next((m for m in db['materials'] if m['path']==relative),None)
    now=datetime.now(timezone.utc).isoformat()
    entry={'id':previous['id'] if previous else 'material-'+hashlib.sha256(relative.encode()).hexdigest()[:12], 'path':relative,'area':args.area,'title':args.title,'status':args.status,'source_refs':args.source_ref,'source_note':args.source,'how_created':args.how,'used_for':args.used_for,'updated_at':now}
    if previous:
        db['materials'][db['materials'].index(previous)]=entry
    else:
        db['materials'].append(entry)
    tmp=db_path.with_suffix('.tmp')
    tmp.write_text(json.dumps(db,indent=2,ensure_ascii=False)+'\n');tmp.replace(db_path)
    event={'timestamp':now,'action':'updated_material' if previous else 'added_material','material':entry,'previous_record':previous,'file_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    with (ROOT/'records/activity.jsonl').open('a') as f:
        f.write(json.dumps(event,ensure_ascii=False)+'\n')
    print(json.dumps({'path':relative,'action':event['action']}))

if __name__=='__main__':
    main()
