exec(open('v36/test_core.py').read().split('levels=json')[0])

# Run the real intro skip into title setup, omitting its display sync call.
# The pending
# command is zero once consumed; STATE+34 remembers the last request.
for off, queued, last, position, wanted in [
    (0, 0, 2, 0x25, 0),    # theme already playing
    (0, 2, 2, 0, 2),       # theme queued: don't queue again
    (0, 0, 0, 0, 2),       # skip before the first theme request
    (255, 0, 1, 0, 0),     # disabled with no active music
    (255, 0, 2, 0x25, 1),  # disabled with an active song: stop it
]:
    u = machine()
    w(u, 0xffff2710, off, 1)
    w(u, 0xffff7d2a, 0)
    w(u, 0xffff7d2c, queued)
    w(u, 0xffff0122, last)
    w(u, 0xffff7d30, position)
    requests = []
    u.hook_add(UC_HOOK_MEM_WRITE, lambda *args: requests.append(1), begin=0xffff7d2c, end=0xffff7d2d)
    u.mem_write(0x26b8, bytes.fromhex('4e75'))
    run(u, V['intro_skip'], 0xf0432)
    assert rd(u, 0xffff7d2c) == wanted
    assert bool(requests) == (wanted != queued)

print('PASS intro music continuity and cold/muted starts')
