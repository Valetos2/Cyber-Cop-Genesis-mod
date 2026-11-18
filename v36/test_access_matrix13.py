exec(open('v36/test_core.py').read().split('levels=json')[0])

FLOOR, ACCESS, LATCH, HISTORY = 0xffff2606, 0xffff26bc, 0xffff216e, 0xffff2718
routes = [int.from_bytes(R[p:p+2], 'big') for p in range(0x8e58, 0x8e74, 2)]
assert sorted(routes) == [i for i in range(16) if i not in (6, 7)]
for camp in (0, 1):
    other = (1-camp)*0x2000
    for dest in range(16):
        elevator = dest in routes
        departure = (dest+1) % 16 if elevator else dest
        for access in range(8):
            for visited in (False, True):
                u = machine()
                w(u, S['CAMP'], camp)
                run(u, 0x2360)
                run(u, 0x2944)
                w(u, FLOOR, departure)
                run(u, 0x4882)
                w(u, ACCESS, access*32)
                history = bytearray(16)
                history[dest] = 255*visited
                if elevator:
                    history[departure] = 255*(not visited)
                u.mem_write(HISTORY, bytes(history))
                latch = 65535*(not visited if elevator else visited)
                w(u, LATCH, latch)
                u.mem_write(0x200000, b'\xff'*0x4000)
                if elevator:
                    w(u, 0xffff218e, routes.index(dest)*2)
                    u.reg_write(UC_M68K_REG_D3, 0xb1)
                    u.reg_write(UC_M68K_REG_A0, 0xffff7dca)
                    run(u, 0x8e9e) # start from the confirmed elevator destination
                else:
                    # Parking and Warehouse aren't target entries. Exercise
                    # the current-map serializer directly for those indices.
                    run(u, V['save17_hook'], 0x8f96)
                assert rd(u, FLOOR) == departure and rd(u, LATCH) == latch
                sram = bytes(u.mem_read(0x200000, 0x4000))
                assert sram[other:other+0x2000] == b'\xff'*0x2000
                del u
                u = machine()
                u.mem_write(0xffff0000, bytes(65536))
                for a in (0x1602, 0x2930, 0x33b6):
                    u.mem_write(a, b'\x4e\x75')
                u.mem_write(0x200000, sram)
                run(u, S['resume_mission36' if camp else 'resume_original36'], 0x124a)
                assert (rd(u, S['CAMP']), rd(u, FLOOR), rd(u, ACCESS)) == (camp, dest, access*32)
                run(u, 0x1fb4, 0x1fc2)
                assert rd(u, LATCH) == 65535*visited and u.mem_read(HISTORY, 16) == history
                run(u, 0x7d76, 0x7db2)
                assert rd(u, ACCESS) == 32*(access if visited else min(7, access+1))
print('PASS 512 SRAM restores: both campaigns, all 16 destinations, access 0-7, prior terminal visit or none')
