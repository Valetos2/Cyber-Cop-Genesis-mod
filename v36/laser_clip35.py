# Clip laser quads horizontally before passing them to the stock span filler.
# Offscreen endpoints can make the filler's flat middle rectangle span the
# viewport even though the corresponding real sloping edge is visible.
p=0xe370
assert r[p:p+8]==bytes.fromhex('33c0ffff26906008')
c.label('laser_clip35');c.emit(src[p:p+6].hex())
c.emit(src[0xe380:0xe3b0].hex())  # fill (A1) with projected quad
c.emit('48e7fffe')
for i,(one,other) in enumerate([(0,4),(4,0)]):
    tag=f'laser35_{i}_'
    c.emit(f'3029{one:04x}3229{other:04x}4a40');c.branch('6a00',tag+'right')
    c.emit('4a41');c.branch('6b00','laser_empty35');c.emit('7400');c.branch('6000',tag+'clip')
    c.label(tag+'right');c.emit('0c4000bf');c.branch('6f00',tag+'done')
    c.emit('0c4100bf');c.branch('6e00','laser_empty35');c.emit('343c00bf')
    c.label(tag+'clip')
    c.emit('360296409240') # d3=boundary-x0; d1=x1-x0
    c.branch('6900','laser_draw35')
    for off in (2,10):
        c.emit(f'3829{other+off:04x}9869{one+off:04x}')
        c.branch('6900','laser_draw35')
        c.emit(f'c9c389c1d869{one+off:04x}3344{one+off:04x}')
    c.emit(f'3342{one:04x}3342{one+8:04x}')
    c.label(tag+'done')
c.label('laser_draw35');c.emit('4cdf7fff');c.jump(0xe4d0)
c.label('laser_empty35');c.emit('4cdf7fff4e75')
patch(p,'laser_clip35',8)
