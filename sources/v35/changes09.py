# Native inventory freezes the movement input path but leaves the old speed.
c.label('stop_inventory09');c.emit('4e75')
# Close any previous interactive panel before changing its graphics bank/layout.
# P+104 prevents a temporary close from ending the original mouse-mode lifetime.
c.label('preopen09');c.emit('48e7fffe');clear(P+96);tst(0xffff26e2,True);branch('6700','preopen09_done');ld(0,0xffff26b8,True);c.emit('0c8000002106');branch('6700','preopen09_done');c.emit('0c8000007070');branch('6700','preopen09_done');wi(P+104,1);c.call(0x2190);clear(P+104);clear(N+40,True);clear(N+20,True);clear(P+12,True);clear(P+8,True);clear(P+40)
c.label('preopen09_done');c.emit('4cdf7fff4e75')
for pc in [0x943e,0x771c,0x7b86,0x8a74,0x8c78,0x8728,0x82ec,0x7a00]:
 label='open09_'+hex(pc)[2:];c.label(label);call('preopen09');c.emit('48e7fffe');call('panel_enter08');c.emit('4cdf7fff');c.emit(source[pc:pc+6].hex());c.jump(pc+6);hook(pc,label)
# Bomb's existing opener has its own setup; call preopen before its bank/layout load.
# (The call is inserted directly in extension.py.)
c.label('code_success09');c.emit('0cb900009916');c.address(0xffff26b8);branch('6600','success09_native');wi(P+96,1)
c.label('success09_native');c.emit(source[0x9b2a:0x9b34].hex());c.jump(0x9b34);hook(0x9b2a,'code_success09',10)
c.label('code_fail09');clear(P+96);c.emit('0cb9000077a8');c.address(0xffff26b8);branch('6600','fail09_native');bi(0xffff26ec,0);c.emit('32bc00b3')
c.label('fail09_native');c.jump(int.from_bytes(source[0x9b40:0x9b44],'big'));hook(0x9b3e,'code_fail09')
c.label('code_green09');tst(P+96);branch('6700','green09_done');c.emit('0cb900009916');c.address(0xffff26b8);branch('6600','green09_done');c.abs('2279',0xffff227e);c.abs('d2f9',0xffff223e);c.emit('93fc00000048');c.emit('0c5100b1');branch('6700','green09_done');c.emit('32bc00b1');bi(0xffff2700,255)
c.label('green09_done');c.emit('4e75')
c.label('key_confirm_draw09');c.call(0x38c8);c.call(0x4d18);c.emit('303c0ae0');c.jump(0x9b5a);hook(0x9b52,'key_confirm_draw09',8)
# Circle mask derived geometrically from the original 16x16 floor-button footprint.
# Matching panel-background pixels inside the mask are included intentionally.
mask={}
for y in range(2,15):
 lo,hi=({2:(5,9),3:(3,11),4:(2,12),12:(2,12),13:(3,11),14:(5,9)}.get(y,(1,13)))
 for x in range(lo,hi+1):
  off=x//8*512+y*4+(x%8)//2;mask[off]=mask.get(off,0)|(1 if x%2==0 else 2)
records=[off+({3:0,1:0x4000,2:0x8000}[nibbles]) for off,nibbles in sorted(mask.items())]
r[0x19f000:0x19f000+len(records)*2]=b''.join(x.to_bytes(2,'big') for x in records)
def dark09(v):return v-1 if 3<=v<=7 else v
lut=bytearray()
for which in [3,1,2]:
 for val in range(256):lut.append(((dark09(val>>4) if which&1 else val>>4)<<4)|(dark09(val&15) if which&2 else val&15))
r[0x19f200:0x19f500]=lut
c.label('circle_shade09');c.emit('302a000804400041322a000c04410009');call('pixel_address');c.abs('23c8',P+100);wi(P+98,1);c.abs('45f9',0x19f000);c.abs('47f9',0xffff0700);c.abs('49f9',0x19f200);c.emit('3e3c'+f'{len(records)-1:04x}')
c.label('circle09_loop');c.emit('341a320202413fff');c.abs('2279',P+100);c.emit('d2c17000101116c0');c.emit('0242c000');branch('6700','circle09_apply');c.emit('ec4a');c.emit('d042')
c.label('circle09_apply');c.emit('12b4000051cf');c.fix.append((len(c.b),'circle09_loop',2));c.emit('00004e75')
c.label('circle_restore09');clear(P+98);c.abs('45f9',0x19f000);c.abs('47f9',0xffff0700);c.emit('3e3c'+f'{len(records)-1:04x}')
c.label('circle09_restore_loop');c.emit('321a02413fff');c.abs('2279',P+100);c.emit('d2c112db51cf');c.fix.append((len(c.b),'circle09_restore_loop',2));c.emit('00004e75')
# Success applies only while that keypad is visible, never during world restoration.
c.label('close_begin09');clear(P+96);c.emit(source[0x2190:0x2198].hex());c.jump(0x2198);hook(0x2190,'close_begin09',8)
