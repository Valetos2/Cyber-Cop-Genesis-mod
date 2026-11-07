exec(open('v36/test_core.py').read().split('levels=json')[0])
u=machine();w(u,0xffff7d20,0xa00e58,4);w(u,0xffff7d2a,0);w(u,0xffff2711,0,1)
run(u,S['robot_attack_sound36']);assert rd(u,0xa01f30,1)==255 and rd(u,0xffff0804,1)==255
assert bytes(u.mem_read(0xa00e68,8))==bytes([0,0x1e,205,0,192,0,255,0])
run(u,S['robot_stop_sound36']);assert rd(u,0xa01f30,1)==0 and rd(u,0xffff0804,1)==0
run(u,S['robot_step_sound36']);assert bytes(u.mem_read(0xa00e68,6))==bytes([0,0x1c,153,0,0xee,1])
run(u,S['robot_attack_sound36']);run(u,0x155a6);assert rd(u,0xa01f30,1)==0
assert bytes(u.mem_read(0xa00e68,6))==bytes([8,0x12,44,0,0x3d,9])
# Source sample and pre-existing boot code remain unchanged except the explicit
# end-of-sample jump. The new samples do not overlap the old sample or each other.
b=R[S['z80_driver36']:S['z80_driver36']+0x1400];old=OLD[0x157a8:0x16ba8]
assert b[0x608:0xf45]==old[0x608:0xf45]
A=Path('amiga3/mission.bin').read_bytes();assert b[0x1000:0x11ee]==bytes(x^128 for x in A[0x2e520:0x2e70e]);assert b[0x1200:0x12c0]==bytes(x^128 for x in A[0x32078:0x32138])
print('PASS PCM sample placement/sign, driver parameters, loop start/stop, restoration of original PCM request')
