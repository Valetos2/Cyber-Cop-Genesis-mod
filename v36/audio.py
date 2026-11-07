# Keep the original driver/sample intact. Its unused Z80 tail contains incidental
# following ROM text, so use a private boot image rather than overwrite that text.
driver=bytearray(src[0x157a8:0x16ba8]);assert len(driver)==0x1400
for address,source,length in [(0x1c00,0x2e520,494),(0x1e00,0x32078,192)]:
 driver[address-0xc00:address-0xc00+length]=bytes(x^128 for x in A[source:source+length])
# Loop only the robot attack. All other PCM starts clear the loop flag, and the
# original DAC shutdown path still restores FM channel6 on completion.
stub=bytes.fromhex('3a301fb7280721001e01c000c9cf3eb6c31d11')
driver[0x1f00-0xc00:0x1f00-0xc00+len(stub)]=stub
driver[0x1f30-0xc00]=0
driver[0x111a-0xc00:0x111d-0xc00]=bytes.fromhex('c3001f')
c.label('sound_boot36');c.abs('41f9',asset('z80_driver36',driver));c.abs('43f9',0xa00c00);c.jump(0x15684);patch(0x1567a,'sound_boot36',10)
c.label('pcm_loop36');c.emit('0c401e00');c.abs('57f9',0xa01f30);c.abs('57f9',0xffff0804);c.emit(src[0x155c4:0x155ca].hex());c.jump(0x155ca);patch(0x155c4,'pcm_loop36')
for name,address,length,step in [('robot_step_sound36',0x1c00,494,153),('robot_attack_sound36',0x1e00,192,205)]:
 c.label(name);c.abs('4a39',0xffff2711);c.branch('6600',name+'_done');c.emit('48e7fffe40e7007c0700')
 c.emit(f'303c{address:04x}323c{step:04x}343c{length:04x}');c.call(0x155b2);c.emit('46df4cdf7fff')
 c.label(name+'_done');c.emit('4e75')
c.label('robot_stop_sound36');c.abs('4a39',0xffff0804);c.branch('6700','robot_stop_sound36_done');c.abs('4239',0xffff0804);c.emit('48e7fffe40e7007c0700');c.call(0x156da);c.abs('4239',0xa01f30);c.call(0x156fa);c.emit('46df4cdf7fff')
c.label('robot_stop_sound36_done');c.emit('4e75')
c.label('robot_attack_event36');c.emit('4a50');c.branch('6b00','robot_attack_event36_done');c.emit('0c500500');c.branch('6e00','robot_attack_event36_done');c.jump(c.labels['robot_attack_sound36'])
c.label('robot_attack_event36_done');c.emit('4e75')
# Sound Test adds24=robot footstep,25=robot attack after all original entries.
c.label('sound_test36');c.abs('3039',0xffff010a);c.emit('0c400018');c.branch('6700','sound_test36_step');c.emit('0c400019');c.branch('6700','sound_test36_attack');c.jump(V['sound_play14']+6)
c.label('sound_test36_step');c.jump(c.labels['robot_step_sound36'])
c.label('sound_test36_attack');c.jump(c.labels['robot_attack_sound36']);patch(V['sound_play14'],'sound_test36')
c.label('sound_stop36');c.call(c.labels['robot_stop_sound36']);c.emit(src[V['sound_stop14']:V['sound_stop14']+8].hex());c.jump(V['sound_stop14']+8);patch(V['sound_stop14'],'sound_stop36',8)
for lo,hi,needle,repl in [(S['options35_next4'],S['options35_soundright'],'7017','7019'),(S['options35_soundright'],S['options35_soundstore'],'0c400018','0c40001a')]:
 p=src.index(bytes.fromhex(needle),lo,hi);r[p:p+len(bytes.fromhex(needle))]=bytes.fromhex(repl)
c.label('sound_options_exit36');c.call(c.labels['robot_stop_sound36']);p=S['options35_exit'];c.emit(src[p:p+6].hex());c.jump(p+6);patch(p,'sound_options_exit36')
for p,name in [(S['capture_panel'],'panel_sound_stop36'),(V['sleep17_begin'],'sleep_sound_stop36')]:
 c.label(name);c.call(c.labels['robot_stop_sound36']);c.emit(src[p:p+6].hex());c.jump(p+6);patch(p,name)

c.label('robot_walk36');c.emit('30280028');c.call(0xce76);c.emit('e8493028003208390000');c.long(0xffff29ac);c.branch('6600','robot_walk36_phase');c.emit('e51831400032')
c.label('robot_walk36_phase');c.emit('02400018');c.branch('6600','robot_walk36_frame');c.abs('4a39',0xffff0804);c.branch('6600','robot_walk36_frame');c.emit('4a50');c.branch('6b00','robot_walk36_frame');c.emit('0c500500');c.branch('6e00','robot_walk36_frame');c.call(c.labels['robot_step_sound36'])
c.label('robot_walk36_frame');c.emit('d041d068001e314000204e75')
