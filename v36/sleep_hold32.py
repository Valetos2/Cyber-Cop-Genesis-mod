"""Hold the mouse sleep icon for the same six VBlanks in both directions."""
c.label('sleep_icon_hold32')
c.call(S['feedback07'])
# Preserve the native dispatcher's node and registers across frame waits.
c.emit('40e748e7fffe')
c.abs('0cb9',0x561c);c.long(N+20) # cmpi.l #sleep node,(owner)
c.branch('6600','sleep_hold32_end')
c.emit('0c790001');c.long(P+2)
c.branch('6600','sleep_hold32_end')
# feedback07 already presented frame 1. Wait for five more pressed frames.
c.emit('7e04') # moveq #4,d7
c.label('sleep_hold32_frames')
c.emit('2f07') # move.l d7,-(sp)
c.call(0x2930)
c.emit("2e1f") # move.l (sp)+,d7
c.branch('51cf','sleep_hold32_frames') # dbra d7
# Leave ownership available for the original entry dispatcher ($18379A).
# Keep the uploaded slot until the next VBlank restores its name entries.
c.abs('4279',P+2)
c.abs('4279',P+32)
c.call(0x2930)
c.label('sleep_hold32_end')
c.emit('4cdf7fff46df4e75')
for p in (0x183794,0x183ab6):
    assert r[p:p+6]==bytes.fromhex('4eb900184c10')
    r[p:p+6]=bytes.fromhex('4eb9')+struct.pack('>I',c.labels['sleep_icon_hold32'])
