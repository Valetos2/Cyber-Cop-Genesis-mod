# Author-owned QR matrix from the CRT demo, Model 2 version 3/M, same URL.
qr38=[list(map(int,line)) for line in (OUT/'atlas_qr_matrix.txt').read_text().splitlines()]
assert len(qr38)==29 and all(len(row)==29 and set(row)<={0,1} for row in qr38)
qr_title38='CYBER-COP INTERACTIVE ATLAS'
qr_url38='https://valetos2.github.io/cyber-cop-atlas'
# Black ink (palette index 1); transparent pixels show CRAM 0, including
# the active background, off-screen borders, and the four-module quiet zone.
pixels38=[bytearray(320) for _ in range(224)]
for y,row in enumerate(qr38):
    for x,black in enumerate(row):
        if black:
            for dy in range(5):
                pixels38[39+y*5+dy][87+x*5:92+x*5]=b'\x01'*5
# The original bitmap is all capitals. Editable 5-bit lowercase and
# punctuation stencils keep the italic silhouette and the exact URL case.
lower38={k:bytes.fromhex(v) for k,v in {
 'a':'00000e011f111f', 'b':'10101e1111111e', 'c':'00000e1110110e',
 'e':'00000e111f100f', 'g':'00000f11110f011e', 'h':'10101e11111111',
 'i':'04000c0404040e', 'l':'0c04040404040e', 'o':'00000e1111110e',
 'p':'00001e11111e1010', 'r':'00001619101010', 's':'00000f100e011e',
 't':'04041f04040403', 'u':'0000111111110f', 'v':'00001111110a04',
 'y':'00001111110f011e',
 '-':'0000001c000000', '.':'00000000000c0c', ':':'000c0c000c0c00',
 '/':'01010204081010',
}.items()}
def atlas_glyph38(letter):
    if letter==' ':
        return [[0]*8]*8
    if letter in lower38:
        return [[int(bool(row&(16>>x))) if 0<=x<5 else 0 for x in range(-int(i<3),8-int(i<3))]
                for i,row in enumerate(lower38[letter])]
    i=ord(letter)-64 if 'A'<=letter<='Z' else ord(letter)-0x15
    glyph=src[0x30716+i*32:0x30716+(i+1)*32]
    assert len(glyph)==32
    return [[int(bool(bv)) for b in glyph[y*4:y*4+4] for bv in (b>>4,b&15)] for y in range(8)]
def atlas_line38(line,y,step):
    x=(320-(len(line)-1)*step-8)//2
    for char in line:
        for dy,row in enumerate(atlas_glyph38(char)):
            for dx,ink in enumerate(row):
                if ink:pixels38[y+dy][x+dx]=1
        x+=step
atlas_line38(qr_title38,6,8)
atlas_line38(qr_url38,209,7)

# Reuse identical patterns; reserve the native font and blank tile 0.
tiles38={}
names38=bytearray(4096)
for ty in range(28):
    for tx in range(40):
        tile=bytes(pixels38[ty*8+y][tx*8+x]*16+pixels38[ty*8+y][tx*8+x+1]
                   for y in range(8) for x in range(0,8,2))
        if any(tile):
            struct.pack_into('>H',names38,(ty*64+tx)*2,tiles38.setdefault(tile,40+len(tiles38)))
qr_tiles38=asset('atlas_qr_tiles38',b''.join(tiles38))
qr_names38=asset('atlas_qr_names38',names38)
assert len(tiles38)*32<0x3000
c.label('atlas_qr38')
c.emit('48e7fffe')
# Set the same backdrop colour for both the visible screen and overscan.
c.abs('4df9',0xc00000)
c.emit('3d7c87000004')
c.emit('7000');c.call(0x1602)
for dest,length in [(0xc000,0x1000),(0xe000,0x1000),(0xd800,0x400),(0xdc00,0x400)]:
    c.emit(f'323c{length:04x}343c{dest:04x}');c.call(0x31b0)
for address,length,dest in [(qr_tiles38,32*len(tiles38),0x0500),(qr_names38,4096,0xe000)]:
    c.abs('41f9',address);c.emit(f'303c{length:04x}323c{dest:04x}');c.call(0x2580)
# Explicit palette: grey background, black text and QR.
c.abs('41f9',0xffff282c);c.emit('703f429851c8fffc')
wi(0xffff282c,0x0ccc);bi(0xffff2702,255);c.call(0x1646)
c.call(0x53a8);c.emit('024000f03c007e00') # initial held keys
c.emit('3e3c012b') # 300 VBlanks
c.label('atlas_qr_wait38')
c.emit('48e70300');c.call(0x2930);c.call(0x53a8);c.emit('4cdf00c0')
c.emit('024000f032004641c2463c004a41')  # (~current & previous) = new press
c.branch('6600','atlas_qr_end38')
c.branch('51cf','atlas_qr_wait38')
c.label('atlas_qr_end38')
c.call(0x1612)
c.emit('323c1000343ce000');c.call(0x31b0)
c.emit('4cdf7fff323c0032');c.call(0x7994);c.jump(0x4fa)
assert r[0x4f2:0x4fa]==bytes.fromhex('323c00324eba749c')
patch(0x4f2,'atlas_qr38',8)
