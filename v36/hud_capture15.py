# Capture-mode clicks are routed through the gamepad mapping, never through
# the HUD click dispatcher. A prior automatic Use selection is not ownership.
p=S['visual_update']
assert r[p:p+12]==bytes.fromhex('4279ffff02224279ffff0202')
c.label('hud_capture15')
c.emit(src[p:p+12].hex())
c.abs('4a79',N);c.branch('6700','hud_capture_clear15')
c.jump(p+12)
c.label('hud_capture_clear15')
c.abs('42b9',N+20)
c.jump(S['visual03_done'])
patch(p,'hud_capture15',12)
