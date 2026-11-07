# Preserve the intermediate arrow tones when the lower rocker is pressed.
for x,y in [(167,39),(167,40),(166,43),(166,44),(165,47)]:
 needle=bytes.fromhex('303c'+f'{x:04x}'+'323c'+f'{y:04x}'+'4eb9')+struct.pack('>I',S['pixel_address'])+bytes.fromhex('7203')
 lo=S['scan_contrast35'];hi=S['scan_contrast35_done'];assert src[lo:hi].count(needle)==1
 p=src.index(needle,lo,hi)+len(needle)-1;r[p]=2

# Mission destruction and projectile-height tables differ at the new props.
# Its barrel is intentionally indestructible (FF); stools become5D/5E debris.
for name,site,reg,original,data,replay in [
 ('destruction36c',0xab78,'49f9',0x113e4,A[0x13f32:0x13f72],src[0xab7c:0xab80]),
 ('hitheight36c',0xab14,'47f9',0x11478,A[0x13fc8:0x140c8],src[0xab18:0xab1c])]:
 ptr=asset(name+'_table',data);c.label(name);tstcamp();c.branch('6700',name+'_original');c.abs(reg,ptr);c.branch('6000',name+'_ready');c.label(name+'_original');c.abs(reg,original);c.label(name+'_ready');c.emit(replay.hex());c.jump(site+8);patch(site,name,8)

# Automatic equipment search advances silently; deliberate FD16 still plays SFX.
assert src[0xfc70:0xfc74]==bytes.fromhex('4eba00a4')
r[0xfc72:0xfc74]=struct.pack('>h',0xfd2a-0xfc72)
# The alarm owns one countdown, not five consecutive retriggers.
assert src[0x7d46:0x7d4a]==bytes.fromhex('33fc0064')
r[0x7d48:0x7d4a]=struct.pack('>H',500)

# Native airlock activation latches its texture until closing the interface.
# Border upload is reversible: run the same swap before and after VRAM upload.
c.label('airlock_border36c');c.abs('4a79',P);c.branch('6700','airlock_border36c_normal')
c.emit('0cb9000077a8');c.long(0xffff26b8);c.branch('6600','airlock_border36c_normal')
c.emit('0c7900c0');c.long(0xffff22f2);c.branch('6600','airlock_border36c_normal')
c.emit('303c00a1343c0041363c00af383c004f3a003c02');c.jump(S['border_top'])
c.label('airlock_border36c_normal');c.emit(src[S['panel_border']:S['panel_border']+6].hex());c.jump(S['panel_border']+6);patch(S['panel_border'],'airlock_border36c')

# Name rendering trims native spaces before centering. Add padding AFTER trim,
# only for the exact card label, keeping the packed native string table intact.
card=asset('card_padded36c',b'card ')
c.label('card_center36c');c.emit('0c470003');c.branch('6600','card_center36c_draw')
c.emit('0c9563617264');c.branch('6600','card_center36c_draw');c.abs('4bf9',card);c.emit('7e04')
c.label('card_center36c_draw');c.emit(src[V['name26_draw']:V['name26_draw']+6].hex());c.jump(V['name26_draw']+6);patch(V['name26_draw'],'card_center36c')

# Equipment replaces the character tile bank. Retain its 4x4 portrait in a
# private VRAM bank, with palette2; native equipment uses palette0.
portrait_gfx=[];portrait_names=[];portrait_pal=[]
for char in range(6):
 header=struct.unpack_from('>I',src,0xf84c+char*4)[0]
 mapping=struct.unpack_from('>I',src,0xf864+char*4)[0]
 palette=struct.unpack_from('>I',src,0xf7d4+char*4)[0]
 tiles=bytearray();names=bytearray()
 for y in range(4):
  for x in range(4):
   entry=struct.unpack_from('>H',src,mapping+y*128+x*2)[0]
   tile=(entry&2047)-40;assert 0<=tile<struct.unpack_from('>H',src,header)[0]//32
   tiles+=src[header+2+tile*32:header+2+(tile+1)*32]
   names+=struct.pack('>H',0x45f0+y*4+x|(entry&0x1800))
 portrait_gfx.append(asset('gear_portrait_gfx36c_'+str(char),tiles))
 portrait_names.append(asset('gear_portrait_names36c_'+str(char),names))
 portrait_pal.append(palette)
ptable=asset('gear_portraits36c',b''.join(struct.pack('>III',*row) for row in zip(portrait_gfx,portrait_names,portrait_pal)))
c.label('gear_portrait36c');c.emit('48e7fffe');c.abs('3039',0xffff2a38);c.emit('c0fc000c');c.abs('4bf9',ptable);c.emit('dac02055')
c.emit('303c0200323cbe00');c.call(0x2580)
c.emit('226d0008');c.abs('41f9',0xffff286c);c.call(0x15f0)
c.emit('286d0004')
for y in range(4):
 for x in range(4):
  c.emit('301c343c'+f'{0xe804+y*128+x*2:04x}');c.call(0x35fe)
c.emit('4cdf7fff');c.emit(src[0xfb88:0xfb8e].hex());c.jump(0xfb8e);patch(0xfb88,'gear_portrait36c')

# Mission's airlock sets a fixed BCD8652 (Amiga9F04). It is not a door
# randomizer entry. Laboratory override0451 remains first in priority.
c.label('airlock_code36c');tstcamp();c.branch('6700','airlock_code36c_native')
c.abs('4a79',0xffff026c);c.branch('6600','airlock_code36c_native');wi(0xffff243a,0x8652);c.jump(0x7798)
c.label('airlock_code36c_native');c.jump(S['airlock_code35']);patch(0x7790,'airlock_code36c',8)
