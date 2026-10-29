"""Rebuild v35c from two original BIN dumps; Python standard library only."""
from pathlib import Path
import sys, subprocess, tempfile, shutil, hashlib, importlib.util
ROOT=Path(__file__).resolve().parent
if len(sys.argv)!=4:raise SystemExit('Usage: python3 build_v35.py Cyber-Cop.bin Corporation.bin output_directory')
cyber,corp,out=[Path(p).resolve() for p in sys.argv[1:]]
for path,digest in [(cyber,'98838ed8d69349ab64a99e4a4e0ea72843d47b175b69fda36957283932f0aba9'),(corp,'226368b1693af2db21bb1cc640b94d5b021c9ff20fcb86207d2b76590503cc98')]:
 if hashlib.sha256(path.read_bytes()).hexdigest()!=digest:raise SystemExit('Wrong original ROM: '+str(path))
out.mkdir(parents=True,exist_ok=True)
with tempfile.TemporaryDirectory(prefix='cyber-cop-v35-') as td:
 work=Path(td)
 for name in ['v13','v34','mouse_lab','v35']:shutil.copytree(ROOT/name,work/name)
 subprocess.run([sys.executable,str(work/'v34/build_v34.py'),str(cyber),str(corp),str(work/'v34')],check=True)
 subprocess.run([sys.executable,str(work/'mouse_lab/build.py'),str(work/'v34/Cyber-Cop_v34.bin')],check=True)
 subprocess.run([sys.executable,str(work/'v35/build.py')],check=True)
 rom=(work/'v35/Cyber-Cop_v35c.bin').read_bytes()
 spec=importlib.util.spec_from_file_location('base_ips',work/'v13/build_v11.py');base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
 src=cyber.read_bytes();patch=base.ips(src+bytes(len(rom)-len(src)),rom)
 (out/'Cyber-Cop_v35c.bin').write_bytes(rom);(out/'Cyber-Cop_v35c.ips').write_bytes(patch)
 shutil.copy2(work/'v35/symbols.json',out/'symbols.json')
 print('v35 SHA256:',hashlib.sha256(rom).hexdigest())
