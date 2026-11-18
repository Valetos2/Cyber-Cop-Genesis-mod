exec(open('v36/test_core.py').read().split('levels=json')[0])
import sys
old = json.loads(Path('v35c/symbols.json').read_text())
M, P = 0xffff0180, 0xffff0200

def context(rom=R):
    u = machine(rom)
    w(u, M, 0x4d53)
    w(u, M+18, 255, 1)
    w(u, P, 1)
    w(u, P+38, 1)
    w(u, 0xffff26b8, 0x7070, 4)
    w(u, 0xffff0118, 1, 1)
    w(u, 0xffff0119, 9, 1)
    return u

def packet_port(u):
    # Model real register transactions, including missing device and a
    # delayed low nibble even after TL reads high on the first two phases.
    state = dict(present=True, phase=0x60, reads=0, delay=0, seq=0)
    nibbles = [0, 11, 15, 15, 0, 0, 0, 7, 0, 3]
    def io(uc, access, address, size, value, data):
        if access == UC_MEM_WRITE:
            if value == 0x60:
                state['seq'] = 0
            else:
                state['seq'] += 1
            state['phase'], state['reads'] = value, 0
        else:
            seq = state['seq']
            nibble = nibbles[seq]
            if not state['present'] or (seq <= 1 and state['reads'] < state['delay']):
                nibble = 15 if seq == 0 else 0
            state['reads'] += 1
            w(uc, address, nibble | ((state['phase'] >> 1) & 16), 1)
    u.hook_add(UC_HOOK_MEM_READ | UC_HOOK_MEM_WRITE, io, begin=0xa10005, end=0xa10005)
    return state

for misses in (1, 16, 29, 30, 45):
    u = context()
    link = packet_port(u)
    link['present'] = False
    for _ in range(misses):
        run(u, 0x18013c)
    run(u, old['detect04'])
    assert bool(rd(u, P)) == (misses < 30)
    if misses >= 30:
        assert rd(u, 0xffff0119, 1) == 11 and rd(u, P+4) == 1
    w(u, P+4, 0)
    link.update(present=True, delay=2)
    run(u, 0x18013c)
    if misses >= 30:
        # Reconnect seen by Options before the next gameplay input.
        run(u, old['options35_max'])
        assert u.reg_read(UC_M68K_REG_D2) == 8 and rd(u, P+4) == 1
    else:
        run(u, old['detect04'])
    assert (rd(u, P), rd(u, P+38), rd(u, P+36)) == (1, 1, 0)
    assert rd(u, M+4, 4) == 7 and rd(u, M+8, 4) == 3

if len(sys.argv) == 2:
    legacy = Path(sys.argv[1]).read_bytes()
    u = context(legacy)
    w(u, M+18, 0, 1)
    run(u, old['detect04'])
    w(u, M+18, 255, 1)
    run(u, old['options35_max'])
    run(u, old['detect04'])
    assert rd(u, P) == 0 and rd(u, P+38) == 1
    u = context(legacy)
    packet_port(u)['delay'] = 2
    run(u, 0x18013c)
    assert rd(u, P+36) == 1

print('PASS full mouse handshakes with transient/delayed replies, reconnect through gameplay and Options')
