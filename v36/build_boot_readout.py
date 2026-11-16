"""Report actual upper ROM words without blocking the normal v35c boot."""
from hashlib import sha256
from pathlib import Path
from struct import pack

base = Path('Cyber-Cop_v35c_4MiB_boot_control.bin').read_bytes()
assert sha256(base).hexdigest() == '7acea947eb1cfb0a7e610b251a3e22a319b2dc230a0af60b793cbf714981c0af'
rom=bytearray(base)
# Nonblank data through the last bank also tests a loader that trims erased space.
for bank in range(32):
    begin=0x200000+(bank<<16)
    rom[begin:begin+0x10000]=pack('>H',0x5100+bank)*0x8000
probes={0x200000:0x915e,0x220000:0xa55a,0x260000:0x6d92,0x2aa000:0xf00d,0x3ffffe:0xbe71}
for addr,word in probes.items():rom[addr:addr+2]=pack('>H',word)
# Match test C's header and gate state at reading.
rom[0x1b0:0x1bc]=b' '*12
stub=0x1f0000
ram=0xffff0880
menu=stub+0x100
digits=stub+0x180
# Before SEGA: sample each address, convert to lowercase hex and store in RAM.
code=bytearray.fromhex('48e7fffe13fc000000a130f143f9')+pack('>I',ram)
code+=bytes.fromhex('45f9')+pack('>I',digits)
code+=bytes.fromhex('22fc726f6d20') # "rom "
for addr in probes:
    code+=bytes.fromhex('3039')+pack('>I',addr)
    code+=bytes.fromhex('7603e95832000241000f12f2100051cbfff2')
    code+=bytes.fromhex('12fc0020')
code+=bytes.fromhex('4cdf7fff')+base[0x394:0x39c]+bytes.fromhex('4ef90000039c')
native_menu=int.from_bytes(base[0xaba:0xabe],'big')
assert base[0xab8:0xaba]==bytes.fromhex('4ef9')
# Draw below the options via the game's own tile font.
draw=bytes.fromhex('4eb9')+pack('>I',native_menu)+bytes.fromhex('48e7fffe4bf9')+pack('>I',ram)
draw+=bytes.fromhex('363ce7047e1c3c3c20004eb90000ffbe4cdf7fff4e75')
for off,data in [(stub,code),(menu,draw),(digits,b'0123456789abcdef')]:
    assert base[off:off+len(data)]==b'\xff'*len(data)
    rom[off:off+len(data)]=data
rom[0x394:0x39c]=bytes.fromhex('4ef9001f00004e71')
rom[0xaba:0xabe]=pack('>I',menu)
rom[0x18e:0x190]=pack('>H',sum((rom[i]<<8)|rom[i+1] for i in range(0x200,len(rom),2))&0xffff)
out=Path('D_v35c_upper_ROM_readout.bin')
out.write_bytes(rom)
print(sha256(rom).hexdigest(),out)
