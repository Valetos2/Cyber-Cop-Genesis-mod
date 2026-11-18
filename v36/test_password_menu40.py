"""Run password screen dispatch, history, and hold behavior on the 68000."""
exec(open('v36/test_core.py').read().split('levels=json')[0])
edit,cache=0xffff2580,0xffff25e8
count=0xffff257e
previous=0xffff0006
u=machine()
u.mem_write(0x150d8,b'\x4e\x75')
def held_action(x,y,held=False,end=0xcea):
    w(u,0xffff29c8,x);w(u,0xffff29ce,y)
    w(u,previous,0xef if held else 0xff)
    run(u,0xd3c,end)
run(u,0xa82);run(u,0xa8c);w(u,count,0)
held_action(0x100,0xb8)
assert rd(u,count)==1
held_action(0x100,0xb8,True)
held_action(0x128,0xd8)
assert rd(u,count)==1 and bytes(u.mem_read(edit,2))==b'a.'
held_action(0x128,0x118,True)
assert rd(u,count)==0 and bytes(u.mem_read(edit,1))==b'.'
held_action(0x128,0x168,end=0xf46)
run(u,0xf6dce,0xf46)
p=b'ak'*12
u.mem_write(edit,p)
w(u,count,24)
held_action(0x128,0x168,end=0xf4a)
run(u,0xf4a,0xf5e)
run(u,0xa8c);w(u,count,0)
held_action(0x128,0xd8,True)
assert rd(u,count)==0
held_action(0x128,0xd8)
assert rd(u,count)==24 and bytes(u.mem_read(edit,24))==p
held_action(0x128,0x118)
held_action(0x128,0x118,True)
assert rd(u,count)==22
held_action(0x128,0x168,end=0xeba)  # partial/invalid entry still goes to the error
assert bytes(u.mem_read(cache,24))==p
print('PASS password UI: empty Enter/Start, history, invalid partial input, key edge, repeated backspace')
# Reset initializes both old session RAM and the new sentinel.
run(u,0x291c,0x292e)
run(u,0xa82)
assert bytes(u.mem_read(cache,24))==bytes(24)
