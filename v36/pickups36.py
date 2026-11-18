# Each record is campaign, native floor, atlas X/Y, world cell type.
pickups36=[tuple(map(int,line.split(','))) for line in (OUT/'pickups36.csv').read_text().splitlines()]
for camp,f,x,y,kind in pickups36:
    base=(assets['mission_items'] if camp else 0x10ddc)+48*f
    assert all((r[p],r[p+1])!=(x,49-y) for p in range(base,base+48,3) if r[p+2])
    p=next(p for p in range(base,base+48,3) if not r[p+2])
    r[p:p+3]=bytes([x,49-y,kind])

def add_legacy_pickups36():
    # Entered only from the validated X21 restore with SRAM still mapped.
    c.call(c.labels['sram_audio_addr33'])
    c.emit('0c1300b4');c.branch('6700','pickup_restore_done36')
    for camp in (0,1):
        tag=f'pickups_camp{camp}'
        tstcamp();c.branch('6600' if not camp else '6700',tag)
        for n,(_,f,x,y,kind) in enumerate(q for q in pickups36 if q[0]==camp):
            t=f'{tag}_{n}'
            c.abs('41f9',0xffff2a3a+48*f);c.emit('93c97e0f') # A1=first empty entry
            c.label(t+'_loop')
            c.emit('4a280002');c.branch('6600',t+'_occupied')
            c.emit('2009');c.branch('6600',t+'_advance')
            c.emit('2248');c.branch('6000',t+'_advance')
            c.label(t+'_occupied')
            # Entries are packed at stride 3. Only read or write bytes.
            c.emit(f'0c1000{x:02x}');c.branch('6600',t+'_advance')
            c.emit(f'0c2800{49-y:02x}0001');c.branch('6700',t+'_done')
            c.label(t+'_advance')
            c.emit('5688');c.branch('51cf',t+'_loop')
            c.emit('2009');c.branch('6700',t+'_done')
            c.emit(f'12fc00{x:02x}12fc00{49-y:02x}12bc00{kind:02x}')
            c.label(t+'_done')
        c.label(tag)
    c.label('pickup_restore_done36')

def hook_legacy_pickups36():
    p=0xf8630
    assert r[p:p+8]==bytes.fromhex('13fc000000a130f1')
    c.label('pickup_restore36')
    add_legacy_pickups36()
    c.emit(src[p:p+8].hex());c.jump(p+8)
    patch(p,'pickup_restore36',8)
