from pathlib import Path
import sys,json,hashlib
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'v13'))
import build_v13 as previous
import build_v11 as base
VERSION='v34'
STATE=0xffff0100
FLAGS={'energy':STATE+4,'battery':STATE+5,'invincible':STATE+6,'dither_off':STATE+7,'stripe_off':STATE+8,'all_access':STATE+14,'autosleep':STATE+44}
SOUND=STATE+10
SOUND_COMMANDS=[(0,0),(0,1),(0,33),(0,31),(0,32),(0,34),(0,35)]+[(1,x) for x in list(range(36,52))+[53]]

def build(source,corp,version=VERSION):
 assert version.startswith("v") and version[1:].isdigit() and len(version)<=40
 assert hashlib.sha256(corp).hexdigest()=='226368b1693af2db21bb1cc640b94d5b021c9ff20fcb86207d2b76590503cc98', 'Wrong Corporation source ROM'
 rom,old=previous.build(source);r=bytearray(rom);c=base.Code();c.b=bytearray(b'\xff'*(0xf6000-base.BASE));start=len(c.b)
 def hook(a,end,label):
  assert end-a>=6 and (end-a)%2==0
  r[a:end]=bytes.fromhex('4ef9')+c.labels[label].to_bytes(4,'big')+bytes.fromhex('4e71')*((end-a-6)//2)
 def word(addr,v):c.emit('33fc'+f'{v&65535:04x}');c.address(addr)
 def byte(addr,v):c.emit('13fc'+f'{v&255:04x}');c.address(addr)
 def toggle(addr):c.emit('0a3900ff');c.address(addr)
 def tst(addr):c.abs('4a39',addr)
 def stringptr(label):c.emit('4bf9');c.fix.append((len(c.b),('absolute',label)));c.address(0)
 # Code.finish handles branch fixups only, fix our absolute labels at end.
 strings={}
 def drawtext(text,where):
  label='text_'+str(len(strings));strings[label]=text
  stringptr(label);c.emit('363c'+f'{where:04x}'+'3e3c'+f'{len(text)-1:04x}'+'3c3c2000');c.call(0xffbe)
 c.label('settings_init');c.emit('0cb900434332');c.address(STATE);c.branch('6700','init_done')
 c.emit('23fc00434332');c.address(STATE)
 for addr in range(STATE+4,STATE+48,4):c.abs('42b9',addr)
 c.label('init_done');c.emit('4e75')
 c.label('intro14');c.call(c.labels['settings_init']);c.jump(old['intro_enter']);hook(0x386,0x38c,'intro14')
 # All action keys confirm; editor Start is independent of A/B/C.
 c.label('front14')
 # Special pre-game call sites: agent selection ignores Start; story accepts all actions.
 for site in [0xf6aa,0xf708,0xf740]:
  c.emit('0c97'+f'{site:08x}');c.branch('6700','agent15_pad')
 c.emit('0c9700000c00');c.branch('6700','story15_pad')
 c.emit('0c9700000d10');c.branch('6700','password16_pad')
 tst(0xffff0014);c.branch('6600','front14_store');tst(0xffff0015);c.branch('6700','front14_store')
 c.emit('0c390002');c.address(0xffff0015);c.branch('6600','front14_map')
 c.emit('3200024100f00c4100f0');c.branch('6700','front14_unlatch')
 c.emit('004000f0');c.branch('6000','front14_store')
 c.label('front14_unlatch');c.abs('50f9',0xffff0015)
 c.label('front14_map');c.emit('0c970000fbd8');c.branch('6700','front14_editor')
 c.emit('3200024100f00c4100f0');c.branch('6700','front14_no_confirm')
 c.emit('08800004')
 c.label('front14_no_confirm');c.emit('00400060');c.branch('6000','front14_store')
 c.label('front14_editor');c.emit('3200024100700c410070');c.branch('6700','front14_editor_finish');c.emit('08800004')
 c.label('front14_editor_finish');c.emit('00400060')
 c.label('front14_store');c.abs('33c0',0xffff0004);c.emit('4e75')
 c.label('agent15_pad');c.emit('3200024100700c410070');c.branch('6700','agent15_done');c.emit('08800004')
 c.label('agent15_done');c.emit('004000e0');c.branch('6000','front14_store')
 c.label('story15_pad');c.emit('3200024100f00c4100f0');c.branch('6700','agent15_done');c.emit('08800004');c.branch('6000','agent15_done')
 c.label('password16_pad');c.emit('0c390002');c.address(0xffff0015);c.branch('6600','password16_map');c.emit('3200024100f00c4100f0');c.branch('6700','password16_ready');c.emit('004000f0');c.branch('6000','front14_store')
 c.label('password16_ready');byte(0xffff0015,255)
 c.label('password16_map');c.emit('3200024100700c410070');c.branch('6700','password16_done');c.emit('08800004')
 c.label('password16_done');c.emit('00400060');c.branch('6000','front14_store')
 hook(old['front_pad'],old['front_pad']+6,'front14')
 # Render toggles. Disabling band draws exactly the same complete wall.
 c.label('wall_depth14');tst(FLAGS['dither_off']);c.branch('6700','wall_depth14_pattern')
 c.emit('e04f0c470025');c.branch('6300','solid14_ok');c.emit('3e3c0025')
 c.label('solid14_ok');c.abs('45f9',0xe4aa);c.emit('1e327000');c.abs('33c7',0xffff2690);c.jump(0xe4d0)
 c.label('wall_depth14_pattern');c.emit(rom[old['wall_depth']:old['wall_depth']+6].hex());c.jump(old['wall_depth']+6)
 hook(old['wall_depth'],old['wall_depth']+6,'wall_depth14')
 c.label('wall_band14');tst(FLAGS['stripe_off']);c.branch('6700','wall_band14_on');c.jump(c.labels['wall_depth14'])
 c.label('wall_band14_on');c.emit(rom[old['wall_with_band']:old['wall_with_band']+8].hex());c.jump(old['wall_with_band']+8)
 hook(old['wall_with_band'],old['wall_with_band']+8,'wall_band14')
 # Block reductions only. Preserve the condition flags of testing unchanged value.
 for name,flag,addr,end,testhex in [
  ('energy_weight','energy',0x322a,0x3230,'4a79ffff2a2a'),('energy_tick','energy',0x32cc,0x32d2,'4a79ffff2a2a'),
  ('energy_psi','energy',0xa914,0xa91c,'4a79ffff2a2a'),
  *[(f'battery_{a:x}','battery',a,a+6,'4a79ffff2a26') for a in [0x3262,0x3270,0x328e,0x329e,0x762e,0x86ae]],
  ('weapon_charge','battery',0xa752,0xa758,'4a79ffff2a2e')]:
  c.label(name);tst(FLAGS[flag]);c.branch('6600',name+'_skip')
  if name=='energy_psi':tst(FLAGS['battery']);c.branch('6600',name+'_skip')
  c.emit(rom[addr:end].hex());c.jump(end)
  c.label(name+'_skip');c.emit(testhex);c.jump(end);hook(addr,end,name)
 c.label('damage14');tst(FLAGS['invincible']);c.branch('6700','damage14_native');c.emit('4e75')
 c.label('damage14_native');c.emit('323c0006');c.call(0x724e);c.jump(0xad06);hook(0xacfe,0xad06,'damage14')
 # Queue native stop patterns for both sound paths. Driver consumes on VBlank.
 c.label('sound_stop14');word(STATE+34,1);word(0xffff7d2c,1);word(0xffff7d46,256);c.abs('4239',0xffff7d3c);c.emit('4e75')
 c.label('sound_play14');c.abs('3039',SOUND);c.branch('6700','sound14_done')
 c.emit('e548');c.emit('41f9');c.fix.append((len(c.b),('absolute','sound_table')));c.address(0);c.emit('d0c0301052404a680002');c.branch('6600','sound14_fx')
 c.abs('33c0',0xffff7d2c);c.abs('33c0',STATE+34);c.branch('6000','sound14_queued')
 c.label('sound14_fx');c.abs('33c0',0xffff7d46)
 c.label('sound14_queued');c.abs('4239',0xffff7d3c)
 c.label('sound14_done');c.emit('4e75')
 # Two front-end menus share the same generated navigation and rendering rules.
 option_entries=[('music',0xffff2710,True,'music'),('sound fx',0xffff2711,True,'flag'),('sound test',None,False,'sound'),('wall dithering',None,False,'dither'),('wall stripe',FLAGS['stripe_off'],True,'flag'),('exit',None,False,'exit')]
 cheat_entries=[('infinite energy',FLAGS['energy'],False,'flag'),('infinite battery',FLAGS['battery'],False,'flag'),('invincibility',FLAGS['invincible'],False,'flag'),('auto sleep',FLAGS['autosleep'],False,'flag'),('access level',None,False,'access'),('exit',None,False,'exit')]
 for menu,title,entries in [('options14','options',option_entries),('cheats31','cheats',cheat_entries)]:
  def lab(s):return menu+'_'+s
  c.label(menu);c.call(c.labels['settings_init']);c.abs('4279',0xffff286a);c.abs('50f9',0xffff2702);c.call(0x1646);c.abs('4239',0xffff2712)
  c.emit('323c1000343ce000');c.call(0x31b0);c.abs('4df9',0xc00000);c.emit('7000');c.call(0x1602)
  c.abs('4279',0xffff4416);byte(0xffff0015,2);word(0xffff29ce,360);c.branch('6100',lab('draw'));word(0xffff286a,0xeee);c.abs('50f9',0xffff2702);c.call(0x1646)
  c.label(lab('loop'));c.call(0x2930);c.call(0x53a8);c.abs('3839',0xffff0006);c.emit('32004641c841');c.branch('6700',lab('loop'))
  c.emit('08040007');c.branch('6600',lab('start_exit'));c.abs('3239',0xffff4416)
  c.emit('08040000');c.branch('6700',lab('down'));c.emit('5341');c.branch('6a00',lab('selected'));c.emit('7205');c.branch('6000',lab('selected'))
  c.label(lab('down'));c.emit('08040001');c.branch('6700',lab('action'));c.emit('52410c410006');c.branch('6d00',lab('selected'));c.emit('7200')
  c.label(lab('selected'));c.abs('33c1',0xffff4416);c.branch('6000',lab('redraw'))
  c.label(lab('action'))
  for idx,(_,flag,inverse,kind) in enumerate(entries):
   c.emit('0c41'+f'{idx:04x}');c.branch('6600',lab('next'+str(idx)))
   if kind in ['flag','music']:
    c.emit('0244007c');c.branch('6700',lab('loop'));toggle(flag)
    if kind=='music':c.branch('6100','music21_toggle')
   elif kind=='dither':c.branch('6100','dither19_change')
   elif kind=='access':c.branch('6100','access31_change')
   elif kind=='sound':
    c.emit('08040002');c.branch('6700',lab('sound_right'));c.abs('3039',SOUND);c.emit('5340');c.branch('6a00',lab('sound_store'));c.emit('303c'+f'{len(SOUND_COMMANDS)-1:04x}');c.branch('6000',lab('sound_store'))
    c.label(lab('sound_right'));c.emit('08040003');c.branch('6700',lab('sound_play'));c.abs('3039',SOUND);c.emit('52400c40'+f'{len(SOUND_COMMANDS):04x}');c.branch('6d00',lab('sound_store'));c.emit('7000')
    c.label(lab('sound_store'));c.abs('33c0',SOUND);c.call(c.labels['sound_stop14']);c.branch('6000',lab('redraw'))
    c.label(lab('sound_play'));c.emit('08040004');c.branch('6700',lab('loop'));c.call(c.labels['sound_play14'])
   elif kind=='exit':
    c.emit('08040004');c.branch('6700',lab('loop'));c.branch('6000',lab('exit'))
   c.branch('6000',lab('redraw'));c.label(lab('next'+str(idx)))
  c.branch('6000',lab('loop'))
  c.label(lab('start_exit'));word(0xffff4416,5);c.branch('6100',lab('draw'))
  c.label(lab('exit'));word(0xffff7d46,256);c.abs('4239',0xffff7d3c);byte(0xffff0015,2);c.jump(0x6dc)
  if menu=='options14':c.label('opt14_redraw')
  c.label(lab('redraw'));c.branch('6100',lab('draw'));c.branch('6000',lab('loop'))
  c.label(lab('draw'));drawtext(title.ljust(16),0xe0a0)
  for idx,(text,flag,inverse,kind) in enumerate(entries):
   addr=0xe20e+idx*0x100;drawtext(text.ljust(24),addr)
   if flag:
    tst(flag);c.branch('6600',lab('flag'+str(idx)));drawtext('on ' if inverse else 'off',addr+38);c.branch('6000',lab('flagend'+str(idx)));c.label(lab('flag'+str(idx)));drawtext('off' if inverse else 'on ',addr+38);c.label(lab('flagend'+str(idx)))
   if kind=='dither':
    c.branch('6100','dither19_index');c.emit('3200d040d041');stringptr('dither19_names');c.emit('dac0363c'+f'{addr+38:04x}'+'7e023c3c2000');c.call(0xffbe)
   if kind=='access':
    c.emit('7000');c.abs('1039',FLAGS['all_access']);c.emit('0640003013c0');c.address(STATE+15);c.abs('4bf9',STATE+15);c.emit('363c'+f'{addr+38:04x}'+'7e003c3c2000');c.call(0xffbe)
   if kind=='sound':
    c.emit('7000');c.abs('3039',SOUND);c.emit('80fc000a0640003013c0');c.address(STATE+12);c.emit('48400640003013c0');c.address(STATE+13);c.abs('4bf9',STATE+12);c.emit('363c'+f'{addr+38:04x}'+'7e013c3c2000');c.call(0xffbe)
  c.abs('3039',0xffff4416);c.emit('e948064000a0');c.abs('33c0',0xffff29c8);c.call(0xf7b2);c.emit('4e75')
 # Shared bounded access change. D0 supplies the current level; front-end uses configured level.
 c.label('access31_change');c.emit('7000');c.abs('1039',FLAGS['all_access'])
 c.label('access31_value');c.emit('08040002');c.branch('6700','access31_right');c.emit('4a40');c.branch('6700','access31_done');c.emit('5340');c.branch('6000','access31_store')
 c.label('access31_right');c.emit('08040003');c.branch('6700','access31_done');c.emit('0c400007');c.branch('6400','access31_done');c.emit('5240')
 c.label('access31_store');c.abs('13c0',FLAGS['all_access']);c.emit('eb48');c.abs('33c0',0xffff26bc)
 c.label('access31_done');c.emit('4e75')
 c.label('opt14_password');c.abs('4239',STATE+36);c.call(c.labels['sound_stop14']);c.abs('4df9',0xc00000);c.emit('303c00a8');c.call(0x1602);c.call(0xa8c);byte(0xffff0015,2);c.jump(0xc36)
 # Both references to old options are redirected; old password retry remains native.
 hook(0x91e,0x924,'options14')
 # Alternate exact title logo tiles/map/palette from the European ROM.
 assets=0x190000
 corp_tiles=corp[0x34ada:0x35cdc];corp_map=corp[0x35cdc:0x36cdc];corp_pal=corp[0x27d0:0x27f0]
 assert len(corp_tiles)==2+int.from_bytes(corp_tiles[:2],'big')
 assert source[0x31118:0x34ada]==corp[0x31118:0x34ada]
 r[assets:assets+len(corp_tiles)]=corp_tiles
 mapaddr=assets+len(corp_tiles);r[mapaddr:mapaddr+4096]=corp_map
 paladdr=mapaddr+4096;r[paladdr:paladdr+32]=corp_pal
 c.label('title14_begin');tst(0xffff0014);c.branch('6700','title14_asset');toggle(STATE+9)
 c.label('title14_asset');c.abs('41f9',0x31118);c.jump(0x500);hook(0x4fa,0x500,'title14_begin')
 for tag,regop,original,alternative,sites in [
  ('logo14_tiles','41f9',0x34ada,assets,[0x50c]),('logo14_map','41f9',0x34f7c,mapaddr,[0x590,0x6f6]),
  ('logo14_pal','43f9',0x27d0,paladdr,[0x14d6,0x1506,0x15e6])]:
  for site in sites:
   label=tag+f'_{site:x}';c.label(label);c.abs(regop,original);tst(STATE+9);c.branch('6600',label+'_done');c.abs(regop,alternative)
   c.label(label+'_done');c.jump(site+6);hook(site,site+6,label)
 c.label('logo14_length');tst(STATE+9);c.branch('6600','logo14_length_cyber');c.abs('d279',assets);c.jump(0x538)
 c.label('logo14_length_cyber');c.abs('d279',0x34ada);c.jump(0x538);hook(0x532,0x538,'logo14_length')
 # Start Game submenu cursor: to the right of the 20-character labels.
 assert r[0x83e:0x844]==bytes.fromhex('317c01500006')
 r[0x840:0x842]=(368).to_bytes(2,'big')
 # Native maximum security access, applied after new-game/password setup.
 c.label('access15_init');c.abs('4279',STATE+16);c.abs('4239',STATE+20);tst(FLAGS['all_access']);c.branch('6700','access15_native')
 c.emit('7000');c.abs('1039',FLAGS['all_access']);c.emit('eb48');c.abs('33c0',0xffff26bc);c.jump(0x1fe6)
 c.label('access15_native');tst(0xffff2712);c.jump(0x1fce);hook(0x1fc8,0x1fce,'access15_init')
 # A/C alias B locally only on an external object's UI node (IDs > 8).
 # Physical button RAM remains untouched: movement, jump, fire and inventory retain their controls.
 c.label('object15_input');c.abs('3039',0xffff0006);c.abs('3239',0xffff0004)
 c.abs('2279',0xffff202a);c.emit('0c6900080002');c.branch('6f00','object15_native')
 for reg,op,bc in [('d0','3400','08800004'),('d1','3401','08810004')]:
  c.emit(op+'024200700c420070');c.branch('6700','object15_'+reg+'_released');c.emit(bc)
  c.label('object15_'+reg+'_released')
 c.label('object15_native');c.emit('3e01');c.jump(0x53f8);hook(0x53ea,0x53f8,'object15_input')
 # Successful quick pickup: remember selected broken item after native inventory compaction.
 c.label('pickup15');c.abs('4279',STATE+16);byte(STATE+20,1);c.call(0x6ace)
 c.emit('0c390002');c.address(STATE+20);c.branch('6600','pickup15_done')
 c.abs('3039',0xffff2740);c.abs('43f9',0xffff2f50);c.emit('1231000008010006');c.branch('6700','pickup15_done')
 c.abs('13c1',STATE+18);c.emit('5240');c.abs('33c0',STATE+16)
 c.label('pickup15_done');c.abs('4239',STATE+20);c.emit('4e75')
 # Only change quick-interact's final jump; ordinary inventory pickup remains native.
 q=old['quick_pickup'];j=rom.index(bytes.fromhex('4ef900006ace'),q,q+64)
 r[j+2:j+6]=c.labels['pickup15'].to_bytes(4,'big')
 c.label('pickup15_success');c.abs('33c7',0xffff2740);tst(STATE+20);c.branch('6700','pickup15_success_done');byte(STATE+20,2)
 c.label('pickup15_success_done');c.jump(0x6af8);hook(0x6af2,0x6af8,'pickup15_success')
 # Forget the pending repair selection as soon as another inventory slot is selected.
 c.label('selection15');c.abs('33c1',0xffff2740);c.emit('2f00');c.abs('3039',STATE+16);c.branch('6700','selection15_done')
 c.emit('5340b041');c.branch('6700','selection15_done');c.abs('4279',STATE+16)
 c.label('selection15_done');c.emit('201f');c.jump(0x6ed4);hook(0x6ece,0x6ed4,'selection15')
 # Perform the focus change before the usual cursor validation/redraw on Start.
 c.label('start15');toggle(0xffff270a);tst(0xffff270a);c.branch('6700','start15_done')
 c.emit('48e7c080');c.abs('3039',STATE+16);c.branch('6700','start15_restore');c.abs('4279',STATE+16)
 c.emit('5340');c.abs('b079',0xffff2740);c.branch('6600','start15_restore')
 c.emit('0cb900002106');c.address(0xffff26b8);c.branch('6600','start15_restore')
 c.abs('41f9',0xffff2f50);c.emit('12300000');c.abs('b239',STATE+18);c.branch('6600','start15_restore')
 c.emit('08010006');c.branch('6700','start15_restore')
 c.emit('23fc0000566c');c.address(0xffff202a)
 c.label('start15_restore');c.emit('4cdf0103')
 c.label('start15_done');c.jump(0x5392);hook(0x538a,0x5392,'start15')

 # Clear full text plane for password (native only cleared 0x700 bytes).
 r[0xc56:0xc58]=(0x1000).to_bytes(2,'big')
 c.label('password16_confirm');c.emit('08000007');c.branch('6600','password16_native')
 c.abs('3039',0xffff0006);c.emit('08000007');c.branch('6700','password16_wait')
 c.call(0xe94);c.jump(0xcea)
 c.label('password16_wait');c.jump(0xcea)
 c.label('password16_native');c.emit('08000004');c.branch('6600','password19_direction');c.jump(0xd3c)
 c.label('password19_direction');c.jump(0xd42)
 hook(0xd36,0xd3c,'password16_confirm')
 # Three-choice Start Game submenu, native actions and font.
 c.label('start16_menu');c.abs('4279',0xffff286a);c.abs('50f9',0xffff2702);c.call(0x1646)
 c.emit('323c1000343ce000');c.call(0x31b0);c.abs('4df9',0xc00000);c.emit('303c00a8');c.call(0x1602)
 drawtext('default character',0xe212);drawtext('select new character',0xe312);drawtext('back',0xe412)
 c.abs('4279',0xffff4416);word(0xffff29ce,368);byte(0xffff0015,2)
 c.branch('6100','start16_cursor');word(0xffff286a,0xeee);c.abs('50f9',0xffff2702);c.call(0x1646)
 c.label('start16_loop');c.call(0x2930);c.call(0x53a8);c.abs('3839',0xffff0006);c.emit('32004641c841');c.branch('6700','start16_loop');c.abs('3239',0xffff4416)
 c.emit('08040000');c.branch('6700','start16_down');c.emit('5341');c.branch('6a00','start16_changed');c.emit('7202');c.branch('6000','start16_changed')
 c.label('start16_down');c.emit('08040001');c.branch('6700','start16_confirm');c.emit('52410c410003');c.branch('6d00','start16_changed');c.emit('7200')
 c.label('start16_changed');c.abs('33c1',0xffff4416);c.branch('6100','start16_cursor');c.branch('6000','start16_loop')
 c.label('start16_confirm');c.emit('08040004');c.branch('6700','start16_loop');byte(0xffff0015,2);c.emit('4a41');c.branch('6700','start16_default');c.emit('0c410001');c.branch('6700','start16_custom');c.jump(0x6dc)
 c.label('start16_default');c.jump(0xa56)
 c.label('start16_custom');c.jump(0xa2e)
 c.label('start16_cursor');c.abs('3039',0xffff4416);c.emit('e948064000f8');c.abs('33c0',0xffff29c8);c.call(0xf7b2);c.emit('4e75')
 hook(0x81e,0x824,'start16_menu')


 # Sleep overlay: own framebuffer, actual VBlank timer, no changes to game state.
 ACTIVE=STATE+24;SEL=STATE+25;STAMP=STATE+26
 c.label('sleep16_enter');word(STATE+92,65535);c.abs('33c0',0xffff20e6);c.abs('4279',ACTIVE);byte(STATE+28,1);c.emit('4e75');hook(0x7062,0x7068,'sleep16_enter')
 c.label('sleep16_wake');c.abs('4279',ACTIVE);c.abs('41f9',0xdfc0);c.call(0xdf6e);c.jump(0x70a2);hook(0x709a,0x70a2,'sleep16_wake')
 c.label('sleep16');tst(STATE+28);c.branch('6700','sleep16_armed');c.abs('3039',0xffff0004);c.emit('024000700c400070');c.branch('6600','sleep16_dots');c.abs('4239',STATE+28)
 c.label('sleep16_armed');c.abs('3839',0xffff0006);c.abs('3039',0xffff0004);c.emit('4640c8400244007f')
 tst(ACTIVE);c.branch('6600','sleep16_active');c.emit('02440070');c.branch('6700','sleep16_dots')
 byte(ACTIVE,1);byte(SEL,0);c.branch('6000','sleep16_changed')
 c.label('sleep16_active');c.emit('4a44');c.branch('6600','sleep16_input')
 c.abs('3039',0xffff2798);c.abs('9079',STAMP)
 c.emit('323c012c');c.emit('0839000600a10001');c.branch('6700','sleep16_ntsc');c.emit('323c00fa')
 c.label('sleep16_ntsc');c.emit('b041');c.branch('6500','sleep16_show');c.abs('4239',ACTIVE);c.branch('6000','sleep16_dots')
 c.label('sleep16_input');c.emit('7000');c.abs('1039',SEL);c.emit('08040000');c.branch('6700','sleep16_down');c.emit('5340');c.branch('6a00','sleep31_up_ok');c.emit('7008');c.label('sleep31_up_ok');c.abs('13c0',SEL);c.branch('6000','sleep16_changed')
 c.label('sleep16_down');c.emit('08040001');c.branch('6700','sleep16_toggle');c.emit('52400c400009');c.branch('6d00','sleep31_down_ok');c.emit('7000');c.label('sleep31_down_ok');c.abs('13c0',SEL);c.branch('6000','sleep16_changed')
 c.label('sleep16_toggle');c.emit('0c400004');c.branch('6c00','sleep31_toggle');c.emit('0244007c');c.branch('6700','sleep16_show');c.emit('0c400002');c.branch('6600','sleep19_other');c.branch('6100','dither19_change');c.branch('6000','sleep16_changed');c.label('sleep19_other')
 for idx,addr in enumerate([0xffff2710,0xffff2711,FLAGS['dither_off'],FLAGS['stripe_off']]):
  c.emit('0c40'+f'{idx:04x}');c.branch('6600',f'sleep16_next{idx}');toggle(addr)
  if idx==0:
   c.branch('6100','music21_toggle')
  c.branch('6000','sleep16_changed');c.label(f'sleep16_next{idx}')
 c.label('sleep31_toggle');c.emit('0c400008');c.branch('6700','sleep31_access');c.emit('0244007c');c.branch('6700','sleep16_show')
 for idx,key in enumerate(['energy','battery','invincible','autosleep'],4):
  c.emit('0c40'+f'{idx:04x}');c.branch('6600','sleep31_next'+str(idx));toggle(FLAGS[key]);c.branch('6000','sleep16_changed');c.label('sleep31_next'+str(idx))
 c.branch('6000','sleep16_show')
 c.label('sleep31_access');c.abs('3039',0xffff26bc);c.emit('ea48');c.branch('6100','access31_value');c.branch('6000','sleep16_changed')
 c.label('sleep16_changed');c.emit('33f9');c.address(0xffff2798);c.address(STAMP);c.call(0) # resolved after draw definition
 sleep_draw_fix=len(c.b)-4
 c.label('sleep16_show');c.call(0x2930);c.emit('4eb9');c.fix.append((len(c.b),('absolute','sleep33_bar')));c.address(0);c.call(0x4d18);c.jump(0x7088)
 c.label('sleep16_dots');c.abs('41f9',0xdfc8);c.call(0xdf6e);c.jump(0x7078)
 hook(0x7070,0x7078,'sleep16')
 c.label('sleep16_draw');c.b[sleep_draw_fix:sleep_draw_fix+4]=c.labels['sleep16_draw'].to_bytes(4,'big');c.emit('0c390004');c.address(SEL);c.branch('6400','sleep31_draw')
 c.emit('7000')
 for idx,addr in enumerate([0xffff2710,0xffff2711,FLAGS['dither_off'],FLAGS['stripe_off']]):
  tst(addr);c.branch('6700',f'sleep16_bit{idx}');c.emit('0040'+f'{1<<idx:04x}');c.label(f'sleep16_bit{idx}')
 c.emit('c0fc3000');c.abs('41f9',0x1a0000);c.emit('d1c0');c.abs('43f9',0xffff8934);c.emit('3e3c0bff')
 c.label('sleep16_copy');c.emit('22d8');c.branch('51cf','sleep16_copy');c.branch('6100','dither19_sleep_text')
 # Arrow uses the exact original title-menu six tiles, recolored to sleep palette.
 c.label('sleep31_arrow');c.emit('7000');c.abs('1039',SEL);c.emit('0c400004');c.branch('6500','sleep31_arrow_normal');c.emit('5940ed48064001e0');c.branch('6000','sleep31_arrow_ready');c.label('sleep31_arrow_normal');c.emit('ed48');c.label('sleep31_arrow_ready');c.abs('43f9',0xffff8934);c.emit('d2c0')
 c.abs('41f9',0x1d0000);c.emit('3e3c0000');arrow_count_fix=len(c.b)-2
 c.label('sleep16_arrow');c.emit('30183218e04913810000');c.branch('51cf','sleep16_arrow');c.emit('4e75')
 # Pre-render sixteen four-line screens with the game's own 8x8 font.
 def putpixel(buf,x,y,value):
  off=x//8*512+y*4+x%8//2
  if x%2:buf[off]=(buf[off]&240)|value
  else:buf[off]=(buf[off]&15)|(value<<4)
 def textpixels(buf,text,x,y):
  for n,ch in enumerate(text):
   tile=0 if ch==' ' else (ord(ch)-21 if ch.isdigit() else ord(ch)-96)
   for yy in range(8):
    for xx in range(8):
     v=source[0x30716+tile*32+yy*4+xx//2]>>(0 if xx%2 else 4)&15
     if v:putpixel(buf,x+n*8+xx,y+yy,15)
 for bits in range(16):
  buf=bytearray(0x3000)
  for idx,title in enumerate(['music','sound fx','wall dithering','wall stripe']):
   textpixels(buf,title,8,32+idx*16)
   if idx!=2:textpixels(buf,'off' if bits&(1<<idx) else 'on',128,32+idx*16)
  r[0x1a0000+bits*0x3000:0x1a0000+(bits+1)*0x3000]=buf
 # Base arrow is at x=160,y=32, matching the native text/sprite origin; selection adds 16 rows (64 framebuffer bytes).
 arrow={}
 for x in range(24):
  for y in range(16):
   tile=20+x//8*2+y//8
   v=source[0x8e4fc+tile*32+(y%8)*4+(x%8)//2]>>(0 if x%2 else 4)&15
   if v:
    xx=160+x;yy=32+y;off=xx//8*512+yy*4+xx%8//2
    arrow[off]=arrow.get(off,0)|({4:11,5:12,6:13,7:15}[v]<<(0 if xx%2 else 4))
 data=b''.join(off.to_bytes(2,'big')+bytes([value,0]) for off,value in sorted(arrow.items()))
 r[0x1d0000:0x1d0000+len(data)]=data;c.b[arrow_count_fix:arrow_count_fix+2]=(len(arrow)-1).to_bytes(2,'big')


 # Second sleep page: one immutable background plus small value overlays.
 c.label('sleep31_draw');c.abs('41f9',0x1d1000);c.abs('43f9',0xffff8934);c.emit('3e3c0bff')
 c.label('sleep31_copy');c.emit('22d8');c.branch('51cf','sleep31_copy')
 for idx,key in enumerate(['energy','battery','invincible','autosleep']):
  c.abs('41f9',0x1d4000);tst(FLAGS[key]);c.branch('6700','sleep31_off'+str(idx));c.emit('d0fc0180');c.label('sleep31_off'+str(idx));c.abs('43f9',0xffff8934+idx*64);c.emit('3e3c005f');c.branch('6100','sleep31_value_copy')
 c.abs('3039',0xffff26bc);c.emit('ea4802400007ef48');c.abs('41f9',0x1d5000);c.emit('d0c0');c.abs('43f9',0xffff8934+4*64);c.emit('7e1f');c.branch('6100','sleep31_value_copy');c.branch('6000','sleep31_arrow')
 c.label('sleep31_value_copy');c.emit('30183218e04913810000');c.branch('51cf','sleep31_value_copy');c.emit('4e75')
 buf=bytearray(0x3000)
 for idx,title in enumerate(['infinite energy','infinite battery','invincibility','auto sleep','access level']):textpixels(buf,title,8,24+idx*16)
 r[0x1d1000:0x1d4000]=buf
 def value_patch(text,width):
  buf=bytearray(0x3000);textpixels(buf,text,144,24)
  offsets=sorted({x//8*512+y*4+x%8//2 for x in range(144,144+width) for y in range(24,32)})
  return b''.join(off.to_bytes(2,'big')+bytes([buf[off],0]) for off in offsets)
 for idx,text in enumerate(['off','on ']):r[0x1d4000+idx*384:0x1d4000+(idx+1)*384]=value_patch(text,24)
 for idx in range(8):r[0x1d5000+idx*128:0x1d5000+(idx+1)*128]=value_patch(str(idx),8)

 # Byte-aligned edges of the selected 2x2 pattern: write only covered bytes.
 # No visibility changes, no per-pixel clipping changes. Original path for others.
 c.label('column16');tst(STATE+32);c.branch('6700','column19_four');c.emit('0c390002');c.address(STATE+32);c.branch('6700','column19_8');c.branch('6000','column16_native');c.label('column19_four');c.emit('4a81');c.branch('6700','column16_native')
 for startbyte,endbyte in [(3,4),(0,1),(2,4),(0,2),(1,3),(1,4),(0,3),(1,2),(2,3)]:
  mask=0xffffffff ^ (((1<<((endbyte-startbyte)*8))-1)<<((4-endbyte)*8))
  c.emit('0c81'+f'{mask:08x}');c.branch('6700',f'col16_{startbyte}_{endbyte}')
 c.label('column16_native');c.emit(rom[old['pattern_column']:old['pattern_column']+6].hex());c.jump(old['pattern_column']+6)
 for startbyte,endbyte in [(3,4),(0,1),(2,4),(0,2),(1,3),(1,4),(0,3),(1,2),(2,3)]:
  tag=f'col16_{startbyte}_{endbyte}';c.label(tag);c.emit('4cd4003c3c00e44e');c.branch('6700',tag+'_tail');c.emit('5346');c.label(tag+'_loop')
  def emitrow(reg):
   pos=startbyte
   while pos<endbyte:
    wordstore=pos%2==0 and endbyte-pos>=2
    opcode=(0x3740 if wordstore else 0x1740)|reg
    c.emit(f'{opcode:04x}{pos:04x}');pos+=2 if wordstore else 1
   c.emit('588b') # addq.l #4,a3
  for reg in range(2,6):emitrow(reg)
  c.branch('51ce',tag+'_loop');c.label(tag+'_tail');c.emit('3c0002460003');c.branch('6700',tag+'_done')
  for reg in range(2,5):
   emitrow(reg)
   if reg<4:c.emit('5346');c.branch('6700',tag+'_done')
  c.label(tag+'_done');c.emit('4e75')
 hook(old['pattern_column'],old['pattern_column']+6,'column16')


 # Mode enters exactly the inventory sleep state, with its normal cursor.
 c.label('sleep17_begin');c.emit('4eb9');c.fix.append((len(c.b),('absolute','name32_before_sleep')));c.address(0);c.abs('50f9',0xffff270a);c.emit('23fc0000561c');c.address(0xffff202a);c.call(0x540a);c.call(0xf7b2);c.abs('50f9',0xffff26e2);c.jump(0x6fb8);hook(0x6fb2,0x6fb8,'sleep17_begin')
 # DIVS overflow leaves the original dividend unchanged on 68000. Saturate
 # only that exceptional path, keeping the side of the screen correct.
 c.label('project17');c.emit(rom[0x4c86:0x4cea].hex())
 for reg,div,bias in [(2,'85c7',96),(1,'83c7',70),(6,'8dc7',70)]:
  c.emit(div);c.branch('6800',f'project17_r{reg}_ok');c.emit(f'{0x4a80|reg:04x}');c.branch('6b00',f'project17_r{reg}_neg');c.emit(f'{0x303c|(reg<<9):04x}7f00');c.branch('6000',f'project17_r{reg}_ok');c.label(f'project17_r{reg}_neg');c.emit(f'{0x303c|(reg<<9):04x}8100');c.label(f'project17_r{reg}_ok')
  c.emit(f'{0x0640|reg:04x}{bias:04x}');c.branch('6800',f'project17_r{reg}_bias');c.emit(f'{0x303c|(reg<<9):04x}{0x7f00+bias:04x}');c.label(f'project17_r{reg}_bias')
  if reg==2:c.emit(rom[0x4cf0:0x4cf4].hex())
 c.emit(rom[0x4d00:0x4d08].hex())
 hook(0x4c86,0x4c8c,'project17')
 # SRAM stores the original 24-character password, not a savestate.
 r[0x1b0:0x1bc]=bytes.fromhex('5241f8200020000100203fff')
 c.label('save17_hook');c.call(0x8faa);c.call(0);savefix=len(c.b)-4;c.abs('4bf9',0xffff25b4);c.jump(0x8f96);hook(0x8f8c,0x8f96,'save17_hook')
 c.label('sram17_save');c.b[savefix:savefix+4]=c.labels['sram17_save'].to_bytes(4,'big');c.emit('48e7fffe');byte(0xa130f1,1)
 c.abs('41f9',0x200001);c.emit('4210');c.abs('43f9',0xffff25b4);c.emit('45e8000874007e17')
 c.label('sram17_write');c.emit('70001019d4401480544a');c.branch('51cf','sram17_write')
 c.emit('3002e0481480544a1482')
 for off,v in [(2,ord('C')),(4,ord('1')),(6,ord('7')),(0,ord('C'))]:c.emit('117c'+f'{v:04x}{off:04x}')
 byte(0xa130f1,0);c.emit('4cdf7fff4e75')
 c.label('sram17_load');c.emit('48e77ffe');byte(0xa130f1,1);c.abs('41f9',0x200001)
 for off,v in [(0,ord('C')),(2,ord('C')),(4,ord('1')),(6,ord('7'))]:c.emit('0c28'+f'{v:04x}{off:04x}');c.branch('6600','sram17_invalid')
 c.emit('41e80008');c.abs('43f9',0xffff2580);c.emit('74007e0b')
 c.label('sram17_read')
 for lo,hi in [(97,112),(107,122)]:
  c.emit('7000101054480c00'+f'{lo:04x}');c.branch('6500','sram17_invalid');c.emit('0c00'+f'{hi:04x}');c.branch('6200','sram17_invalid');c.emit('12c0d440')
 c.branch('51cf','sram17_read');c.emit('70001010e14810280002b042');c.branch('6600','sram17_invalid');c.emit('7001');c.branch('6000','sram17_return')
 c.label('sram17_invalid');c.emit('7000')
 c.label('sram17_return');byte(0xa130f1,0);c.emit('4cdf7ffe4a404e75')
 c.label('resume17');c.call(c.labels['sram17_load']);c.branch('6700','resume17_empty');c.call(c.labels['sound_stop14']);c.abs('4df9',0xc00000);c.emit('303c00a8');c.call(0x1602);word(0xffff257e,24);byte(0xffff0015,2);c.jump(0xe94)
 c.label('resume17_empty');drawtext('no saved game'.ljust(20),0xe014)
 c.emit('323c0064');c.call(0x7994)
 drawtext(' '*20,0xe014);word(0xffff0008,2500);c.branch('6000','main18_loop')

 # The native wall filler assumes vertically overlapping end edges. A thin
 # sloping stripe violates that assumption. Rasterize the stripe by columns.
 c.label('band17');c.abs('43f9',0xffff2458);c.emit('30290002b069000e');c.branch('6d00','band17_slow');c.emit('30290006b069000a');c.branch('6d00','band17_slow');c.jump(0xe4d0)
 c.label('band17_slow');c.emit('48e7fffe');c.abs('4df9',0xffff2458)
 c.emit('3016322e0004b041');c.branch('6f00','band17_ordered')
 c.emit('2016222e00042c812d400004202e0008222e000c2d4100082d40000c')
 c.label('band17_ordered');c.emit('3016322e00040c4000bf');c.branch('6e00','band17_done');c.emit('4a41');c.branch('6b00','band17_done');c.emit('b041');c.branch('6700','band17_vertical')
 # E276 calculates signed 16.16 slope, and adds one to its denominator.
 for top,bot in [(2,6),(10,14)]:
  c.emit('7600362e'+f'{bot:04x}'+'966e'+f'{top:04x}'+'380198405344');c.call(0xe276)
  if top==2:c.emit('2f04')
 c.emit('2a04281f');c.branch('6000','band17_initial')
 c.label('band17_vertical');c.emit('78007a00')
 c.label('band17_initial');c.emit('342e000248c248424242362e000a48c3484342434a40');c.branch('6a00','band17_left')
 c.emit('3c004446')
 for stepreg,outreg in [(4,2),(5,3)]:
  c.emit(f'{0x2e00|stepreg:04x}'+'cec62f07'+f'{0x2e00|stepreg:04x}'+'4847cec648474247de9f'+f'{0xd080|(outreg<<9)|7:04x}')
 c.emit('7000')
 c.label('band17_left');c.emit('0c4100bf');c.branch('6f00','band17_right');c.emit('323c00bf')
 c.label('band17_right');c.abs('45f9',0xffff8b30);c.emit('3c000246fff8ed4e3e0002470007e24fde46d4c7')
 c.emit('7c00');c.abs('3c39',0xffff2690);c.emit('2846') # A4=color
 c.label('band17_column');c.emit('2c0248464a46');c.branch('6b00','band17_next');c.emit('0c46007f');c.branch('6f00','band17_top');c.emit('3c3c007f')
 c.label('band17_top');c.emit('2e0348470c47007f');c.branch('6e00','band17_next');c.emit('4a47');c.branch('6a00','band17_bottom');c.emit('7e00')
 c.label('band17_bottom');c.emit('264ae54e96c6e44e9c47');c.branch('6b00','band17_next');c.emit('2e0c08000000');c.branch('6600','band17_odd');c.emit('e94f')
 c.label('band17_even_loop');c.emit('0213000f8f13588b');c.branch('51ce','band17_even_loop');c.branch('6000','band17_next')
 c.label('band17_odd');c.emit('021300f08f13588b');c.branch('51ce','band17_odd')
 c.label('band17_next');c.emit('d484d6855240b041');c.branch('6e00','band17_done');c.emit('3c0002460007');c.branch('6700','band17_boundary');c.emit('08000000');c.branch('6600','band17_column');c.emit('528a');c.branch('6000','band17_column')
 c.label('band17_boundary');c.emit('45ea01fd');c.branch('6000','band17_column')
 c.label('band17_done');c.emit('4cdf7fff4e75')
 hook(old['band_guard_above_keep'],old['band_guard_above_keep']+6,'band17')

 # Four-entry main menu. Keep native title loading, palette and background.
 c.label('main18_text')
 for idx,title in enumerate(['start new game','resume saved game','enter password','options']):drawtext(title.ljust(20),0xe212+idx*0x100)
 tst(STATE+87);c.branch('6700','main32_hidden_text');drawtext('cheats'.ljust(20),0xe612);c.branch('6000','main32_text_done');c.label('main32_hidden_text');drawtext(' '*20,0xe612);c.label('main32_text_done')
 # Main-menu plane is vertically scrolled by 168 pixels: row 16 is screen y=216.
 # Right-align the complete label, including future three-digit versions.
 drawtext(version,0xe800+2*(40-len(version)))
 c.emit('4e75');hook(0xab8,0xabe,'main18_text')
 c.label('main18_enter');c.call(c.labels['settings_init']);c.branch('6100','music20_ensure');c.abs('3039',STATE+30);c.emit('0c400004');c.branch('6300','main18_valid');c.emit('7000');c.abs('33c0',STATE+30)
 c.label('main18_valid');tst(STATE+87);c.branch('6600','main32_valid_selection');c.emit('0c790004');c.address(STATE+30);c.branch('6600','main32_valid_selection');word(STATE+30,3);c.label('main32_valid_selection');word(0xffff29ce,368);byte(0xffff0015,2);c.branch('6100','main18_cursor');c.branch('6100','intro31_show');c.abs('50f9',0xffff2702);c.call(0x1646);word(0xffff0008,2500)
 c.label('main18_loop');c.call(0x2930);c.call(0x53a8);c.abs('3839',0xffff0006);c.emit('32004641c841');c.branch('6600','main18_event')
 c.emit('5379');c.address(0xffff0008);c.branch('6600','main18_loop');c.jump(0x77a)
 c.label('main18_event');word(0xffff0008,2500);c.abs('3239',STATE+30)
 c.emit('3004024000fd');c.branch('6700','main32_count_ok');byte(STATE+88,0);c.label('main32_count_ok')
 c.emit('08040000');c.branch('6700','main18_down');c.emit('5341');c.branch('6a00','main18_changed');c.emit('7200');c.branch('6000','main18_changed')
 c.label('main18_down');c.emit('08040001');c.branch('6700','main18_confirm');tst(STATE+87);c.branch('6600','main32_down_unlocked');c.emit('0c410003');c.branch('6d00','main32_down_one');c.abs('3039',0xffff0004);c.emit('024000ff0c4000fd');c.branch('6700','main32_pure_down');byte(STATE+88,0);c.branch('6000','main18_loop');c.label('main32_pure_down');c.emit('0c440002');c.branch('6600','main18_loop');c.abs('5239',STATE+88);c.emit('0c390004');c.address(STATE+88);c.branch('6500','main18_loop');byte(STATE+87,255);byte(STATE+88,0);drawtext('cheats'.ljust(20),0xe612);c.emit('7204');c.branch('6000','main18_changed')
 c.label('main32_down_one');c.emit('5241');c.branch('6000','main18_changed')
 c.label('main32_down_unlocked');c.emit('52410c410005');c.branch('6d00','main18_changed');c.emit('7204')
 c.label('main18_changed');c.abs('33c1',STATE+30);drawtext(' '*20,0xe014);c.branch('6100','main18_cursor');c.branch('6000','main18_loop')
 c.label('main18_confirm');c.emit('08040004');c.branch('6700','main18_loop');byte(0xffff0015,2)
 for idx,label in [(0,'start16_menu'),(1,'resume17'),(2,'opt14_password'),(3,'options14'),(4,'cheats31')]:
  c.emit('0c41'+f'{idx:04x}');c.branch('6700',label)
 c.branch('6000','main18_loop')
 c.label('main18_cursor');c.abs('3039',STATE+30);c.emit('e948064000f8');c.abs('33c0',0xffff29c8);c.call(0xf7b2);c.emit('4e75')
 hook(0x73a,0x740,'main18_enter')
 # Native bad-password message and wait remain unchanged; return to main menu.
 assert r[0xf46:0xf48]==bytes.fromhex('4efa');r[0xf48:0xf4a]=(0x6dc-0xf48).to_bytes(2,'big',signed=True)
 # Successful auto-selection of the ID card also focuses its Use button.
 c.label('id18_selected');c.abs('33c1',0xffff2740);c.call(0x6e98)
 c.emit('0c79001d');c.address(0xffff21ba);c.branch('6700','id32_focus');c.emit('0cb9000087c8');c.address(0xffff26b8);c.branch('6600','id34_not_screen');c.emit('0c790019');c.address(0xffff21ba);c.branch('6500','id34_not_screen');c.emit('0c79001b');c.address(0xffff21ba);c.branch('6300','id32_focus');c.label('id34_not_screen');c.emit('0c79000c');c.address(0xffff21ba);c.branch('6600','id18_done');c.emit('0cb900009916');c.address(0xffff26b8);c.branch('6600','id18_done');c.label('id32_focus')
 c.abs('50f9',0xffff270a);c.emit('23fc000056a8');c.address(0xffff202a);c.call(0x540a);c.call(0xf7b2)
 c.label('id18_done');c.emit('70ff4e75');hook(0x8f66,0x8f74,'id18_selected')

 # Dithering choices: Off / 2x2 / 4x4 / 4x8 / vertical bars.
 # Keep old off flag and zero-initialized mode, so old saves default to 2x2.
 c.label('dither19_index');c.emit('7000');tst(FLAGS['dither_off']);c.branch('6600','dither19_index_done');c.abs('1039',STATE+32);c.emit('5240')
 c.label('dither19_index_done');c.emit('4e75')
 c.label('dither19_change');c.emit('32040241000c');c.branch('6700','dither19_index_done');c.branch('6100','dither19_index');c.emit('08040002');c.branch('6700','dither19_right');c.emit('4a40');c.branch('6700','dither19_index_done');c.emit('5340');c.branch('6000','dither19_store')
 c.label('dither19_right');c.emit('0c400004');c.branch('6400','dither19_index_done');c.emit('5240')
 c.label('dither19_store');c.emit('4a40');c.branch('6600','dither19_on');byte(FLAGS['dither_off'],255);c.emit('4e75')
 c.label('dither19_on');byte(FLAGS['dither_off'],0);c.emit('5340');c.abs('13c0',STATE+32);c.emit('4e75')
 c.label('dither19_options');c.branch('6100','dither19_change');c.branch('6000','opt14_redraw')
 c.label('dither19_sleep_text');c.branch('6100','dither19_index');c.emit('c0fc0180');c.abs('41f9',0x1d0800);c.emit('d1c0');c.abs('43f9',0xffff8934);c.emit('3e3c005f')
 c.label('dither19_text_copy');c.emit('30183218e04913810000');c.branch('51cf','dither19_text_copy');c.emit('4e75')
 names=['off','2x2','4x4','4x8','bar']
 for idx,name in enumerate(names):
  buf=bytearray(0x3000);textpixels(buf,name,128,64)
  offsets=sorted({x//8*512+y*4+x%8//2 for y in range(64,72) for x in range(128,152)})
  data=b''.join(off.to_bytes(2,'big')+bytes([buf[off],0]) for off in offsets)
  assert len(data)==384;r[0x1d0800+idx*384:0x1d0800+(idx+1)*384]=data
 c.label('dither19_select');c.emit('4a43');c.branch('6b00','dither19_pattern');c.jump(old['bayer_solid'])
 c.label('dither19_pattern');c.emit('024300ffed4b')
 for mode in range(3):
  c.emit('0c39'+f'{mode:04x}');c.address(STATE+32);c.branch('6600',f'dither19_next{mode}');c.abs('49f9',0x1e0000+mode*0x4000);c.emit('d8c34e75');c.label(f'dither19_next{mode}')
 c.abs('49f9',0x1ec000);c.emit('d8c34e75');hook(0xe146,0xe14e,'dither19_select')
 for lo,hi,was,now in [(old['bayer_span'],old['span_native'],'02430003','02430007'),(old['center_pattern'],old['pattern_column'],'0247000f','0247001f')]:
  chunk=bytes(r[lo:hi]);assert chunk.count(bytes.fromhex(was))==1;r[lo:hi]=chunk.replace(bytes.fromhex(was),bytes.fromhex(now))
 bayer=[[0,8,2,10],[12,4,14,6],[3,11,1,9],[15,7,13,5]];shades=list(source[0xe4aa:0xe4d0]);order=[0,4,2,6,1,5,3,7]
 for mode in range(4):
  table=bytearray()
  for index in range(256):
   depth=index*128;slot=min(depth//256,len(shades)-1);hi=shades[slot];first=slot;end=slot+1
   while first and shades[first-1]==hi:first-=1
   while end<len(shades) and shades[end]==hi:end+=1
   lo=shades[end] if end<len(shades) else hi;k=0 if hi==lo else min(16,(depth-first*256)*16//((end-first)*256))
   for y in range(16):
    vals=[]
    for x in range(8):
     threshold=([[0,2],[3,1]][y%2][x%2]*4 if mode==0 else bayer[y%4][x%4] if mode==1 else bayer[(y//2)%4][x%4] if mode==2 else order.index(x)*2)
     # Original stripes quantize coverage to eighths, not sixteenths.
     vals.append(lo if (threshold<k if mode!=3 else order.index(x)<k//2) else hi)
    table.extend(bytes.fromhex(''.join(format(v,'x') for v in vals)))
  assert len(table)==0x4000;r[0x1e0000+mode*0x4000:0x1e0000+(mode+1)*0x4000]=table
 # 4x8 uses four distinct rows, each repeated twice. Keep the existing fast
 # 4-row writer for the other modes; select phase using framebuffer parity.
 c.label('column19_8');c.emit('2e0b028700000004');c.branch('6700','col19_odd')
 for name,offsets,sequence in [('col19_even',[0,8,16,24],[2,2,3,3,4,4,5,5]),('col19_odd',[0,4,12,20],[2,3,3,4,4,5,5,2])]:
  c.label(name)
  for reg,off in zip(range(2,6),offsets):c.emit(f'{0x202c|(reg<<9):04x}{off:04x}')
  c.emit('4a81');c.branch('6700',name+'_full');c.emit('2e014687c487c687c887ca87')
  for typ in ['partial','full']:
   if typ=='full':c.label(name+'_full')
   c.emit('3c00e64e');c.branch('6700',name+'_'+typ+'_tail');c.emit('5346');c.label(name+'_'+typ+'_loop')
   def row(reg):
    if typ=='partial':c.emit('2e13ce81'+f'{0x8e80|reg:04x}'+'26c7')
    else:c.emit(f'{0x26c0|reg:04x}')
   for reg in sequence:row(reg)
   c.branch('51ce',name+'_'+typ+'_loop');c.label(name+'_'+typ+'_tail');c.emit('3c0002460007');c.branch('6700',name+'_'+typ+'_done')
   for j,reg in enumerate(sequence[:7]):
    row(reg)
    if j<6:c.emit('5346');c.branch('6700',name+'_'+typ+'_done')
   c.label(name+'_'+typ+'_done');c.emit('4e75')
 c.label('dither19_names');c.b.extend(''.join(names).encode('ascii'))
 if len(c.b)%2:c.emit('00')

 c.label('music20_record');c.emit('5240');c.abs('33c0',0xffff7d2c);c.abs('33c0',STATE+34);c.jump(0x150d0);hook(0x150c8,0x150d0,'music20_record')
 # Ordinary menu transitions retain an already playing/queued main theme.
 # A return from Sound Test restores it, and Music Off never queues a start.
 c.label('music20_ensure');tst(0xffff2710);c.branch('6600','music20_off')
 c.abs('3039',0xffff7d2c);c.branch('6700','music20_current');c.emit('0c400002');c.branch('6700','music20_done');c.branch('6000','music20_start')
 c.label('music20_current');c.emit('0c790002');c.address(STATE+34);c.branch('6700','music20_done')
 c.label('music20_start');c.emit('7001');c.jump(0x150b4)
 c.label('music20_off');c.abs('3039',0xffff7d2c);c.emit('0c400001');c.branch('6700','music20_done');c.emit('4a40');c.branch('6600','music20_stop');c.abs('4a79',0xffff7d30);c.branch('6700','music20_done')
 c.label('music20_stop');c.emit('7000');c.jump(0x150b4)
 c.label('music20_done');c.emit('4e75')
 # Preserve the native error sound and its wait, then restart only if enabled.
 c.label('password20_music');tst(0xffff2710);c.branch('6600','password20_quiet');c.emit('7001');c.call(0x150b4)
 c.label('password20_quiet');c.abs('4279',0xffff286a);c.jump(0xf30);hook(0xf2a,0xf30,'password20_music')

 # Music toggles must not replace an active environmental loop.
 c.label('music21_toggle');c.emit('0c790020');c.address(STATE+34);c.branch('6400','music23_toggle_done');c.emit('7001');tst(0xffff2710);c.branch('6700','music22_toggle_send');c.emit('7000')
 c.label('music22_toggle_send');c.call(0x150b4)
 c.label('music23_toggle_done');c.emit('4e75')
 # All non-theme commands are permitted. Muted theme requests stop the
 # preceding loop, as required by native alarm/lift completion handlers.
 c.label('music21_gate');tst(0xffff2710);c.branch('6700','music23_allow');c.emit('0c400001');c.branch('6600','music23_allow');c.emit('7000')
 c.label('music23_allow');c.jump(0x150c0);hook(0x150b4,0x150c0,'music21_gate')
 # Invalid Use -> previous valid icon, unless the player explicitly chose a direction.
 c.label('cursor21_fallback');c.emit('0c6900070002');c.branch('6500','cursor21_right');c.emit('0c6900080002');c.branch('6200','cursor21_right');c.emit('08870002');c.jump(0x54d8)
 c.label('cursor21_right');c.emit('08870003');c.jump(0x54d8);hook(0x5534,0x553a,'cursor21_fallback')
 # Atomic VDP control/data transaction and queue append. VBlank also writes HUD tiles.
 c.label('tile21_atomic');c.emit('40e7007c0700');c.call(c.labels['tile21_body'] if 'tile21_body' in c.labels else 0);tilefix=len(c.b)-4;c.emit('40e71eaf000246df548f4e75')
 c.label('tile21_body');c.b[tilefix:tilefix+4]=c.labels['tile21_body'].to_bytes(4,'big');c.emit(rom[0x35fe:0x3644].hex());hook(0x35fe,0x3604,'tile21_atomic')
 # Refresh the two affected HUD regions, including corruption already captured in GST files.
 c.label('hud21_refresh');c.abs('43f9',0x3440);c.abs('3839',0xffff2a2a);c.emit('0cb900007070');c.address(0xffff26b8);c.branch('6600','hud34_energy');c.emit('0c79ffff');c.address(STATE+92);c.branch('6700','hud34_energy');c.abs('3839',STATE+92);c.label('hud34_energy');c.emit('4a44');c.call(0x33ec);c.emit('48e7fffe')
 c.emit('303c1914343ce94c');c.call(0x35fe);c.call(0x3852);c.emit('4cdf7fff4e75');hook(0x33e2,0x33ec,'hud21_refresh')
 # Keep the original aggregate password damage, but never fill a vital part to its death threshold.
 c.label('health21_decode');c.emit('161d3403e24a0242007f');c.abs('41f9',0xffff2fd6);c.emit('7c09')
 c.label('health21_part');c.emit('322800020c460002');c.branch('6700','health21_vital');c.emit('4a46');c.branch('6600','health21_capacity')
 c.label('health21_vital');c.emit('5341')
 c.label('health21_capacity');c.emit('b441');c.branch('6f00','health21_last');c.emit('3141000494415188');c.branch('51ce','health21_part');c.jump(0x1192)
 c.label('health21_last');c.emit('31420004');c.jump(0x1192);hook(0x1162,0x1168,'health21_decode')
 # Clear the unused tail before rebuilding a floor's 16-entry item list.
 c.label('floor21_clear');c.emit('2f0020497e0b7000')
 c.label('floor21_zero');c.emit('20c0');c.branch('51cf','floor21_zero');c.emit('201f');c.abs('41f9',0xffff305a);c.jump(0x4a9c);hook(0x4a96,0x4a9c,'floor21_clear')
 # Extended checkpoint. Password remains at the original location for CC17 compatibility.
 # Tail: magic, length, checksum, then password binding + native state fields.
 ranges=[(0xffff25b4,24),(0xffff2a3a,768),(0xffff2718,16),(0xffff2f8e,80),(0xffff2a26,12),(0xffff2f50,52),(0xffff2740,2),(0xffff2fea,32)]
 payload=sum(n for a,n in ranges);tail=0x200041
 offsets={};pos=tail+16
 for addr,n in ranges:offsets[addr]=pos;pos+=n*2
 c.label('save21');c.emit('48e7fffe');c.abs('3f39',0xffff2608);c.emit('33f9');c.address(0xffff2606);c.address(0xffff2608);c.call(0x4a80);c.abs('33df',0xffff2608)
 c.call(c.labels['sram17_save']);byte(0xa130f1,1);c.abs('43f9',tail);c.emit('4211');c.abs('45f9',tail+16);c.emit('7400')
 for idx,(addr,n) in enumerate(ranges):
  c.abs('41f9',addr);c.emit('3e3c'+f'{n-1:04x}');c.label(f'save21_copy{idx}');c.emit('70001018d4401480544a');c.branch('51cf',f'save21_copy{idx}')
 # Checksum includes password; write magic last to reject interrupted writes.
 c.emit('3002e048');c.abs('13c0',tail+12);c.abs('13c2',tail+14)
 for off,v in [(8,payload>>8),(10,payload&255),(2,ord('2')),(4,ord('1')),(6,0x21),(0,ord('X'))]:byte(tail+off,v)
 byte(0xa130f1,0);c.emit('4cdf7fff4e75')
 # Redirect only the save call in the native ID-card password hook.
 c.b[c.labels['save17_hook']+8-base.BASE:c.labels['save17_hook']+12-base.BASE]=c.labels['save21'].to_bytes(4,'big')
 c.label('load21');c.abs('4239',STATE+50);c.abs('4239',STATE+36);c.call(c.labels['sram17_load']);c.branch('6700','load21_return');c.emit('48e7fffe');byte(0xa130f1,1);c.abs('41f9',tail);c.emit('0c100058');c.branch('6600','load21_done');byte(STATE+36,2)
 for off,v in [(0,ord('X')),(2,ord('2')),(4,ord('1')),(6,0x21)]:c.emit('0c28'+f'{v:04x}{off:04x}');c.branch('6600','load21_done')
 c.emit('700010280008e1481028000a0c40'+f'{payload:04x}');c.branch('6600','load26_old_length');byte(STATE+50,255);c.branch('6000','load26_length_ok')
 c.label('load26_old_length');c.emit('0c40'+f'{payload-32:04x}');c.branch('6600','load21_done')
 c.label('load26_length_ok');c.abs('33c0',STATE+48)
 c.abs('41f9',tail+16);c.abs('43f9',0xffff2580);c.emit('7e17')
 c.label('load21_bind');c.emit('10105448b019');c.branch('6600','load21_done');c.branch('51cf','load21_bind')
 c.abs('41f9',tail+16);c.emit('7400');c.abs('3e39',STATE+48);c.emit('5347')
 c.label('load21_sum');c.emit('700010105448d440');c.branch('51cf','load21_sum');c.abs('1039',tail+12);c.emit('e148');c.abs('1039',tail+14);c.emit('b042');c.branch('6600','load21_done');byte(STATE+36,1)
 c.label('load21_done');byte(0xa130f1,0);c.emit('4cdf7fff');c.emit('0c390002');c.address(STATE+36);c.branch('6600','load21_return');c.abs('4239',STATE+36);c.emit('7000')
 c.label('load21_return');c.emit('4a404e75')
 c.b[c.labels['resume17']+2-base.BASE:c.labels['resume17']+6-base.BASE]=c.labels['load21'].to_bytes(4,'big')
 def restore21(addr,n,tag):
  c.abs('41f9',offsets[addr]);c.abs('43f9',addr);c.emit('3e3c'+f'{n-1:04x}');c.label(tag);c.emit('12d05448');c.branch('51cf',tag)
 c.label('restore21_floor');tst(0xffff2712);c.branch('6700','restore21_floor_native');tst(STATE+36);c.branch('6700','restore21_floor_native');c.emit('48e7fffe');byte(0xa130f1,1)
 restore21(0xffff2a3a,768,'restore21_items');restore21(0xffff2f8e,80,'restore21_body');byte(0xa130f1,0);c.emit('4cdf7fff')
 c.label('restore21_floor_native');c.call(0x4832);c.emit('7000');c.jump(0x1f66);hook(0x1f60,0x1f66,'restore21_floor')
 c.label('restore21_terminal');c.call(0x2ca0);tst(0xffff2712);c.branch('6700','restore21_terminal_native');tst(STATE+36);c.branch('6700','restore21_terminal_native');c.emit('48e7fffe');byte(0xa130f1,1);restore21(0xffff2718,16,'restore21_flags');byte(0xa130f1,0);c.emit('4cdf7fff')
 c.label('restore21_terminal_native');c.call(0x33b6);c.jump(0x1fbc);hook(0x1fb4,0x1fbc,'restore21_terminal')
 c.label('restore21_late');tst(0xffff2712);c.branch('6700','restore21_late_native');tst(STATE+36);c.branch('6700','restore21_late_native');c.emit('48e7fffe');byte(0xa130f1,1)
 for idx,(addr,n) in enumerate(ranges[4:]):
  if addr==0xffff2fea:tst(STATE+50);c.branch('6700','restore26_codes_done')
  restore21(addr,n,f'restore21_exact{idx}')
 c.label('restore26_codes_done')
 byte(0xa130f1,0);c.emit('4cdf7fff');c.abs('3239',0xffff2740);c.call(0x6e98);c.branch('6000','restore21_late_end')
 c.label('restore21_late_native');c.call(0x6e86)
 c.label('restore21_late_end');tst(0xffff2712);c.branch('6700','resume25_music_done');tst(0xffff2710);c.branch('6600','resume25_music_done');c.emit('7001');c.call(0x150b4);c.label('resume25_music_done');c.abs('4239',STATE+36);c.emit('23fc00004d38');c.address(0xffff2794);c.jump(0x2074);hook(0x2066,0x2074,'restore21_late')

 # The original renderer substitutes depth 100 for a corner behind the camera.
 # Reconstruct the stripe edge through the horizontal vanishing point instead
 # of interpolating against that fictitious corner. Only affected near faces.
 c.label('band21_capture');c.emit('48e7c080');c.emit('200a9088');c.abs('33c0',STATE+38);c.abs('33c7',STATE+40);c.emit('301202407fff');c.abs('33c0',STATE+42);c.emit('4cdf0103');c.jump(c.labels['wall_band14'])
 hook(old['wall_with_band'],old['wall_with_band']+8,'band21_capture')
 c.label('band21');c.emit('48e7fffe');c.abs('43f9',0xffff2458);c.emit('4cd1000f48e7f000');c.abs('3039',STATE+40);c.emit('0c400064');c.branch('6700','band21_left_bad');c.emit('0c790064');c.address(STATE+42);c.branch('6600','band21_native');c.emit('7600');c.branch('6000','band21_fix')
 c.label('band21_left_bad');c.emit('0c790064');c.address(STATE+42);c.branch('6700','band21_both');c.emit('7604')
 c.label('band21_fix');c.abs('3039',0xffff260c);c.abs('45f9',0x11508);c.emit('32320000');c.abs('47f9',0x11608);c.emit('34330000') # D1=sin,D2=cos
 c.emit('08390003');c.address(STATE+39);c.branch('6700','band21_vector');c.emit('c3424442') # Z-axis: denominator cos, numerator -sin
 c.label('band21_vector');c.emit('4a41');c.branch('6700','band21_native');c.emit('48c2e18a85c1');c.branch('6900','band21_native');c.emit('06420060');c.branch('6900','band21_native') # D2 vanishing x
 c.emit('303130009042');c.branch('6900','band21_native');c.branch('6700','band21_native') # D0 validX-vX
 # D4 is other endpoint offset. Clip it to the screen edge in its current direction.
 c.emit('780498433a313000ba714000');c.branch('6d00','band21_to_right');c.emit('7a00');c.branch('6000','band21_target')
 c.label('band21_to_right');c.emit('3a3c00bf')
 c.label('band21_target');c.emit('3385400033854008');c.emit('9a42');c.branch('6900','band21_native')
 for off in [2,10]:
  c.emit('323130'+f'{off:02x}'+'04410046c3c583c0');c.branch('6900','band21_native');c.emit('06410046');c.branch('6900','band21_native');c.emit('338140'+f'{off:02x}')
 c.branch('6000','band21_commit')
 c.label('band21_native');c.emit('4cdf000f48d1000f4cdf7fff');c.jump(c.labels['band17'])
 c.label('band21_commit');c.emit('4fef00104cdf7fff');c.jump(c.labels['band17'])
 c.label('band21_both');c.abs('3039',0xffff260c);c.abs('45f9',0x11508);c.emit('08390003');c.address(STATE+39);c.branch('6700','band21_both_axis');c.emit('45ea0100')
 c.label('band21_both_axis');c.emit('323200004a41');c.branch('6a00','band21_both_abs');c.emit('4441')
 c.label('band21_both_abs');c.emit('0c410100');c.branch('6500','band21_native')
 c.label('band21_skip');c.emit('4fef00104cdf7fff4e75');hook(old['band_guard_above_keep'],old['band_guard_above_keep']+6,'band21')


 # v25: first stationary turn is 16, held turns 32. Latch updated by actual
 # movement dispatch, reset each input frame when direction is released/changed.
 c.label('turn24_reset');c.emit('48e7c000');c.abs('3039',0xffff0004);c.emit('4640320002410003');c.branch('6600','turn24_clear');c.emit('0240000c');c.abs('1239',STATE+45);c.emit('b001');c.branch('6700','turn24_reset_done');c.label('turn24_clear');c.abs('4239',STATE+45)
 c.label('turn24_reset_done');c.emit('4cdf0003');c.jump(0x67ac)
 # Replace last callback in old main_input; keep polling and hotkeys unchanged.
 at=old['main_input'];needle=bytes.fromhex('4eb9000067ac');pos=r.index(needle,at,at+100);r[pos+2:pos+6]=c.labels['turn24_reset'].to_bytes(4,'big')
 for tag,bit,delta,addr in [('left',4,-16,0xa2bc),('right',8,16,0xa2cc)]:
  c.label('turn24_'+tag);c.call(0xa2ac);c.emit('323c'+f'{delta&65535:04x}');c.emit('0c3900'+f'{bit:02x}');c.address(STATE+45);c.branch('6600','turn24_'+tag+'_first');c.emit('d241')
  c.label('turn24_'+tag+'_first');byte(STATE+45,bit);c.call(0xa33e);c.jump(0xa14c);hook(addr,addr+6,'turn24_'+tag)
 # Airlock Enter -> yellow button. Reverse remains digit 6.
 r[0x5f8a+16:0x5f8a+20]=(0x6052).to_bytes(4,'big')
 # Any Y item which changes the world-view callback to an object panel must
 # enter native inventory input mode. Ordinary consumables retain their mode.
 c.label('use24');c.abs('2f39',0xffff26b8);c.call(0x72ac);c.abs('2039',0xffff26b8);c.emit('b09f');c.branch('6700','use24_done');c.abs('50f9',0xffff270a)
 c.label('use24_done');c.emit('4e75')
 at=old['item_keys'];pos=r.index(bytes.fromhex('4ef9000072ac'),at,at+140);r[pos+2:pos+6]=c.labels['use24'].to_bytes(4,'big')
 # Native cursor mapping scans unbounded if coming from a different panel.
 # Search only until its sentinel and fall back to the first inventory node.
 c.label('cursor24');c.emit('2f072448');c.abs('2279',0xffff202a);c.emit('30113e3c003f')
 c.label('cursor24_scan');c.emit('4a50');c.branch('6b00','cursor24_default');c.emit('b050');c.branch('6700','cursor24_found');c.emit('41e80014');c.branch('51cf','cursor24_scan')
 c.label('cursor24_default');c.emit('204a')
 c.label('cursor24_found');c.abs('23c8',0xffff202a);c.emit('2e1f4e75');hook(0x8f24,0x8f2c,'cursor24')
 # Optional safety: at one smallest gauge division (16/512), before death check.
 # For an object panel, close it using native return-to-world before sleeping.
 c.label('autosleep24');tst(FLAGS['autosleep']);c.branch('6700','autosleep24_done');c.emit('0c790010');c.address(0xffff2a2a);c.branch('6e00','autosleep24_done');tst(0xffff270e);c.branch('6600','autosleep24_done')
 c.emit('0cb900002106');c.address(0xffff26b8);c.branch('6700','autosleep24_world');c.call(0x2190)
 c.label('autosleep24_world');c.abs('4a79',0xffff2a2a);c.branch('6e00','autosleep24_positive');word(0xffff2a2a,1);c.label('autosleep24_positive');c.call(0x6fb2)
 c.label('autosleep24_done');c.emit('4e75')
 c.label('death24');c.call(c.labels['autosleep24']);c.call(0x2ce2);c.call(0x2cb2);c.jump(0x20c8);hook(0x20c0,0x20c8,'death24')
 # Battery remains native, every 16 updates. Energy pulse at 8 mod 64
 # fits between battery pulses; native easing finishes within seven updates.
 c.label('warnings24');c.emit('4eb9');c.fix.append((len(c.b),('absolute','name26_frame')));c.address(0);c.emit('48e7fffe');c.emit('0cb900002106');c.address(0xffff26b8);c.branch('6600','warnings24_done');c.abs('3039',0xffff29ac);c.emit('0240003f');c.emit('0c400008');c.branch('6600','warnings24_done')
 c.abs('3039',0xffff2a2a);c.emit('c0fc0014');c.emit('7200');c.abs('3239',0xffff2a2c);c.emit('c2fc0003b081');c.branch('6e00','warnings24_done');c.emit('7400');c.branch('6000','warnings24_pulse')
 c.label('warnings24_pulse');c.abs('41f9',0xffff284c);c.abs('43f9',0xffff28cc);c.emit('7e0f');c.branch('6100','warnings24_colors');c.abs('41f9',0xffff288c);c.abs('43f9',0xffff290c);c.emit('7e07');c.branch('6100','warnings24_colors');c.abs('50f9',0xffff2702);c.abs('50f9',0xffff2703)
 c.label('warnings24_done');c.emit('4cdf7fff');c.abs('4a39',0xffff2703);c.jump(0x2092)
 c.label('warnings24_colors');c.emit('30184a42');c.branch('6600','warnings24_half');c.emit('7000');c.branch('6000','warnings24_store')
 c.label('warnings24_half');c.emit('e24802400666') # halve RGB components, retain even Genesis levels
 c.label('warnings24_store');c.emit('32c0');c.branch('51cf','warnings24_colors');c.emit('4e75');hook(0x208c,0x2092,'warnings24')

 r[0x8c54:0x8c5e]=bytes.fromhex('4e71')*5
 # v26: retain a consumable's group, otherwise select its old right neighbour.
 c.label('consume26');c.emit('48e70e00');c.abs('43f9',0xffff2f50);c.abs('3039',0xffff2740);c.emit('78001831000032007aff7c33')
 c.label('consume26_next');c.emit('52410c410034');c.branch('6d00','consume26_read');c.emit('7200')
 c.label('consume26_read');c.emit('1a311000');c.branch('6b00','consume26_skip');c.emit('ba04');c.branch('6600','consume26_remove')
 c.label('consume26_skip');c.branch('51ce','consume26_next')
 c.label('consume26_remove');c.emit('50f10000');c.call(0x6d84);c.abs('43f9',0xffff2f50);c.emit('72007c33')
 c.label('consume26_same');c.emit('b8311000');c.branch('6700','consume26_select');c.emit('5241');c.branch('51ce','consume26_same');c.emit('72007c33')
 c.label('consume26_other');c.emit('ba311000');c.branch('6700','consume26_select');c.emit('5241');c.branch('51ce','consume26_other');c.emit('7200')
 c.label('consume26_select');c.call(0x6e98);c.emit('4cdf0070');c.jump(0x6738);hook(0x7204,0x720a,'consume26')
 # Refill/Chemicals only work in their own native refill panels.
 c.label('refill26_allowed');c.abs('3039',0xffff21ba);c.emit('0240003f0c400013');c.branch('6600','refill26_chem');c.emit('0cb900008576');c.address(0xffff26b8);c.branch('6000','refill26_result')
 c.label('refill26_chem');c.emit('0c400015');c.branch('6600','refill26_yes');c.emit('0cb900008476');c.address(0xffff26b8)
 c.label('refill26_result');c.branch('6700','refill26_yes');c.emit('70ff4e75')
 c.label('refill26_yes');c.emit('70004e75')
 c.label('refill26_valid');c.call(c.labels['refill26_allowed']);c.emit('4a40');c.branch('6600','refill26_done');c.abs('3039',0xffff2740);c.jump(0x55c0)
 c.label('refill26_done');c.emit('4e75');hook(0x55ba,0x55c0,'refill26_valid')
 c.label('refill26_use');c.call(c.labels['refill26_allowed']);c.emit('4a40');c.branch('6600','refill26_done');tst(0xffff2715);c.jump(0x72b2);hook(0x72ac,0x72b2,'refill26_use')
 # Terminal: select cable once, after the card is visibly inserted.
 c.label('terminal26_cable');c.emit('23fc00007cce');c.address(0xffff226e);c.emit('7006');c.call(0x8f4a);c.jump(0x7c8a);hook(0x7c80,0x7c8a,'terminal26_cable')
 # Copy the user's 18 unused CORE-logo tiles, keeping every used HUD tile.
 easter=bytes.fromhex(Path(__file__).with_name('easter_tiles.hex').read_text());assert len(easter)==576
 for i,(a,b) in enumerate([(0x37d1e,0x37dde),(0x37e7e,0x37f3e),(0x3813e,0x381fe)]):r[a:b]=easter[i*192:(i+1)*192]

 # Gas instrument: stereo pan, identical operator levels/envelopes.
 assert r[0x14f8d]==0x40;r[0x14f8d]=0xc0
 # Seed new games from pre-game VBlank elapsed frames. Passwords retain legacy seed;
 # extended SRAM restores its exact keypad table after ordinary initialization.
 c.label('seed26');byte(STATE+87,0);byte(STATE+88,0);byte(STATE+80,0);word(STATE+82,0);byte(STATE+84,0);byte(STATE+56,0);word(STATE+58,0);word(STATE+64,65535);word(STATE+66,65535);word(STATE+68,0);word(STATE+70,0);word(STATE+72,0);word(STATE+74,0);byte(STATE+78,0xa6);byte(STATE+62,0);byte(STATE+63,0);word(STATE+52,0);byte(STATE+54,0);c.emit('203c01234567');tst(0xffff2712);c.branch('6600','seed26_store');c.abs('3039',0xffff2798);c.emit('c0fc9e370a8001234567')
 c.label('seed26_store');c.abs('23c0',0xffff2294);c.emit('2f07');c.emit('7e1f')
 c.label('seed26_warm');tst(0xffff2712);c.branch('6600','seed26_done');c.call(0x5054);c.branch('51cf','seed26_warm')
 c.label('seed26_done');c.emit('2e1f');c.jump(0x1f82);hook(0x1f78,0x1f82,'seed26')
 # Destroyed fuse box reduces automatic restoration opportunities 20-fold.
 c.label('fuse26_destroy');byte(STATE+54,255);word(STATE+52,0);c.emit('70ff4bf9ffff2150');c.jump(0x7b1a);hook(0x7b12,0x7b1a,'fuse26_destroy')
 c.label('fuse26_tick');c.abs('3039',0xffff29ac);c.emit('024003ff');c.branch('6600','fuse26_return');tst(STATE+54);c.branch('6700','fuse26_native');c.abs('5279',STATE+52);c.emit('0c790014');c.address(STATE+52);c.branch('6500','fuse26_return');word(STATE+52,0)
 c.label('fuse26_native');c.jump(0x330e)
 c.label('fuse26_return');c.emit('4e75');hook(0x3302,0x330e,'fuse26_tick')
 # End credits: same 40-character line scroller, unmodified original credits.
 # Keep original visible credits and blank tail; append our block at the end.
 native_rows=[source[a:a+40] for a in range(0x1736,0x1eb6,40)]
 last=max(i for i,row in enumerate(native_rows) if row.strip())
 credits=b''.join(native_rows[:last+1])+b' '*40
 for line in [' romhack by', ' '*18+'valentin valet2 kozin', ' '*18+'and gpt 6 astra', ' '*18+'2026']:
  assert len(line)<=40
  credits+=line.ljust(40).encode('ascii')
 credits+=b''.join(native_rows[last+1:])
 strings['credits26_text']=credits.decode('ascii')+'\0'
 c.label('credits26');c.emit('4879');c.fix.append((len(c.b),('absolute','credits26_text')));c.address(0);c.jump(0xbbc);hook(0xbb6,0xbbc,'credits26')

 # Eye's native bounds test accidentally compares X with the Z limit.
 assert r[0xab52:0xab56]==bytes.fromhex('0c413200');r[0xab52:0xab56]=bytes.fromhex('0c433200')
 # Map impact destroys D2 (Z), and destroying fuse can overwrite D0 (X).
 c.label('eye26_cell');c.emit('48e7a000');c.call(0xab3e);c.emit('4cdf000506400100');c.jump(0x7680);hook(0x7678,0x7680,'eye26_cell')
 c.label('grenade26_consume');c.call(c.labels['consume26']);c.jump(0x8058);hook(0x803c,0x8058,'grenade26_consume')
 # Grenade terrain damage: native 5-cell half-width, safe bounded 11x11 scan.
 # Uses the existing destructible-cell table; does not destroy ordinary walls.
 c.label('grenade26_map');c.emit('48e7fffe302800083428000c04400500044205003c007e0a48473e3c000a')
 c.label('grenade26_row');c.emit('48e7a000');c.call(0xab3e);c.emit('4cdf000506400100');c.branch('51cf','grenade26_row');c.emit('0642010030064847');c.branch('51cf','grenade26_outer');c.branch('6000','grenade26_done')
 c.label('grenade26_outer');c.emit('48473e3c000a');c.branch('6000','grenade26_row')
 c.label('grenade26_done');c.emit('4cdf7fff317c012c002e');c.jump(0x81e2);hook(0x81dc,0x81e2,'grenade26_map')
 # Bomb destruction must trigger the same outage when it removes a fuse box.
 c.label('bomb26_fuse');c.emit('1c130246003f0c460020');c.branch('6600','bomb26_continue');c.emit('48e7fffe');c.call(0x7b12);c.emit('4cdf7fff')
 c.label('bomb26_continue');c.jump(0x97b8);hook(0x97b2,0x97b8,'bomb26_fuse')

 # Embryo has its own sprite; remove only its spurious first scanline.
 embryo=0x914e0
 for col in range(16):r[embryo+col*17]=0
 # World-object preview must not depend on the selected backpack placeholder slot.
 c.label('preview26');c.emit('0c470eb18'.replace('0eb18','eb18'));c.branch('6700','preview26_world');c.emit('0c790020');c.address(0xffff2740);c.jump(0x374a)
 c.label('preview26_world');c.jump(0x374c);hook(0x3742,0x374a,'preview26')

 # Bomb: Enter commits the displayed timer; editing invalidates the commit.
 c.label('bomb26_open');byte(STATE+60,0);c.abs('41f9',0x1813a);c.jump(0x9500);hook(0x94fa,0x9500,'bomb26_open')
 c.label('bomb26_input');c.emit('0c400064');c.branch('6600','bomb26_digit');tst(STATE+60);c.branch('6700','bomb26_return');c.abs('4a79',0xffff2198);c.branch('6700','bomb26_return');c.jump(0x98ae)
 c.label('bomb26_digit');c.call(0x9a96);c.emit('0c41000a');c.branch('6700','bomb26_enter');byte(STATE+60,0);c.jump(0x9898)
 c.label('bomb26_enter');c.abs('4a79',0xffff2198);c.branch('6700','bomb26_return');byte(STATE+60,255)
 c.label('bomb26_return');c.emit('4e75');hook(0x9888,0x988e,'bomb26_input')
 # Native red lamp was reset/closed before it could be seen. Flush it first.
 c.label('keypad32_lamps');c.call(0x9d40);c.abs('4a79',0xffff29ba);c.branch('6700','keypad32_no_alarm');c.emit('337c00b20004');c.abs('50f9',0xffff2700);c.label('keypad32_no_alarm');c.call(0x9d5c);c.jump(0x9936);hook(0x992e,0x9936,'keypad32_lamps')
 c.label('keypad32_frame');c.call(0x2930);c.abs('2279',0xffff227e);c.abs('d2f9',0xffff223e);c.emit('92fc0048303c00b3');c.abs('4a79',0xffff29ba);c.branch('6700','keypad32_apply');c.emit('303c00b2');c.label('keypad32_apply');c.emit('b0690004');c.branch('6700','keypad32_redraw');c.emit('33400004');c.abs('50f9',0xffff2700);c.label('keypad32_redraw');c.call(0x38c8);c.jump(0x991e);hook(0x9916,0x991e,'keypad32_frame')
 c.label('keypad26_red');c.emit('337c00b20004');c.abs('50f9',0xffff2700);c.emit('0cb900009916');c.address(0xffff26b8);c.branch('6600','keypad26_red_done');c.call(0x38c8);c.call(0x4d18);c.emit('7204');c.call(0x7994)
 c.label('keypad26_red_done');c.jump(0x9b4a);hook(0x9b3e,0x9b4a,'keypad26_red')

 # A is a gesture modifier. Direction changes rotate the movement vector,
 # never the view; diagonal speed uses the same scalar speed as axial motion.
 c.label('strafe26');c.abs('3039',0xffff0004);c.emit('08000006');c.branch('6600','strafe26_native');c.emit('464036000243000c0c430004');c.branch('6700','strafe26_side');c.emit('0c430008');c.branch('6600','strafe26_native')
 c.label('strafe26_side');byte(STATE+62,255)
 # Ground-only in a normal jump; levitation/jetpack permit air strafing.
 tst(0xffff26e4);c.branch('6600','strafe26_allowed');tst(0xffff26e5);c.branch('6600','strafe26_allowed');c.abs('3039',0xffff441c);c.abs('b079',0xffff4440);c.branch('6e00','strafe26_native')
 c.label('strafe26_allowed');c.abs('3039',0xffff0004);c.emit('464036000243000f');c.abs('41f9',0xffff4412);c.emit('3003024000030c400002');c.branch('6700','strafe26_backward');c.call(0xa268)
 c.emit('3003024000030c400001');c.branch('6700','strafe26_frontdiag');c.emit('323c0100');c.branch('6000','strafe26_frontsign')
 c.label('strafe26_frontdiag');c.emit('323c0080')
 c.label('strafe26_frontsign');c.emit('08030002');c.branch('6700','strafe26_apply');c.emit('4441');c.branch('6000','strafe26_apply')
 c.label('strafe26_backward');c.call(0xa184);c.call(0xa324);c.emit('323c008008030003');c.branch('6700','strafe26_apply');c.emit('4441')
 c.label('strafe26_apply');c.emit('d3680028026803fe0028');c.abs('3039',0xffff260c);c.emit('90680028314000324e75')
 c.label('strafe26_native');c.abs('3039',0xffff0004);c.jump(0xa0f0);hook(0xa0ea,0xa0f0,'strafe26')
 # A-up triggers jump/crouch only if no strafe occurred during this gesture.
 c.label('gesture26');tst(0xffff26e8);c.branch('6700','gesture26_pad');c.abs('3039',0xffff441c);c.abs('b079',0xffff4440);c.branch('6d00','gesture26_pad');c.abs('4239',0xffff26e8)
 c.label('gesture26_pad');c.abs('3039',0xffff0004);c.emit('08000006');c.branch('6600','gesture26_released');c.emit('464002400003');c.branch('6700','gesture26_done');c.abs('13c0',STATE+63);c.emit('4e75')
 c.label('gesture26_released');c.emit('08390006');c.address(0xffff0007);c.branch('6600','gesture26_done');tst(STATE+62);c.branch('6600','gesture26_cancel');c.abs('3039',0xffff0004);c.emit('464002400003');c.branch('6600','gesture26_direction');c.emit('7000');c.abs('1039',STATE+63)
 c.label('gesture26_direction');c.emit('0c400001');c.branch('6700','gesture26_up');c.emit('0c400002');c.branch('6600','gesture26_cancel');c.call(0x9dc6);c.call(0x9dce);c.branch('6000','gesture26_cancel')
 c.label('gesture26_up');c.call(0x9dea);c.call(0x9dbe)
 c.label('gesture26_cancel');byte(STATE+62,0);byte(STATE+63,0)
 c.label('gesture26_done');c.emit('4e75');hook(0xabe0,0xabe6,'gesture26')

 # Sample physical controls once per VBlank, separately from game input RAM.
 # D0 is the first TH-low sample already read by poll6. Pad bits 2/3 are zero.
 c.label('pad28_sample');c.emit('2f0132000241000c');c.branch('6600','pad28_absent');byte(STATE+80,255);word(STATE+82,0);byte(STATE+84,0);c.branch('6000','pad28_sample_done')
 c.label('pad28_absent');tst(STATE+80);c.branch('6700','pad28_sample_done');c.emit('0c790006');c.address(STATE+82);c.branch('6400','pad28_sample_done');c.abs('5279',STATE+82);c.emit('0c790006');c.address(STATE+82);c.branch('6600','pad28_sample_done');byte(STATE+84,255);word(STATE+72,0);word(STATE+74,0)
 c.label('pad28_sample_done');c.emit('221f4e75')
 c.label('raw26');raw=bytes(r[old['poll6']:old['mode_action']])
 for was,now in [(0xffff0010,STATE+68),(0xffff0012,STATE+70),(0xffff0004,STATE+64),(0xffff0006,STATE+66)]:raw=raw.replace(was.to_bytes(4,'big'),now.to_bytes(4,'big'))
 assert raw[0x22:0x28]==bytes.fromhex('103900a10003')
 raw=raw[:0x28]+bytes.fromhex('4eb9')+c.labels['pad28_sample'].to_bytes(4,'big')+raw[0x28:]
 c.b.extend(raw)
 c.label('buffer26_mask');c.emit('323c00b0');tst(0xffff270a);c.branch('6700','buffer26_mask_done');c.emit('0041000f');c.abs('2279',0xffff202a);c.emit('0c6900080002');c.branch('6e00','buffer26_mask_a');c.emit('0cb900007070');c.address(0xffff26b8);c.branch('6600','buffer26_mask_done')
 c.label('buffer26_mask_a');c.emit('00410040')
 c.label('buffer26_mask_done');c.emit('4e75')
 c.label('buffer26_sample');c.emit('0c3900a6');c.address(STATE+78);c.branch('6600','buffer26_sample_done');c.abs('4a79',0xffff0014);c.branch('6600','buffer26_sample_done');c.call(c.labels['raw26']);c.emit('4640');c.abs('c079',STATE+66);c.call(c.labels['buffer26_mask']);c.emit('c041');c.abs('8179',STATE+72)
 c.abs('3039',STATE+70);c.emit('4640');c.abs('c079',STATE+68);c.abs('8179',STATE+74)
 c.label('buffer26_sample_done');c.abs('5279',0xffff2798);c.jump(0x1755e);hook(0x17558,0x1755e,'buffer26_sample')
 c.label('buffer26_consume');c.emit('40e7007c070048e76040');c.emit('0c3900a6');c.address(STATE+78);c.branch('6700','buffer26_ready');byte(STATE+80,0);word(STATE+82,0);byte(STATE+84,0);c.call(c.labels['raw26']);word(STATE+72,0);word(STATE+74,0);byte(STATE+62,0);byte(STATE+63,0);byte(STATE+78,0xa6)
 c.label('buffer26_ready');c.call(c.labels['buffer26_mask']);c.abs('3439',STATE+72);c.emit('c441');c.abs('4279',STATE+72)
 c.abs('3039',0xffff0004);c.emit('8042');c.abs('33c0',0xffff0006);c.abs('3039',STATE+64);c.emit('4642c042');c.abs('33c0',0xffff0004)
 c.abs('3439',STATE+74);c.abs('4279',STATE+74);c.abs('3239',0xffff0010);c.emit('4642c242');c.abs('33c1',0xffff0012);c.emit('4642');c.abs('8479',STATE+68);c.abs('33c2',0xffff0010)
 # Reset gesture eligibility when player control is not active.
 tst(0xffff270a);c.branch('6700','buffer26_consume_done');byte(STATE+62,0);byte(STATE+63,0)
 c.label('buffer26_consume_done');c.emit('4cdf020646df4e75')
 at=old['main_input'];assert r[at:at+6]==bytes.fromhex('4eb9')+old['poll6'].to_bytes(4,'big');r[at+2:at+6]=c.labels['buffer26_consume'].to_bytes(4,'big')

 # Brief centered item name on the 8-pixel strip above the action icons.
 c.label('name26_changed');c.abs('33c0',0xffff21ba);byte(STATE+56,255);c.jump(0x6eda);hook(0x6ed4,0x6eda,'name26_changed')
 c.label('name26_clear');c.emit('3e3c000d383ce91e')
 c.label('name26_clear_loop');c.emit('3404303c011b');c.call(0x35fe);c.emit('5444');c.branch('51cf','name26_clear_loop');c.emit('4e75')
 c.label('name32_before_sleep');c.emit('48e7fffe');c.abs('4a79',STATE+58);c.branch('6700','name32_sleep_cleared');c.call(c.labels['name26_clear']);c.label('name32_sleep_cleared');byte(STATE+56,0);word(STATE+58,0);c.emit('4cdf7fff4e75');
 c.label('name26_frame');c.emit('48e7fffe');tst(0xffff270e);c.branch('6600','name30_cancel');c.emit('0cb900007070');c.address(0xffff26b8);c.branch('6700','name30_cancel');c.emit('0cb900008d42');c.address(0xffff26b8);c.branch('6600','name30_normal');tst(0xffff26eb);c.branch('6600','name30_cancel');c.abs('4a79',STATE+58);c.branch('6700','name30_cancel');c.call(c.labels['name26_clear']);c.label('name30_cancel');byte(STATE+56,0);word(STATE+58,0);c.branch('6000','name26_done');c.label('name30_normal');tst(STATE+56);c.branch('6600','name26_show');c.abs('3039',STATE+58);c.branch('6700','name26_done');c.abs('3239',0xffff2798);c.emit('9240');c.branch('6b00','name26_done');word(STATE+58,0);c.call(c.labels['name26_clear']);c.branch('6000','name26_done')
 c.label('name26_show');byte(STATE+56,0);c.call(c.labels['name26_clear']);c.abs('3039',0xffff21ba);c.emit('0240003f0c400022');c.branch('6200','name26_done');c.emit('c0fc000c');c.abs('4bf9',0x103f3);c.emit('dac07e0a')
 c.label('name26_trim_left');c.emit('0c150020');c.branch('6600','name26_trim_right');c.emit('528d');c.branch('51cf','name26_trim_left');c.branch('6000','name26_done')
 c.label('name26_trim_right');c.emit('0c3570200020') # corrected below: cmpi.b #space,(a5,d7.w)
 c.b[-6:]=bytes.fromhex('0c3500207000')
 c.branch('6600','name26_draw');c.emit('5347');c.branch('6a00','name26_trim_right');c.branch('6000','name26_done')
 c.label('name26_draw');c.emit('363c002d96470243fffe0643e900');c.emit('4eb9');c.fix.append((len(c.b),('absolute','name27_text')));c.address(0);c.abs('3039',0xffff2798);c.emit('06400064');c.branch('6600','name26_timer');c.emit('7001')
 c.label('name26_timer');c.abs('33c0',STATE+58)
 c.label('name26_done');c.emit('4cdf7fff4e75')

 # Gray label glyphs occupy 11 of 18 unused CORE-logo tiles in VRAM.
 # Only the temporary VRAM copy is changed; user's hidden ROM tiles stay intact.
 c.label('name27_text');c.emit('40e7007c07007800');c.emit('33fc8f02');c.address(0xc00004)
 c.label('name27_char');c.emit('7000101d0c000020');c.branch('6700','name27_space');c.emit('0c000039');c.branch('6e00','name27_letter');c.emit('04400015');c.branch('6000','name27_glyph')
 c.label('name27_space');c.emit('7000');c.branch('6000','name27_glyph')
 c.label('name27_letter');c.emit('04400060')
 c.label('name27_glyph');c.emit('c0fc002041f9');c.fix.append((len(c.b),('absolute','name27_font')));c.address(0);c.emit('d0c03204064101150c440006');c.branch('6d00','name27_slot');c.emit('5a41')
 c.label('name27_slot');c.emit('74003401eb4a4842008240000000');c.abs('23c2',0xc00004);c.emit('7c0f')
 c.label('name27_pixels');c.emit('33d8');c.address(0xc00000);c.branch('51ce','name27_pixels')
 c.emit('30013403');c.call(0x35fe);c.emit('54435244');c.branch('51cf','name27_char');c.emit('46df4e75')
 c.label('name27_font')
 font=source[0x30716:0x30716+40*32]
 assert set(n for b in font for n in [b>>4,b&15])=={0,15}
 # HUD tile $11B is palette0: retain each background pixel under the glyph.
 background=source[0x37dde:0x37dfe]
 assert background==bytes.fromhex('22'*28+'00'*4)
 c.b.extend(bytes(((7 if b>>4 else background[i%32]>>4)<<4)|(7 if b&15 else background[i%32]&15) for i,b in enumerate(font)))

 # Ending alone bypasses music-off, without restarting an existing main theme.
 c.label('ending29_music');c.emit('48e7c000');c.abs('3039',0xffff7d2c);c.emit('0c400002');c.branch('6700','ending29_done');c.emit('4a40');c.branch('6600','ending29_start')
 c.emit('0c790002');c.address(STATE+34);c.branch('6600','ending29_start');c.abs('4a79',0xffff7d30);c.branch('6600','ending29_done')
 c.label('ending29_start');c.emit('7001');c.call(0x150c0)
 c.label('ending29_done');c.emit('4cdf00034e75')
 c.label('ending29');c.call(c.labels['ending29_music']);c.call(0x2f80);c.emit('323c003c');c.jump(0x2eb8);hook(0x2eb0,0x2eb8,'ending29')

 # Sleep is entered only at the main-loop input boundary, never inside VBlank.
 c.label('pad28_sleep');tst(STATE+84);c.branch('6700','pad28_sleep_done');c.emit('0cb900002106');c.address(0xffff26b8);c.branch('6600','pad28_sleep_done');tst(0xffff270e);c.branch('6600','pad28_sleep_done');tst(0xffff270f);c.branch('6600','pad28_sleep_done')
 c.emit('48e7fffe');byte(STATE+84,0);word(STATE+72,0);word(STATE+74,0);c.call(0x6fb2);c.emit('4cdf7fff')
 c.label('pad28_sleep_done');c.emit('4e75')
 c.label('pad28_consume');c.call(c.labels['buffer26_consume']);c.emit('2f00');c.call(c.labels['pad28_sleep']);c.emit('201f4e75')
 at=old['main_input'];r[at+2:at+6]=c.labels['pad28_consume'].to_bytes(4,'big')

 c.label('ending30_exit');byte(0xffff2710,0);c.abs('4ff9',0xfffffffe);c.jump(0x386);hook(0x2f78,0x2f80,'ending30_exit')

 # Sleep changes only the displayed Energy bar; native wake adds the gain once.
 # No text/glyph cache. Timer and last displayed value use four bytes.
 c.label('sleep32_dots_frame');c.call(0x2930);c.branch('6100','sleep33_bar');c.call(0x4d18);c.jump(0x7088);hook(0x7080,0x7088,'sleep32_dots_frame')
 c.label('sleep33_bar');c.emit('48e7fffe');c.emit('0c79ffff');c.address(STATE+92);c.branch('6700','sleep33_calc');c.abs('3039',0xffff2798);c.abs('9079',STATE+90);c.emit('323c001e0839000600a10001');c.branch('6700','sleep33_interval');c.emit('323c0019');c.label('sleep33_interval');c.emit('b041');c.branch('6500','sleep33_done')
 c.label('sleep33_calc');c.emit('33f9');c.address(0xffff2798);c.address(STATE+90);c.abs('3839',0xffff20e4);c.emit('e84c0c4401f0');c.branch('6300','sleep33_cap');c.emit('383c01f0');c.label('sleep33_cap');c.emit('024401f0');c.abs('d879',0xffff2a2a);c.emit('0c440200');c.branch('6300','sleep33_value');c.emit('383c0200');c.label('sleep33_value');c.abs('b879',STATE+92);c.branch('6700','sleep33_done');c.abs('33c4',STATE+92)
 c.label('sleep33_done');c.emit('4cdf7fff4e75')
 # Search all 52 slots; an intact Gas Mask overrides any Face Mask.
 c.label('gas33');c.emit('2f027400');c.abs('41f9',0xffff2f50);c.emit('7233');c.label('gas33_next');c.emit('10180c00000f');c.branch('6700','gas33_safe');c.emit('0c000010');c.branch('6600','gas33_continue');c.emit('7401');c.label('gas33_continue');c.branch('51c9','gas33_next');c.emit('4a42');c.branch('6600','gas33_face');c.emit('241f');c.jump(0x3220);c.label('gas33_face');c.emit('241f');c.jump(0x3240);c.label('gas33_safe');c.emit('241f4e75');hook(0x3204,0x320a,'gas33')
 # Block starting the decoder on an alarm-locked keypad, regardless of input route.
 c.label('pick33');c.abs('4a79',0xffff29ba);c.branch('6700','pick33_native');c.emit('4e75');c.label('pick33_native');c.emit('08070006');c.branch('6700','pick33_unbroken');c.jump(0x9c1e);c.label('pick33_unbroken');c.jump(0x9be2);hook(0x9bdc,0x9be2,'pick33')
 # The lift leaves its Use suppression latch set after arrival: clear it at exit.
 c.label('lift33_arrived');c.call(0x9342);byte(0xffff2715,0);c.jump(0x2190);hook(0x8e50,0x8e58,'lift33_arrived')
 # Native jet sound is a two-voice music sequence, not an independent SFX.
 # Keep alarm priority and release the jet sequence on manual/battery shutdown.
 c.label('jet33_start');c.abs('4a79',0xffff29ba);c.branch('6600','jet33_done');c.emit('7020');c.jump(0x150b4)
 c.label('jet33_done');c.emit('4e75');hook(0x7b7a,0x7b84,'jet33_start')
 c.label('jet33_finish');c.abs('3039',0xffff7d2c);c.branch('6600','jet33_queued');c.abs('3039',STATE+34);c.label('jet33_queued');c.emit('0c400021');c.branch('6600','jet33_done');c.emit('7001');c.abs('4a79',0xffff29ba);c.branch('6700','jet33_send');c.emit('701f');c.label('jet33_send');c.jump(0x150b4)
 a=old['down_a13'];at=r.index(bytes.fromhex('4ef9000150b4'),a,a+70);r[at+2:at+6]=c.labels['jet33_finish'].to_bytes(4,'big')
 c.label('jet33_empty');c.emit('48e78000');tst(0xffff26e4);c.branch('6700','jet33_empty_clear');c.call(c.labels['jet33_finish']);c.label('jet33_empty_clear');byte(0xffff26e4,0);byte(0xffff26de,0);c.emit('4cdf0001');c.jump(0x32be);hook(0x32b2,0x32be,'jet33_empty')
 c.label('jet33_alarm_end');c.emit('7001');tst(0xffff26e4);c.branch('6700','jet33_send');c.emit('7020');c.branch('6000','jet33_send')
 hook(0x7d04,0x7d0e,'jet33_alarm_end')
 c.label('jet33_timeout');c.call(c.labels['jet33_alarm_end']);c.jump(0x34b8);hook(0x34ae,0x34b8,'jet33_timeout')
 c.label('jet34_toggle');tst(0xffff26e4);c.branch('6700','jet34_on');byte(0xffff26e4,0);byte(0xffff26e8,0);byte(0xffff26e9,0);c.jump(c.labels['jet33_finish'])
 c.label('jet34_on');c.jump(0x7b74);hook(0x7b6c,0x7b74,'jet34_toggle')

 c.label('intro31_blank');c.emit('08b90006ffff000333f9ffff000200c00004');byte(STATE+86,255);c.emit(rom[old['intro_skip']:old['intro_skip']+6].hex());c.jump(old['intro_skip']+6);hook(old['intro_skip'],old['intro_skip']+6,'intro31_blank')
 c.label('intro31_show');tst(STATE+86);c.branch('6700','intro31_show_done');c.call(0x26b8);c.emit('08f90006ffff000333f9ffff000200c00004');byte(STATE+86,0)
 c.label('intro31_show_done');c.emit('4e75')

 # align data
 if len(c.b)%2:c.emit('00')
 c.label('sound_table')
 for fx,cmd in SOUND_COMMANDS:c.emit(f'{cmd:04x}{fx:04x}')
 for label,text in strings.items():c.label(label);c.b.extend(text.encode('ascii'))
 for pos,label in c.fix:
  if isinstance(label,tuple):c.b[pos:pos+4]=c.labels[label[1]].to_bytes(4,'big')
  else:c.b[pos:pos+2]=(c.labels[label]-(base.BASE+pos)).to_bytes(2,'big',signed=True)
 blob=c.b[start:];assert set(r[0xf6000:0xf6000+len(blob)])=={255};r[0xf6000:0xf6000+len(blob)]=blob
 r[0x18e:0x190]=(sum(int.from_bytes(r[i:i+2],'big') for i in range(0x200,len(r),2))&65535).to_bytes(2,'big')
 return bytes(r),dict(old,**c.labels)
if __name__=='__main__':
 if len(sys.argv) not in (1,4):raise SystemExit('Usage: python3 build_v34.py Cyber-Cop.bin Corporation.bin output_directory')
 srcpath,corppath,out=(sys.argv[1:] if len(sys.argv)==4 else ['upload/Cyber-Cop_(W)_[c][!].bin','upload/Corporation_(E)_[c][!].bin','v34'])
 src=Path(srcpath).read_bytes();corp=Path(corppath).read_bytes();rom,labels=build(src,corp);out=Path(out);out.mkdir(parents=True,exist_ok=True)
 (out/'Cyber-Cop_v34.bin').write_bytes(rom);(out/'symbols.json').write_text(json.dumps(labels,indent=2));(out/'Cyber-Cop_v34.ips').write_bytes(base.ips(src+bytes(len(rom)-len(src)),rom))
 print('built',len(rom),hashlib.sha256(rom).hexdigest(),hex(max(labels.values())))
