exec(open('v36/test_core.py').read().split('levels=json')[0])
levels=json.loads(Path('amiga_research/maps.json').read_text())[1]
for camp in [0,1]:
 for button in range(14):
  u=machine();w(u,S['CAMP'],camp);run(u,0x2360);run(u,0x2944);w(u,0xffff2606,0);run(u,0x4832)
  u.reg_write(UC_M68K_REG_D0,button*2);run(u,0x8e34,0x8e50)
  floor=rd(u,0xffff2606);assert 0<=floor<16 and floor not in (6,7)
  assert rd(u,S['CAMP'])==camp
  if camp:assert bytes(u.mem_read(0xffff305a,4000))==bytes.fromhex(levels[floor]['cells'])
  run(u,0x8faa);assert rd(u,0xffff25a4,1)&1==camp
 # Capture -> campaign-specific prison and coordinates; loader executed.
 u=machine();w(u,S['CAMP'],camp);run(u,0x2360);run(u,0x2944);w(u,0xffff2606,0);run(u,0x4832);run(u,0x2dde,0x2e08)
 assert (rd(u,0xffff2606),rd(u,0xffff441a),rd(u,0xffff441e))==((10,0x4500,0x1800) if camp else (11,0x2a00,0x2300))
 # All six airlock directions retain their known coordinate transforms.
 for entry,f,x,z,expect in [(0x78de,5,0x4800,0x1000,(6,0x800,0x1000)),(0x78de,5,0x4200,0x2a00,(7,0x1900,0x700)),(0x7918,6,0x800,0x1000,(5,0x4800,0x1000)),(0x7918,6,0x800,0x2a00,(7,0x2f00,0x700)),(0x7952,7,0x3200,0x700,(6,0x900,0x2a00)),(0x7952,7,0x1000,0x700,(5,0x3900,0x2a00))]:
  w(u,0xffff2606,f);w(u,0xffff441a,x);w(u,0xffff441e,z);u.reg_write(UC_M68K_REG_A0,0xffff4412);run(u,entry)
  assert (rd(u,0xffff2606),rd(u,0xffff441a),rd(u,0xffff441e))==expect
print('PASS both campaigns: all14 elevator destinations load, password generation, prison routing, six airlock transforms')
