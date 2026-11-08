# Amiga guard pixels, enlarged2x; crop includes the top of the belt.
# Original Amiga guard, local resource7; original sprite palette for Parking.
guard_sheet,_,_=sheet('mission',7)
pixels=[[guard_sheet[(y-6)//2][128+(x-4)//2] if 4<=x<68 and 6<=y<102 else 0 for x in range(72)] for y in range(104)]
tiles=bytearray()
for ty in range(13):
 for tx in range(9):
  for y in range(8):
   for x in range(0,8,2):tiles.append(pixels[ty*8+y][tx*8+x]*16+pixels[ty*8+y][tx*8+x+1])
gfx=asset('memorial_guard_tiles36b',tiles);names=bytearray(4096)
for ty in range(13):
 for tx in range(9):struct.pack_into('>H',names,(7+ty)*128+(24+tx)*2,40+ty*9+tx)
nameptr=asset('memorial_names36b',names);pal=asset('memorial_palette36c',struct.pack('>16H',*[mdcolor(aw(al(0x131e8+6*4)+(8+i)*2)) for i in range(16)]))
c.label('memorial36b');c.emit('48e7fffe')
# Clear current AND target palettes before the first VBlank: power-on RAM may
# contain coloured values. Also restore plane-A scroll after menu timeout.
c.abs('41f9',0xffff282c);c.emit('703f429851c8fffc')
c.abs('4df9',0xc00000);c.emit('2d7cc00000000004703f72003c8151c8fffc')
c.emit('7000');c.call(0x1602)

for dest in [0xc000,0xe000]:c.emit('323c1000343c'+f'{dest:04x}');c.call(0x31b0)
c.emit('323c0400343cd800');c.call(0x31b0);c.emit('323c0400343cdc00');c.call(0x31b0);c.call(0x2576)
c.abs('41f9',gfx);c.emit('303c0ea0323c0500');c.call(0x2580)
c.abs('41f9',nameptr);c.emit('303c1000323ce000');c.call(0x2580)
draw('in memory of',0xe58e);draw('kevin bulmer',0xe68e)
c.abs('41f9',0xffff282c);c.abs('43f9',pal);c.call(0x15f0);wi(0xffff286a,0xeee);bi(0xffff2702,255);c.call(0x1646);wi(0xffff0854,150)
c.label('memorial_wait36b');c.call(0x2930);c.call(0x53a8);c.emit('024000f00c4000f0');c.branch('6600','memorial_end36b');c.abs('5379',0xffff0854);c.branch('6600','memorial_wait36b')
c.label('memorial_end36b');c.call(0x1612)
for dest in [0xc000,0xe000]:c.emit('323c1000343c'+f'{dest:04x}');c.call(0x31b0)
c.emit('4cdf7fff');c.emit(src[0x394:0x39c].hex());c.jump(0x39c);patch(0x394,'memorial36b',8)
