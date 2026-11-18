# N is forced to pointer mode while in sleep. Take a snapshot at the common
# sleep entry, before the first sleep input or fade, rather than at menu open.
SLEEP_VIEW=0xffff0868  # 0: no saved mode, 1: free look, 2: pointer
p=0x6fb2
assert r[p:p+6]==bytes.fromhex('4ef9')+struct.pack('>I',V['sleep17_begin'])
c.label('sleep_save_view14')
c.abs('4239',SLEEP_VIEW);c.abs('4239',START_WAKE_PENDING)
c.abs('4a79',P);c.branch('6700','sleep_enter_native14')
c.abs('4a39',0xffff0192);c.branch('6700','sleep_enter_native14')
c.abs('4a79',N);c.branch('6600','sleep_save_pointer14')
bi(SLEEP_VIEW,1);c.branch('6000','sleep_enter_native14')
c.label('sleep_save_pointer14');bi(SLEEP_VIEW,2)
c.label('sleep_enter_native14');c.jump(V['sleep17_begin'])
patch(p,'sleep_save_view14')

# Wake can come from Start, Mode, the mouse button or the sleep icon.
# Keep the native wake redraw, and suppress any still-held mouse UI buttons.
p=0x7108
assert r[p:p+6]==bytes.fromhex('51f9ffff270e')
c.label('sleep_restore_view14')
c.emit(src[p:p+6].hex())
c.abs('4a79',P);c.branch('6700','wake_clear_view14')
c.abs('4a39',0xffff0192);c.branch('6700','wake_clear_view14')
c.abs('4a39',SLEEP_VIEW);c.branch('6700','wake_clear_view14')
c.emit('0c390002');c.long(SLEEP_VIEW);c.branch('6700','wake_pointer14')
c.abs('4279',N);c.branch('6000','wake_guard14')
c.label('wake_pointer14');wi(N,1)
c.label('wake_guard14')
wi(P+90,1)
c.abs('42b9',N+24);c.abs('42b9',N+28)
c.label('wake_clear_view14');c.abs('4239',SLEEP_VIEW);c.jump(p+6)
patch(p,'sleep_restore_view14')
