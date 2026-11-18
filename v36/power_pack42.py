# Preclosing another panel clears native pad inventory mode. Only retain
# that byte for the Power Pack transition, without touching actual exits.
site = S['open09_82ec']
assert r[site:site+6] == bytes.fromhex('4eb9') + struct.pack('>I', S['preopen09'])
c.label('power_pack_preopen42')
c.abs('4a79', 0xffff0200)
c.branch('6600', 'power_pack_mouse42')
c.abs('1f39', 0xffff270a)  # move.b inventory,-(sp)
c.call(S['preopen09'])
c.abs('13df', 0xffff270a)  # move.b (sp)+,inventory
c.jump(site+6)
c.label('power_pack_mouse42')
c.call(S['preopen09'])
c.jump(site+6)
patch(site,'power_pack_preopen42')
