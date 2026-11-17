exec(open('v36/test_core.py').read().split('levels=json')[0])
import sys

FLOOR, ACCESS, LATCH, HISTORY = 0xffff2606, 0xffff26bc, 0xffff216e, 0xffff2718

def fresh(rom):
    u = machine(rom)
    u.mem_write(0xffff0000, bytes(65536))
    # Leave game logic intact; skip only display sync and full scene redraw.
    for a in (0x2930, 0x1602, 0x33b6, 0xffbe, 0x1646):
        u.mem_write(a, b'\x4e\x75')
    return u

def terminal(u):
    run(u, 0x7d76, 0x7db2)
    return rd(u, ACCESS) // 32

def ride(u, target, arrival):
    w(u, 0xffff218e, target)
    u.reg_write(UC_M68K_REG_D0, target)
    run(u, 0x8e7a)
    assert rd(u, 0xffff7dca) == 0xb1
    u.reg_write(UC_M68K_REG_D0, target)
    run(u, 0x8e22, 0x8e50)
    assert rd(u, FLOOR) == arrival

def new_game_checkpoint(rom):
    u = fresh(rom)
    run(u, 0x2360)
    run(u, 0x2944)
    run(u, 0x4832)
    assert rd(u, FLOOR) == 0 and rd(u, ACCESS) == 0
    u.mem_write(0x200000, b'\xff' * 0x4000)
    assert terminal(u) == 1
    ride(u, 2, 1)  # 5F -> 4F, uses real acceptance and arrival routines
    return bytes(u.mem_read(0x200000, 0x4000)), rd(u, 0xffff25a4, 1) & 4

def cold_resume(rom, sram):
    u = fresh(rom)  # no gameplay RAM or CPU state from the previous instance
    u.mem_write(0x200000, sram)
    run(u, S['resume_original36'], 0x124a)
    assert rd(u, FLOOR) == 1 and rd(u, ACCESS) == 32
    run(u, 0x1fb4, 0x1fc2)
    assert list(u.mem_read(HISTORY, 2)) == [255, 0]
    return u

sram, bit = new_game_checkpoint(R)
assert bit == 0
u = cold_resume(R, sram)
assert rd(u, LATCH) == 0 and terminal(u) == 2
w(u, LATCH, 0)  # Repeat visit must still be refused by per-floor history.
assert terminal(u) == 2

if len(sys.argv) == 2:
    prior = Path(sys.argv[1]).read_bytes()
    old_sram, bit = new_game_checkpoint(prior)
    assert bit == 4
    u = cold_resume(prior, old_sram)
    assert rd(u, LATCH) == 0xffff and terminal(u) == 1
    w(u, 0xffff2712, 0, 1)  # the initial restore has finished
    ride(u, 0, 0)
    ride(u, 2, 1)
    assert terminal(u) == 2
    u = cold_resume(prior, old_sram)
    w(u, 0xffff2712, 0, 1)
    ride(u, 2, 1)  # Same-floor trip also reinitializes the latch.
    assert terminal(u) == 2
    v = cold_resume(R, old_sram)
    assert rd(v, LATCH) == 0 and terminal(v) == 2
    print('PASS reproduction and migration of the old checkpoint')

u = fresh(R)
w(u, 0xffff2712, 255, 1)
w(u, LATCH, 0xffff)
run(u, 0x1fbc, 0x1fc2)
assert rd(u, LATCH) == 0xffff  # native password without X21 metadata
print('PASS 5F access, real 4F elevator save, cold Continue, 4F access, no duplicate award')
