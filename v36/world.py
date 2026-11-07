# Access permissions differ between the campaigns even where elevator button
# ordering is the same. Retain each campaign's eight access-level rows.
table_hook(0x8e80,asset('mission_lift_access',A[0x13cea:0x13dea]),'lift_access36')
# Amiga floor callbacks select flying/crawling ambient enemies independently.
c.label('ambient_both36');c.abs('3039',0xffff2730);c.abs('d079',0xffff2732);c.emit('0c400006');c.branch('6e00','ambient_done36');c.emit('08390000');c.long(0xffff2799);c.branch('6600','ambient_ground36');c.jump(0xa3ea)
c.label('ambient_ground36');c.jump(0xa496)
c.label('ambient_done36');c.emit('4e75')
ambient={0xc482:0xa3ea,0xc528:0xa496,0xd31e:0xb426,0xc43e:c.labels['ambient_both36']}
table_hook(0x486c,asset('mission_ambient',struct.pack('>16I',*[ambient[al(0x131a8+f*4)] for f in range(16)])),'ambient36')
# Capture/death relocates the player to a different prison in Mission.
c.label('prison36');tstcamp();c.branch('6700','prison36_original')
wi(0xffff2606,10);c.call(0x4a80);wi(0xffff441a,0x4500);wi(0xffff441e,0x1800);c.jump(0x2e04)
c.label('prison36_original');c.emit(src[0x2de8:0x2df0].hex());c.jump(0x2df0);patch(0x2de8,'prison36',8)
# The special gas/alarm terminal is L8 in Mission rather than L3 in Genesis.
c.label('alarm_floor36');tstcamp();c.branch('6700','alarm_floor36_original');c.emit('0c79000f');c.long(0xffff2606);c.jump(0x7d24)
c.label('alarm_floor36_original');c.emit(src[0x7d1c:0x7d24].hex());c.jump(0x7d24);patch(0x7d1c,'alarm_floor36',8)
