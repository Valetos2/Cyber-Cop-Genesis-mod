# Link loss changes the usable state, not the player's Mouse Off preference.
LINK_DISABLED=0xffff0866
MOUSE_PRESENT=0xffff0192

c.label('mouse_reconcile13')
c.abs('4a39',MOUSE_PRESENT);c.branch('6600','mouse_connected13')
c.abs('4a79',P);c.branch('6700','mouse_missing_off13')
bi(LINK_DISABLED,1)
c.branch('6000','mouse_missing_clear13')
c.label('mouse_missing_off13')
c.abs('4a79',P+38);c.branch('6700','mouse_reconcile_done13')
c.label('mouse_missing_clear13')
c.abs('4279',P);c.abs('4279',P+38)
c.call(S['mouse_toggle05']);c.abs('4279',P+70)
c.emit('0c390009ffff0119');c.branch('6500','mouse_link_redraw13')
bi(0xffff0119,11) # Lamps is the last remaining normal row.
c.branch('6000','mouse_link_redraw13')
c.label('mouse_connected13')
c.abs('4a39',LINK_DISABLED);c.branch('6700','mouse_present_only13')
c.abs('4239',LINK_DISABLED);c.abs('4279',P+70);wi(P,1);sleep_owner_clear()
c.branch('6000','mouse_mark_present13')
c.label('mouse_present_only13')
c.abs('4a79',P+38);c.branch('6600','mouse_reconcile_done13')
c.label('mouse_mark_present13');wi(P+38,1)
c.label('mouse_link_redraw13');c.jump(S['detect04_refresh'])
c.label('mouse_reconcile_done13');c.emit('4e75')
p=S['detect04']
assert r[p:p+6]==bytes.fromhex('4a39ffff0192')
patch(p,'mouse_reconcile13')

# Options used to set P+38 itself, losing the reconnect event before gameplay
# saw it. Run the same reconciliation here, then count the visible rows.
p=S['options35_max']
assert r[p:p+8]==bytes.fromhex('74064a39ffff0192')
q=S['options35_maxdone']
needle=bytes.fromhex('33fc0001ffff0226')
i=r.index(needle,p,q)
r[i:i+8]=bytes.fromhex('4e71')*4
c.label('mouse_options_link13')
c.emit('48e7fffe');c.call(S['detect04']);c.emit('4cdf7fff')
c.emit(r[p:p+8].hex());c.jump(p+8)
patch(p,'mouse_options_link13',8)

# TL can already be high on the first two phases. If the first sample has
# the old nibble, give the lines a few reads to settle with TH/TR held.
# Once the transaction has begun, the existing bounded TL waits still apply.
for p,value,resume,op in [(0x18019a,0,0x1801a0,'4a4266000132'),
                          (0x1801b0,11,0x1801b8,'0c42000b6600011a')]:
 assert r[p:resume]==bytes.fromhex(op),(hex(p),r[p:resume].hex())
 label='mouse_header13_'+str(value)
 c.label(label)
 c.emit('0c42'+f'{value:04x}');c.branch('6700',label+'_ready')
 c.emit('2f057a07') # preserve D5, use an independent bounded wait
 c.label(label+'_poll')
 c.emit('14100242001f0c42'+f'{(0x10|value):04x}')
 c.branch('6700',label+'_stable')
 c.branch('51cd',label+'_poll')
 c.emit('2a1f');c.jump(0x1802d0)
 c.label(label+'_stable');c.emit('2a1f0242000f')
 c.label(label+'_ready');c.jump(resume)
 patch(p,label,resume-p)
