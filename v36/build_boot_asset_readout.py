"""Use the v35c title path to report word and byte reads of actual v36 assets."""
from hashlib import sha256
import json
from pathlib import Path
from struct import pack

base=Path('Cyber-Cop_v35c_4MiB_boot_control.bin').read_bytes()
source=Path('Cyber-Cop_v36b_test01.bin').read_bytes()
assert sha256(base).hexdigest()=='7acea947eb1cfb0a7e610b251a3e22a319b2dc230a0af60b793cbf714981c0af'
assert sha256(source).hexdigest()=='bbcf44f728058e1cba83dd252900cd65610b001968ca2ac22a80d2bfc84fdf26'
symbols=json.loads(Path('v36/symbols.json').read_text())
probes=[symbols['menu36_title_0'],symbols['z80_driver36'],
        symbols['memorial_palette36c']+2,symbols['memorial_guard_tiles36b']+0x240]
assert all(not a%2 and 0x200000<=a<0x400000 for a in probes)
rom=bytearray(base)
# Unlike D, keep the v36b header (including SRAM declaration) and sparse banks.
rom[0x100:0x200]=source[0x100:0x200]
rom[0x200000:]=source[0x200000:]
stub,menu,digits=0x1f0000,0x1f0200,0x1f0280
ram=0xffff0880
code=bytearray.fromhex('48e7fffe13fc000000a130f143f9')+pack('>I',ram)
code+=bytes.fromhex('45f9')+pack('>I',digits)
line=2+5*len(probes)
for bytewise,label in [(False,b'w '),(True,b'b ')]:
    code+=bytes.fromhex('32fc')+label
    for a in probes:
        if bytewise:
            code+=bytes.fromhex('1039')+pack('>I',a)+bytes.fromhex('e1481039')+pack('>I',a+1)
        else:
            code+=bytes.fromhex('3039')+pack('>I',a)
        code+=bytes.fromhex('7603e95832000241000f12f2100051cbfff212fc0020')
code+=bytes.fromhex('4cdf7fff')+base[0x394:0x39c]+bytes.fromhex('4ef90000039c')
native_menu=int.from_bytes(base[0xaba:0xabe],'big')
assert base[0xab8:0xaba]==bytes.fromhex('4ef9')
draw=bytes.fromhex('4eb9')+pack('>I',native_menu)+bytes.fromhex('48e7fffe')
for i in range(2):
    draw+=bytes.fromhex('4bf9')+pack('>I',ram+i*line)
    draw+=bytes.fromhex('363c')+pack('>H',0xe704+i*0x100)+bytes((0x7e,line-1))
    draw+=bytes.fromhex('3c3c20004eb90000ffbe')
draw+=bytes.fromhex('4cdf7fff4e75')
assert stub+len(code)<=menu and menu+len(draw)<=digits
for off,data in [(stub,code),(menu,draw),(digits,b'0123456789abcdef')]:
    assert base[off:off+len(data)]==b'\xff'*len(data)
    rom[off:off+len(data)]=data
rom[0x394:0x39c]=bytes.fromhex('4ef9001f00004e71')
rom[0xaba:0xabe]=pack('>I',menu)
rom[0x18e:0x190]=pack('>H',sum((rom[i]<<8)|rom[i+1] for i in range(0x200,len(rom),2))&0xffff)
out=Path('G_v36b_asset_readout.bin')
out.write_bytes(rom)
print(sha256(rom).hexdigest(),out)
print(' '.join(f'{a:06x}={rom[a:a+2].hex()}' for a in probes))
