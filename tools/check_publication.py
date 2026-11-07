#!/usr/bin/env python3
"""Review only proposed files, not the ROM or the repository's full history."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

TEXT_EXTENSIONS = {'.py', '.md', '.csv', '.yml', '.yaml', '.toml', '.txt'}
JSON_NAMES = {'symbols.json', 'input_manifest.json', 'PUBLICATION_MANIFEST.json'}
# Reviewed source-only web template/test; generated atlas HTML remains blocked.
SPECIAL_NAMES = {'.gitignore', '.githooks/pre-commit', 'atlas37/template.html', 'atlas38/template.html', 'atlas38/test_ui.js'}
BLOCKED_PARTS = {'upload', 'transfer_helpers', 'transfer_test02', '__pycache__', 'st_resources', 'rebuild_verify_test02'}

def problem(name, data):
    p = Path(name)
    if p.is_absolute() or '..' in p.parts:
        return 'unsafe path'
    if any(part in BLOCKED_PARTS for part in p.parts):
        return 'private/generated directory'
    if name not in SPECIAL_NAMES and p.suffix not in TEXT_EXTENSIONS and not (p.suffix == '.json' and p.name in JSON_NAMES):
        return 'not an approved source/metadata extension (review explicitly; no binary bypass)'
    if len(data) > 1_000_000:
        return 'unexpectedly large source file'
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError:
        return 'non-UTF8/binary file'
    if '\0' in text:
        return 'binary NUL in source'
    if re.search(r'data:(?:image|audio|application)/[^\s]*;base64,[A-Za-z0-9+/=]{256,}', text):
        return 'embedded resource data URL'
    if re.search(r'(?<![0-9A-Fa-f])[0-9A-Fa-f]{2048,}(?![0-9A-Fa-f])', text):
        return 'large hex payload; possible binary dump'
    if p.name == 'symbols.json':
        try:
            obj = json.loads(text)
            if not isinstance(obj, dict) or not all(isinstance(k,str) and type(v) is int for k,v in obj.items()):
                return 'symbols must be name-to-address metadata, not asset data'
        except ValueError:
            return 'invalid symbol JSON'
    return None

def git(*args):
    return subprocess.check_output(['git', *args])

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--directory', type=Path, help='Check an explicit proposed upload directory (API workflow)')
    args = ap.parse_args()
    if args.directory:
        paths = sorted(p for p in args.directory.rglob('*') if p.is_file())
        files = [(p.relative_to(args.directory).as_posix(), p.read_bytes()) for p in paths]
    else:
        branch = git('symbolic-ref', '--short', 'HEAD').decode().strip()
        if branch != 'wip':
            print('REFUSED: this workflow publishes only wip; current branch is '+branch, file=sys.stderr)
            return 1
        names = git('diff', '--cached', '--name-only', '--diff-filter=ACMR', '-z').decode().split('\0')
        files = [(name, git('show', ':'+name)) for name in names if name]
    errors = [(name, why) for name, data in files if (why := problem(name, data))]
    for name, why in errors:
        print(f'REFUSED {name}: {why}', file=sys.stderr)
    if errors:
        return 1
    print(f'PASS publication preflight: {len(files)} proposed text/source files. Manual diff review still required.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
