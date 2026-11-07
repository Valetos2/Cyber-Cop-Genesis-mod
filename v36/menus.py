# Executed inside build.py so every symbol and asset has one owner.
STATE=0xffff0100;P=0xffff0200;N=0xffff01a0
def bi(a,v):c.emit('13fc'+f'{v:04x}');c.long(a)
def draw(text,where):
 a=asset('text36_'+str(len(assets)),text.encode('ascii'))
 c.abs('4bf9',a);c.emit('363c'+f'{where:04x}'+'3e3c'+f'{len(text)-1:04x}'+'3c3c2000');c.call(0xffbe)

# Build a compact visible list while keeping stable action IDs0..6.
VISIBLE=0xffff0840;COUNT=0xffff0850;HAS=0xffff0852
c.label('main36_text');c.emit('48e7fffe');c.abs('3f39',CAMP);wi(HAS,0)
for camp in [0,1]:
 wi(CAMP,camp);c.call(V['sram17_load']);c.emit('4a40');c.branch('6700','main36_no_save_'+str(camp));c.emit('08f9'+f'{camp:04x}');c.long(HAS);c.label('main36_no_save_'+str(camp))
c.abs('33df',CAMP);wi(COUNT,0)
for row in range(7):draw(' '*24,0xe212+row*0x100)
for idx,title in enumerate(['start original game','start amiga mission disk','continue original game','continue mission disk','enter password','options','cheats']):
 if idx in [2,3]:c.emit('0839'+f'{idx-2:04x}');c.long(HAS);c.branch('6700','main36_skip_'+str(idx))
 if idx==6:c.abs('4a39',STATE+87);c.branch('6700','main36_skip_'+str(idx))
 c.abs('3039',COUNT);c.emit('3200d040');c.abs('41f9',VISIBLE);c.emit('31bc'+f'{idx:04x}'+'0000')
 a=asset('menu36_title_'+str(idx),title.ljust(24).encode());c.abs('4bf9',a);c.emit('3601e14b0643e2123e3c00173c3c2000');c.call(0xffbe);c.abs('5279',COUNT)
 c.label('main36_skip_'+str(idx))
c.emit('4cdf7fff4e75');patch(V['main18_text'],'main36_text')

c.label('main36_enter')
for a in [P+116,N,P+34,P+24,P+2,P+84]:c.abs('4279',a)
c.abs('42b9',N+20);c.call(V['settings_init']);c.call(V['music20_ensure'])
c.abs('3039',STATE+30);c.abs('b079',COUNT);c.branch('6500','main36_enter_cursor');wi(STATE+30,0)
c.label('main36_enter_cursor');wi(0xffff29ce,368);bi(0xffff0015,2);c.ref('4eb9','main36_cursor');c.call(V['intro31_show']);c.abs('50f9',0xffff2702);c.call(0x1646);wi(0xffff0008,2500)
c.label('main36_loop');c.call(0x2930);c.call(0x53a8);c.abs('3839',0xffff0006);c.emit('32004641c841');c.branch('6600','main36_event');c.abs('5379',0xffff0008);c.branch('6600','main36_loop');c.jump(0x77a)
c.label('main36_event');wi(0xffff0008,2500);c.abs('3239',STATE+30)
c.emit('3004024000fd');c.branch('6700','main36_count_ok');bi(STATE+88,0)
c.label('main36_count_ok');c.emit('08040000');c.branch('6700','main36_down');c.emit('5341');c.branch('6a00','main36_changed');c.emit('7200');c.branch('6000','main36_changed')
c.label('main36_down');c.emit('08040001');c.branch('6700','main36_confirm');c.abs('4a39',STATE+87);c.branch('6600','main36_unlocked');c.abs('3039',COUNT);c.emit('5340b240');c.branch('6d00','main36_inc');c.abs('3039',0xffff0004);c.emit('024000ff0c4000fd');c.branch('6600','main36_bad_down');c.emit('0c440002');c.branch('6600','main36_loop');c.abs('5239',STATE+88);c.emit('0c390004');c.long(STATE+88);c.branch('6500','main36_loop');bi(STATE+87,255);bi(STATE+88,0);c.call(c.labels['main36_text']);c.abs('3239',COUNT);c.emit('5341');c.branch('6000','main36_changed')
c.label('main36_bad_down');bi(STATE+88,0);c.branch('6000','main36_loop')
c.label('main36_unlocked');c.abs('3039',COUNT);c.emit('5340b240');c.branch('6c00','main36_loop')
c.label('main36_inc');c.emit('5241')
c.label('main36_changed');c.abs('33c1',STATE+30);draw(' '*24,0xe014);c.ref('4eb9','main36_cursor');c.branch('6000','main36_loop')
c.label('main36_confirm');c.emit('08040004');c.branch('6700','main36_loop');bi(0xffff0015,2);c.emit('d241');c.abs('41f9',VISIBLE);c.emit('32301000')
for idx,target in [(0,'start_original36'),(1,'start_mission36'),(2,'resume_original36'),(3,'resume_mission36')]:
 c.emit('0c41'+f'{idx:04x}');c.branch('6700',target)
for idx,target in [(4,'opt14_password'),(5,'options14'),(6,'cheats31')]:
 c.emit('0c41'+f'{idx:04x}');c.branch('6600','main36_not_'+str(idx));c.jump(V[target]);c.label('main36_not_'+str(idx))
c.branch('6000','main36_loop')
for name,camp,target in [('start_original36',0,S['newmenu35']),('start_mission36',1,S['newmenu35']),('resume_original36',0,V['resume17']),('resume_mission36',1,V['resume17'])]:
 c.label(name);wi(CAMP,camp);c.jump(target)
c.label('main36_cursor');c.abs('3039',STATE+30);c.emit('e948064000f8');c.abs('33c0',0xffff29c8);c.call(0xf7b2);c.emit('4e75')
for old,new in [('main18_enter','main36_enter'),('main18_loop','main36_loop'),('main18_cursor','main36_cursor')]:patch(V[old],new)
# A test map selected from either campaign must still use its own original adapter.
c.label('lab_select36');wi(CAMP,0);wi(P+108,0x100);c.jump(0xa56)
lab_store=S['newmenu35_accept']+8+4+4 # Locate by bytes rather than rely on layout.
needle=bytes.fromhex('33fc0100ffff026c4ef900000a56')
hits=[p for p in range(S['newmenu35_accept'],S['newmenu35_main']) if src[p:p+len(needle)]==needle]
assert len(hits)==1,hits
patch(hits[0],'lab_select36',8)
