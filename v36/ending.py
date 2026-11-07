# Mission has its own ending illustration/text. Decode the original resource,
# deduplicate8x8 tiles, and feed native Genesis ending upload/fade routines.
sector,count=struct.unpack_from('>HH',A,0x62d0+15*4)
raw=DISK[sector*512:(sector+count)*512];data=bytearray();p=34
while len(data)<32000:
 n=raw[p];p+=1
 if n<128:data+=raw[p:p+n+1];p+=n+1
 elif n>128:data+=bytes([raw[p]])*(257-n);p+=1
pixels=[[sum(((data[y*160+plane*40+x//8]>>(7-x%8))&1)<<plane for plane in range(4)) for x in range(320)] for y in range(200)]
tiles=[];lookup={};names=bytearray(4096)
for ty in range(25):
 for tx in range(40):
  tile=bytes(pixels[ty*8+y][tx*8+x]<<4|pixels[ty*8+y][tx*8+x+1] for y in range(8) for x in range(0,8,2))
  if not any(tile):idx=0
  else:
   if tile not in lookup:lookup[tile]=40+len(tiles);tiles.append(tile)
   idx=lookup[tile]
  struct.pack_into('>H',names,((ty+1)*64+tx)*2,idx)
gfx=b''.join(tiles);assert len(gfx)<0x7000
table_hook(0x2ebc,asset('mission_ending_tiles',struct.pack('>H',len(gfx))+gfx),'ending_tiles36')
table_hook(0x2ece,asset('mission_ending_plane',names),'ending_plane36')
palette=asset('mission_ending_palette',struct.pack('>16H',*[mdcolor(aw(0x5504+i*2)) for i in range(16)]))
c.label('ending_palette36');tstcamp();c.branch('6700','ending_palette36_original');c.abs('43f9',palette);c.branch('6000','ending_palette36_upload')
c.label('ending_palette36_original');c.abs('43f9',0x2e90)
c.label('ending_palette36_upload');c.call(0x15f0);c.jump(0x2eee);patch(0x2ee6,'ending_palette36',8)
