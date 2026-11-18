# Raw controller snapshots feed the existing VBlank event words $0148/$014A.
# Release is confirmed across two samples; a press is still immediate.
# An invalid six-button identification response is not a release. Allow the
# extended bank to expire after six invalid responses (3-button swap/unplug).
PAD_PREV_RAW=0xffff0874
PAD_EXT_RAW=0xffff0876
PAD_EXT_INVALID=0xffff0878
p=0xf9190
assert r[p:p+8]==bytes.fromhex('4a43670000047400')
c.label('pad_release24')
c.emit('48e70c00') # D4-D5
c.emit('3800')
c.emit('0c3900a6ffff014e');c.branch('6600','pad_basic_save24')
c.abs('3a39',PAD_PREV_RAW)
c.abs('8a79',0xffff0140)
c.emit('0045ff4fc045') # debounce B/C/Start, leave A/D-pad intact
c.label('pad_basic_save24');c.abs('33c4',PAD_PREV_RAW)
c.emit('4a43');c.branch('6700','pad_ext_valid24')
c.emit('0c790006');c.long(PAD_EXT_INVALID);c.branch('6400','pad_ext_clear24')
c.abs('5279',PAD_EXT_INVALID)
c.emit('0c790006');c.long(PAD_EXT_INVALID);c.branch('6400','pad_ext_clear24')
c.abs('3439',0xffff0144);c.branch('6000','pad_release_done24')
c.label('pad_ext_clear24');c.emit('7400');c.branch('6000','pad_ext_filter24')
c.label('pad_ext_valid24');c.abs('4279',PAD_EXT_INVALID)
c.label('pad_ext_filter24')
c.abs('3839',PAD_EXT_RAW)
c.abs('33c2',PAD_EXT_RAW)
c.emit('0c3900a6ffff014e');c.branch('6600','pad_release_done24')
c.abs('c879',0xffff0144)
c.emit('8444')
c.label('pad_release_done24')
c.emit('4cdf0030');c.jump(p+8)
patch(p,'pad_release24',8)

# Mark the dispatched extended edges as consumed in the legacy view of the
# snapshot too, so re-entering a consumer cannot dispatch the same press.
# Keep the historical X/Z/Y priority and keep Mode's edge separate.
p=0xf01d6
assert r[p:p+6]==bytes.fromhex('3039ffff0012')
c.label('pad_items_read24')
c.emit(r[p:p+6].hex())
c.emit('00790007ffff0012')
c.jump(p+6)
patch(p,'pad_items_read24')
p=0xf0104
assert r[p:p+10]==bytes.fromhex('0cb900007070ffff26b8')
c.label('pad_mode_read24')
c.emit('00790008ffff0012')
c.emit(r[p:p+10].hex())
c.jump(p+10)
patch(p,'pad_mode_read24',10)

# The sleep renderer can span another input update. Preserve a physical Start
# press until the wake handler reads it rather than trusting the last snapshot.
p=0xf92b2
assert r[p:p+6]==bytes.fromhex('4279ffff0148')
c.label('pad_sleep_capture24')
c.emit('08020007');c.branch('6700','pad_sleep_capture_done24')
c.emit('0cb900007070ffff26b8');c.branch('6600','pad_sleep_capture_done24')
bi(START_WAKE_PENDING,1)
c.label('pad_sleep_capture_done24')
c.emit(r[p:p+6].hex());c.jump(p+6)
patch(p,'pad_sleep_capture24')

# World/sleep transitions reset the legacy game snapshot without resetting the
# physical pad. Do not let that synthetic release manufacture another press.
p=0xf92b8
assert r[p:p+6]==bytes.fromhex('3039ffff0004')
c.label('pad_primary_read24')
c.abs('3239',0xffff0140);c.emit('0041ff4f')
c.emit(r[p:p+6].hex())
c.emit('c041');c.jump(p+6)
patch(p,'pad_primary_read24')
p=0xf92e2
assert r[p:p+6]==bytes.fromhex('3239ffff0010')
c.label('pad_extended_read24')
c.emit(r[p:p+6].hex())
c.abs('8279',0xffff0144);c.jump(p+6)
patch(p,'pad_extended_read24')
