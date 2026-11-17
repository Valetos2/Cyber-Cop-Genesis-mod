lab=bytearray(src[1573978:1577978])
for x,z,v in [(22,10,0x9c),(24,10,0x9d),(26,10,0x9e),(14,15,0x82),(22,14,0x82),(26,14,0x82)]:
 assert lab[(49-z)*80+x]==0;lab[(49-z)*80+x]=v
labptr=asset('lab02_map36b',lab)
p=src.index(bytes.fromhex('41f9')+struct.pack('>I',1573978),S['floor35'],S['floor35_main'])
table_hook(p,labptr,'lab_map36b')
# The second hidden laboratory is exposed together with the first one.
c.label('lab_reveal36b');draw('load test map 02',0xe50e);c.emit(src[S['newmenu35_unlocked']:S['newmenu35_unlocked']+8].hex()) if False else None
c.jump(S['newmenu35_loop'])
# Back (index 2) is always visible. Four new Down presses at that row
# expose the two maps at indices 3 and 4.
for start,end,old,new in [
 ('newmenu35_down','newmenu35_unlocked','0c410001','0c410002'),
 ('newmenu35_down','newmenu35_unlocked','363ce40e','363ce50e'),
 ('newmenu35_down','newmenu35_unlocked','72026000','72036000'),
 ('newmenu35_unlocked','newmenu35_inc','0c410002','0c410004'),
]:
 p=src.index(bytes.fromhex(old),S[start],S[end]);assert r[p:p+4]==bytes.fromhex(old)
 r[p:p+4]=bytes.fromhex(new)
c.label('lab_cursor36b');c.emit('48e7fffe')
c.ref('4bf9','newmenu_back_text36');c.emit('363ce40e3e3c00033c3c2000');c.call(0xffbe)
c.abs('4a79',P+110);c.branch('6700','lab_cursor_done36b');draw('load test map 02',0xe60e);c.label('lab_cursor_done36b');c.emit('4cdf7fff');c.emit(src[S['newmenu35_cursor']:S['newmenu35_cursor']+6].hex());c.jump(S['newmenu35_cursor']+6);patch(S['newmenu35_cursor'],'lab_cursor36b')
c.label('newmenu_back_text36');c.emit('6261636b')
c.label('lab_accept36b');wi(P+108,0);c.emit('0c410002');c.branch('6500','lab_normal36b');c.branch('6700','lab_back36b');wi(CAMP,0);wi(P+108,0x100);c.emit('0c410004');c.branch('6600','lab_start36b');wi(CAMP,1);wi(P+108,0x101)
c.label('lab_start36b');c.jump(0xa56)
c.label('lab_normal36b');c.jump(S['newmenu35_main']);patch(S['newmenu35_accept'],'lab_accept36b',8)
c.label('lab_back36b');c.jump(S['newmenu35_back'])
c.label('lab_actor36b');c.abs('4a79',P+108);c.branch('6700','lab_actor_native36b');c.emit('0c790101');c.long(P+108);c.branch('6600','lab_actor_done36b');c.emit('303c1980343c0e80');c.call(c.labels['robot_constructor36'])
c.label('lab_actor_done36b');c.emit('4e75')
c.label('lab_actor_native36b');c.jump(S['construct35']+6);patch(S['construct35'],'lab_actor36b')
