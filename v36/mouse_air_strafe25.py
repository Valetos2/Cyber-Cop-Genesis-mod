# Permit the existing strafe branch in the air when a real enabled mouse is
# present. Mouse Off keeps its stock jump movement and A gesture.
p=0xf8f2e
assert r[p:p+12]==bytes.fromhex('3039ffff441cb079ffff4440')
c.label('air_strafe25')
c.abs('4a79',P);c.branch('6700','air_strafe_pad25')
c.abs('4a39',0xffff0192);c.branch('6600','air_strafe_mouse25')
c.label('air_strafe_pad25');c.emit(r[p:p+12].hex());c.jump(p+12)
c.label('air_strafe_mouse25');c.jump(0xf8f3e)
patch(p,'air_strafe25',12)
