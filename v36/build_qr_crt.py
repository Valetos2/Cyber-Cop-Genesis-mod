"""Standalone Mega Drive QR scale selector, with no game assets or SRAM."""
from ctypes import CDLL, Structure, POINTER, c_int, c_ubyte, c_char_p
from ctypes.util import find_library
from pathlib import Path
import struct
import sys

URL=b'https://valetos2.github.io/cyber-cop-atlas'
SCALES=(2,3,4,5)
GREY=0xccc # Lightest non-white regular grey in original 5F world palette.
class QR(Structure):
    _fields_=[('version',c_int),('width',c_int),('data',POINTER(c_ubyte))]
lib=CDLL(find_library('qrencode') or 'libqrencode.so.4')
lib.QRcode_encodeString8bit.argtypes=(c_char_p,c_int,c_int)
lib.QRcode_encodeString8bit.restype=POINTER(QR)
lib.QRcode_free.argtypes=(POINTER(QR),)
ptr=lib.QRcode_encodeString8bit(URL,3,1) # Model 2, version 3, M
assert ptr and (ptr.contents.version,ptr.contents.width)==(3,29)
matrix=bytes(ptr.contents.data[i]&1 for i in range(29*29))
lib.QRcode_free(ptr)

tiles={bytes(32):0}
maps=[]
for scale in SCALES:
    size=37*scale
    left,top=(320-size)//2,(224-size)//2
    table=bytearray()
    def pix(x,y):
        if not (left<=x<left+size and top<=y<top+size):return 0
        x,y=(x-left)//scale-4,(y-top)//scale-4
        return 0 if 0<=x<29 and 0<=y<29 and matrix[y*29+x] else 1
    for ty in range(32):
        for tx in range(64):
            tile=bytes(pix(tx*8+x,ty*8+y)*16+pix(tx*8+x+1,ty*8+y)
                       for y in range(8) for x in range(0,8,2))
            table+=struct.pack('>H',tiles.setdefault(tile,len(tiles)))
    maps.append(table)
assert len(tiles)*32<0xc000

r=bytearray(0x10000)
W=lambda p,v:struct.pack_into('>H',r,p,v)
L=lambda p,v:struct.pack_into('>I',r,p,v)
L(0,0xfffffe00);L(4,0x200)
for at in range(8,0x100,4):L(at,0x200)
def field(a,n,s): r[a:a+n]=s.encode('ascii').ljust(n,b' ')
field(0x100,16,'SEGA MEGA DRIVE')
field(0x110,16,'(C)VALET2 2026')
for p in (0x120,0x150):field(p,48,'CYBER-COP ATLAS QR CRT TEST')
field(0x180,14,'GM 00000000-00')
field(0x190,16,'J');L(0x1a0,0);L(0x1a4,len(r)-1);L(0x1a8,0xff0000);L(0x1ac,0xffffff)
field(0x1f0,16,'JUE')

code=bytearray();labels={};fix=[]
def emit(h):code.extend(bytes.fromhex(h))
def mark(n):labels[n]=0x200+len(code)
def ref(op,n,width):
    emit(op);fix.append((len(code),n,width));code.extend(bytes(width))
def b(op,n):ref(op,n,2)
def addr(op,n):ref(op,n,4)
def control(v):emit(f'2d7c{v:08x}0004')
emit('46fc2700103900a100010200000f');b('6700','vdp')
emit('23fc5345474100a14000') # TMSS on hardware that has it
mark('vdp');emit('4df900c00000')
# H40, 224 lines, plane A at E000/plane B at C000, 64x32 cells.
for i,v in enumerate([4,4,0x38,0,6,0x68,0,0,0,0,0,0,0x81,0x3f,0,2,1,0,0]):
    emit(f'3d7c{0x8000+i*256+v:04x}0004')
control(0x40000000);emit('70003e3c7fff');mark('clear');emit('3c80');b('51cf','clear')
control(0x40000010);emit('2c807000') # zero VSRAM
control(0xc0000000);emit(f'3c803cbc{GREY:04x}')
control(0x40000000);addr('41f9','tiles');emit(f'3e3c{len(tiles)*16-1:04x}')
mark('tile_copy');emit('3c98');b('51cf','tile_copy')
emit('13fc004000a10009' '13fc000000a10003') # pad 1 TH output, low phase
emit('7a007800');mark('draw')
emit('3d7c81040004') # blank while copying the map
control(0x60000003);addr('41f9','maps');emit('3005e148e948d0c0') # index * 4096
emit('3e3c07ff');mark('map_copy');emit('3c98');b('51cf','map_copy')
emit('13c500ff0000' '3d7c81440004')
mark('wait_out');emit('0839000300c00005');b('6600','wait_out')
mark('wait_in');emit('0839000300c00005');b('6700','wait_in')
emit('0839000500a10003');b('6600','released')
emit('4a44');b('6600','wait_out')
emit('7801524502450003');b('6000','draw')
mark('released');emit('7800');b('6000','wait_out')

mark('tiles');code.extend(b''.join(tiles))
mark('maps');code.extend(b''.join(maps))
for p,n,width in fix:code[p:p+width]=(labels[n]-(0x200+p) if width==2 else labels[n]).to_bytes(width,'big',signed=width==2)
r[0x200:0x200+len(code)]=code
W(0x18e,sum(v for v, in struct.iter_unpack('>H',r[0x200:]))&65535)
Path(sys.argv[1]).write_bytes(r)
