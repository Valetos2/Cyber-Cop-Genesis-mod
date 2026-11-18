"""Extend the audio record in the same campaign bank; publish version last."""
fields34=[(FUSE_WORDS,28),(FUSE_TICK,2),(0xffff0134,3)]
def fuse_fields34(read):
    c.emit('49eb000a') # lea 10(a3),a4; first free odd byte
    for addr,n in fields34:
        c.abs('41f9',addr);c.emit(f'7e{n-1:02x}')
        loop='fuse_field34_'+str(addr)+read;c.label(loop)
        if read=='write':
            c.emit('10181880460019400002') # byte and complement
        elif read=='check':
            c.emit('10144600b02c0002');c.branch('6600','fuse_bad34')
        else:c.emit('10d4') # (a4),(a0)+
        c.emit('584c');c.branch('51cf',loop)
