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
# Replace the label strip with the original Atari artwork. Reuse the three
# existing private letter tiles at the RIGHT edge, keeping shared Holo tiles.
stpix=json.loads((OUT/'st_items_pixels.json').read_text());written={}
for item in [25,26,27]:
 off=int.from_bytes(src[0xa052+item*4:0xa054+item*4],'big');at=0x3f520+off+2*128
 oldtiles=list(struct.unpack_from('>4H',src,at));newtiles=[oldtiles[3],oldtiles[1],oldtiles[2],oldtiles[0]]
 r[at:at+8]=struct.pack('>4H',*newtiles)
 for col,tile in enumerate(newtiles):
  data=bytearray(src[0x39aa0+((oldtiles[col]&2047)-40)*32:0x39aa0+((oldtiles[col]&2047)-40)*32+32])
  for y in range(18,24):
   for x in range(max(col*8,2),min(col*8+8,30)):
    v=stpix[100+y-4][(item-25)*32+x-2] if x>=4 else 7;p=(y%8)*4+x%8//2;shift=0 if x%2 else 4;data[p]=(data[p]&~(15<<shift))|(v<<shift)
  addr=0x39aa0+((tile&2047)-40)*32
  if addr in written:assert written[addr]==data,(item,col)
  written[addr]=data;r[addr:addr+32]=data
