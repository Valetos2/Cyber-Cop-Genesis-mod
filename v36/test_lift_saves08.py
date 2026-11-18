"""Optional targeted reproduction with locally supplied v36a saves."""
exec(open('v36/test_core.py').read().split('levels=json')[0])
base=Path('v36/release_v36a/Cyber-Cop_v36a.bin').read_bytes()
for slot,old_goal,goal in [(3,6,2),(6,0,12)]:
 state=Path(f'upload/Cyber-Cop_v36a.gs{slot}').read_bytes()[0x2478:0x12478]
 for rom,target in [(base,old_goal),(R,goal)]:
  for button in range(2):
   u=machine(rom);u.mem_write(0xffff0000,state)
   if slot==6:
    # Run native target capture before the random starting-floor selection.
    run(u,0x8a88,0x8a92)
   u.reg_write(UC_M68K_REG_D0,button);run(u,0x8c36)
   assert rd(u,0xffff2182)==target
   stamp=rd(u,0xffff0858);duration=rd(u,0xffff085a)
   w(u,0xffff2798,stamp+duration);run(u,0x8b18)
   assert rd(u,0xffff260a)==target and rd(u,0xffff2186)==1
   run(u,0x8b18,0x8b2a);assert rd(u,0xffff2186)==0
 print(f'PASS gs{slot}: baseline target {old_goal}, corrected target {goal}; both buttons and final display before closing')
