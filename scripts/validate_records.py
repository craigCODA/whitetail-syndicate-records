#!/usr/bin/env python3
"""Check provenance, registered paths, inventory hashes and authored links."""
from pathlib import Path
import hashlib, json, re, sys
from refresh_inventory import ROOT, GENERATED, files

def main():
    errors=[]
    sources=json.loads((ROOT/'records/sources.json').read_text())['sources']
    materials=json.loads((ROOT/'records/materials.json').read_text())['materials']
    inventory=json.loads((ROOT/'records/file-inventory.json').read_text())['files']
    source_ids=[s['id'] for s in sources]
    if len(source_ids)!=len(set(source_ids)):errors.append('duplicate source IDs')
    for label,values in [('material IDs',[m['id'] for m in materials]),('material paths',[m['path'] for m in materials]),('inventory paths',[f['path'] for f in inventory])]:
        if len(values)!=len(set(values)):errors.append('duplicate '+label)
    for m in materials:
        p=(ROOT/m['path']).resolve()
        if not p.is_relative_to(ROOT) or not p.is_file():errors.append('missing or unsafe material path '+m['path'])
        if set(m['source_refs'])-set(source_ids):errors.append('unknown source for '+m['path'])
        for field in ['title','status','source_note','how_created','used_for']:
            if not m.get(field):errors.append('empty '+field+' for '+m['path'])
    for source in sources:
        for path in source.get('repository_paths',[]):
            if not (ROOT/path).exists():errors.append('missing source derivative '+path)
    actual={p.relative_to(ROOT).as_posix():p for p in files()}
    expected={f['path']:f for f in inventory}
    if actual.keys()!=expected.keys():errors.append('inventory file set mismatch; run refresh_inventory.py')
    for path,p in actual.items():
        item=expected.get(path)
        if item and (p.stat().st_size!=item['size_bytes'] or hashlib.sha256(p.read_bytes()).hexdigest()!=item['sha256']):errors.append('inventory hash mismatch '+path)
    unregistered=set(actual)-{m['path'] for m in materials}-{'records/materials.json','records/activity.jsonl'}
    if unregistered:errors.append('unregistered files: '+', '.join(sorted(unregistered)))
    authored=[ROOT/'README.md',ROOT/'AGENTS.md',ROOT/'STATUS.md']+[ROOT/area/'README.md' for area in ['interviews','product-audit','outreach','website','launch-research','artwork','records']]+[ROOT/'records/material-directory.md',ROOT/'outreach/contacts/index.md',ROOT/'interviews/nathan-deville/README.md']
    authored += [p for p in [ROOT/'records/billing/README.md', ROOT/'records/billing/summary.md', ROOT/'records/evidence-standards.md', ROOT/'records/billing/provenance.md'] if p.exists()]
    for p in authored:
        text=re.sub(r'```[\s\S]*?```','',p.read_text())
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',text):
            if re.match(r'^[a-z]+:',target) or target.startswith('#'):continue
            target=target.split('#')[0]
            if target and not (p.parent/target).exists():errors.append('broken link in '+str(p.relative_to(ROOT))+': '+target)
    for line in (ROOT/'records/activity.jsonl').read_text().splitlines():
        event=json.loads(line)
        if not event.get('timestamp') or not event.get('action'):errors.append('invalid activity event')
    secrets=re.compile(r'(?<![A-Za-z0-9])(gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}|sk-[A-Za-z0-9_-]{32,})(?![A-Za-z0-9])')
    for p in files():
        if p.suffix in ['.md','.json','.jsonl','.py','.js','.html','.csv'] and secrets.search(p.read_text(errors='ignore')):errors.append('credential-shaped value requires review in '+str(p.relative_to(ROOT)))
    if errors:
        print('\n'.join('ERROR '+e for e in errors));return 1
    print(json.dumps({'result':'PASS','registered_materials':len(materials),'sources':len(sources),'verified_file_hashes':len(inventory),'authored_link_checks':len(authored)}));return 0

if __name__=='__main__':
    sys.exit(main())
