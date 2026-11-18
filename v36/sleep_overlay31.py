# The mouse sleep icon presents its pressed frame before this wake jump.
# Retire the click's HUD owner now, so the next VBlank restores the normal
# tiles instead of uploading the pressed icon again during the wake redraw.
p=0x183abc
assert r[p:p+6]==bytes.fromhex('4ef90000709a')
c.label('sleep_overlay_wake31')
c.abs('42b9',N+20)
c.abs('4279',P+2)
c.abs('4279',P+32)
# Keep the uploaded slot until hud_draw restores its original name entries.
c.jump(0x709a)
patch(p,'sleep_overlay_wake31')
