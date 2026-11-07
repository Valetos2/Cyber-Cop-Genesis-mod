# Zero means enabled, matching the reset-cleared extension state.
LIGHTS_OFF=0xffff0856
c.label('light_queue36c');c.abs('4a39',LIGHTS_OFF);c.branch('6600','light_queue_done36c');c.emit(src[0xcfc8:0xcfce].hex());c.jump(0xcfce);c.label('light_queue_done36c');c.emit('4e75');patch(0xcfc8,'light_queue36c')
# Options adds one stable row between stripe and mouse.
lo=S['options35_max'];hi=S['options35_maxdone']
for old,new in [('7405','7406'),('7406','7407'),('7407','7408')]:
 needle=bytes.fromhex(old);assert src[lo:hi].count(needle)==1;p=src.index(needle,lo,hi);r[p:p+2]=bytes.fromhex(new)
lo=S['options35_draw'];hi=S['options35_arrow']
for old in [0xe70e,0xe734,0xe80e,0xe90e]:
 needle=bytes.fromhex('363c')+struct.pack('>H',old)
 start=lo
 while True:
  p=src.find(needle,start,hi)
  if p<0:break
  r[p+2:p+4]=struct.pack('>H',old+0x100);start=p+4
needle=bytes.fromhex('0c420005');p=src.index(needle,lo,hi);r[p+2:p+4]=bytes.fromhex('0006')
p=src.index(bytes.fromhex('68300003'),S['front_slider35'],S['front_slider35_names']);r[p:p+4]=bytes.fromhex('69300003')
c.label('options_lamps_action36c');c.emit('0c410005');c.branch('6600','options_lamps_mouse36c');c.emit('0244007c');c.branch('6700','options_lamps_loop36c');c.emit('0a3900ff');c.long(LIGHTS_OFF);c.jump(S['options35_redraw'])
c.label('options_lamps_loop36c');c.jump(S['options35_loop'])
c.label('options_lamps_mouse36c');c.emit('0c410006');c.branch('6600','options_lamps_sens36c');c.jump(S['options35_not_dither']+8)
c.label('options_lamps_sens36c');c.jump(S['options35_sensitivity']);patch(S['options35_not_dither'],'options_lamps_action36c',8)
c.label('options_lamps_draw36c');draw('lamps',0xe70e);c.abs('4a39',LIGHTS_OFF);c.branch('6600','options_lamps_off36c');draw('on ',0xe734);c.branch('6000','options_lamps_drawn36c');c.label('options_lamps_off36c');draw('off',0xe734);c.label('options_lamps_drawn36c');c.call(S['options35_max']);c.jump(S['options35_arrow']+6);patch(S['options35_arrow'],'options_lamps_draw36c')
# Clear the extra bottom row before the existing complete redraw.
c.label('options_clear36c');draw(' '*26,0xea0e);c.emit(src[S['options35_draw']:S['options35_draw']+10].hex());c.jump(S['options35_draw']+10);patch(S['options35_draw'],'options_clear36c',10)
# Sleep keeps IDs0..10; lamps use11. Move the first four text rows up16px.
c.label('sleep_lamps_draw36c');c.emit('7000');c.abs('1039',P+44);c.emit('0c400004');c.branch('6500','sleep_lamps_first36c');c.emit('0c400009');c.branch('6500','sleep_lamps_draw_native36c')
c.label('sleep_lamps_first36c');c.abs('41f9',0xffff89b4);c.abs('43f9',0xffff8974);c.emit('7c17')
c.label('sleep_lamps_column36c');c.emit('7e37');c.label('sleep_lamps_copy36c');c.emit('22d8');c.branch('51cf','sleep_lamps_copy36c');c.emit('7e17');c.label('sleep_lamps_clear36c');c.emit('4299');c.branch('51cf','sleep_lamps_clear36c');c.emit('41e8012043e900c0');c.branch('51ce','sleep_lamps_column36c')
# Sparse font overlay, preserving the original on/off and dither text above.
for off in [0,1]:
 patches=[];words=[('lamps',8),('off' if off else 'on ',128)]
 for text,x0 in words:
  for j,ch in enumerate(text):
   tile=0 if ch==' ' else ord(ch)-96
   for y in range(8):
    for x in range(0,8,2):
     val=src[0x30716+tile*32+y*4+x//2];val=(240 if val>>4 else 0)|(15 if val&15 else 0)
     x1=x0+j*8+x;offset=x1//8*512+(80+y)*4+x1%8//2;patches.append((offset,val))
 ptr=asset('sleep_lamps_text36c_'+str(off),b''.join(struct.pack('>HH',a,b) for a,b in patches))
 if off==0:c.abs('41f9',ptr);c.abs('4a39',LIGHTS_OFF);c.branch('6700','sleep_lamps_overlay36c')
 else:c.abs('41f9',ptr)
c.label('sleep_lamps_overlay36c');c.abs('43f9',0xffff8934);c.emit('3e3c'+f'{len(patches)-1:04x}')
c.label('sleep_lamps_overlay_loop36c');c.emit('3018321813810000');c.branch('51cf','sleep_lamps_overlay_loop36c')
c.label('sleep_lamps_draw_native36c');c.emit(src[S['sleep_arrow03']:S['sleep_arrow03']+8].hex());c.jump(S['sleep_arrow03']+8);patch(S['sleep_arrow03'],'sleep_lamps_draw36c',8)
c.label('sleep_lamps_arrow36c');c.emit('0c39000b');c.long(P+44);c.branch('6600','sleep_lamps_arrow_old36c');c.emit('303c00c0');c.jump(0xf71ea)
c.label('sleep_lamps_arrow_old36c');c.emit('0c390004');c.long(P+44);c.branch('6400','sleep_lamps_arrow_done36c');c.emit('04400040');c.label('sleep_lamps_arrow_done36c');c.jump(0xf71ea);patch(S['arrow05_draw'],'sleep_lamps_arrow36c')
# Joystick navigation uses an explicit visible order, preserving native actions.
navptrs=[]
for present,on in [(0,0),(1,0),(1,1)]:
 order=[0,1,2,3,11]+([9] if present else [])+([10] if present and on else [])+[4,5,6,7,8]
 navptrs.append(asset('sleep_lamps_nav36c_'+str(len(navptrs)),bytes([len(order)]+order)))
c.label('sleep_lamps_nav36c');c.emit('7000');c.abs('1039',0xffff0119);c.emit('320402410003');c.branch('6700','sleep_lamps_action36c')
c.abs('41f9',navptrs[0]);c.abs('4a79',P+38);c.branch('6700','sleep_lamps_nav_table36c');c.abs('41f9',navptrs[1]);c.abs('4a79',P);c.branch('6700','sleep_lamps_nav_table36c');c.abs('41f9',navptrs[2])
c.label('sleep_lamps_nav_table36c');c.emit('740014187200')
c.label('sleep_lamps_find36c');c.emit('b0301000');c.branch('6700','sleep_lamps_found36c');c.emit('5241b242');c.branch('6500','sleep_lamps_find36c');c.emit('7200')
c.label('sleep_lamps_found36c');c.emit('08040000');c.branch('6700','sleep_lamps_down36c');c.emit('5341');c.branch('6a00','sleep_lamps_store36c');c.emit('32025341');c.branch('6000','sleep_lamps_store36c')
c.label('sleep_lamps_down36c');c.emit('5241b242');c.branch('6500','sleep_lamps_store36c');c.emit('7200')
c.label('sleep_lamps_store36c');c.emit('10301000');c.abs('13c0',0xffff0119);c.jump(V['sleep16_changed'])
c.label('sleep_lamps_action36c');c.emit('0c40000b');c.branch('6600','sleep_lamps_action_native36c');c.emit('0244007c');c.branch('6700','sleep_lamps_still36c');c.emit('0a3900ff');c.long(LIGHTS_OFF);c.jump(V['sleep16_changed'])
c.label('sleep_lamps_still36c');c.jump(V['sleep16_show']);c.label('sleep_lamps_action_native36c');c.jump(S['sleep_input']);patch(S['sleep_nav04'],'sleep_lamps_nav36c',8)
# Mouse first-page rows begin at screenY24; gaps remain inert.
c.label('sleep_lamps_click36c');c.abs('3239',N+6);c.emit('0c410078');c.branch('6c00','sleep_lamps_slider36c');c.emit('044100180c410060');c.branch('6400','sleep_lamps_next36c');c.emit('34010242000f0c420008');c.branch('6400','sleep_lamps_click_done36c');c.emit('e8490c410004');c.branch('6500','sleep_lamps_row36c');c.branch('6600','sleep_lamps_mouse_row36c');c.emit('720b');c.branch('6000','sleep_lamps_row36c')
c.label('sleep_lamps_mouse_row36c');c.abs('4a79',P+38);c.branch('6700','sleep_lamps_next36c');c.emit('7209')
c.label('sleep_lamps_row36c');c.emit('0c41000b');c.branch('6600','sleep_lamps_oldrow36c');c.abs('3439',N+4);c.emit('044200480c4200a0');c.branch('6400','sleep_lamps_next36c');bi(0xffff0119,11);c.emit('0a3900ff');c.long(LIGHTS_OFF);c.jump(S['sleep_click_changed'])
c.label('sleep_lamps_oldrow36c');c.jump(S['sleep_row']);c.label('sleep_lamps_slider36c');c.jump(S['sleep_slider04']);c.label('sleep_lamps_next36c');c.jump(S['sleep_next_page']);c.label('sleep_lamps_click_done36c');c.emit('4e75');patch(S['sleep_page0'],'sleep_lamps_click36c',8)
