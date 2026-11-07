sys.path.insert(0,str(OUT))
from scan_research import sheet
scan,_,_=sheet('mission',11);screen_data=bytearray()
for frame in range(15):
 px=[[scan[frame//4*48+y][frame%4*80+x] for x in range(80)] for y in range(48)]
 for col in range(10):
  for y in range(48):
   for x in range(0,8,2):screen_data.append(px[y][col*8+x]*16+px[y][col*8+x+1])
scanptr=asset('mission_scanman36b',screen_data)
for site in [0x7f5a,0x7f88,0x7fb8]:
 name='screen36b_'+hex(site)[2:];c.label(name);tstcamp();c.branch('6700',name+'_original');c.abs('23fc',scanptr);c.long(0xffff2178);c.jump(site+10);c.label(name+'_original');c.emit(src[site:site+10].hex());c.jump(site+10);patch(site,name,10)
# Each corrected label now owns all four tiles: the letter crosses a tile
# boundary at the requested position, so sharing that boundary tile was wrong.
stpix=json.loads((OUT/'st_items_pixels.json').read_text())
gfx=bytearray(src[0x39aa0:0x3f520]);first=40+len(gfx)//32
for item in [25,26,27]:
 off=int.from_bytes(src[0xa052+item*4:0xa054+item*4],'big');at=0x3f520+off+2*128
 oldtiles=list(struct.unpack_from('>4H',src,at))
 for col,tile in enumerate(oldtiles):
  data=bytearray(src[0x39aa0+((tile&2047)-40)*32:0x39aa0+((tile&2047)-40)*32+32])
  for y in range(18,24):
   for x in range(col*8,col*8+8):
    if 2<=x<28:
     v=stpix[100+y-4][(item-25)*32+x]
     p=(y%8)*4+x%8//2;shift=0 if x%2 else 4;data[p]=(data[p]&~(15<<shift))|(v<<shift)
  struct.pack_into('>H',r,at+col*2,first);first+=1;gfx+=data
bank=asset('item_graphics36c',struct.pack('>H',len(gfx))+gfx)
for at in [0x4e66,0x4ea0,0xfb30]:
 assert src[at:at+4]==struct.pack('>I',0x39a9e);r[at:at+4]=struct.pack('>I',bank)
