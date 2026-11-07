exec(open('v36/test_core.py').read().split('levels=json')[0])
gst=Path('upload/Cyber-Cop_v36_test02.gs0').read_bytes()
for mode in ['native','table','off']:
 u=machine();u.mem_write(0xffff0000,gst[0x2478:0x12478]);u.mem_write(0x150d8,bytes.fromhex('4e75'))
 if mode=='native':u.mem_write(0xd4a0,OLD[0xd4a0:0xd4a6])
 if mode=='off':u.mem_write(0xcfc8,bytes.fromhex('4e75'));u.mem_write(0x45b8,bytes.fromhex('4e75'))
 counts={};cur=[''];u.hook_add(UC_HOOK_CODE,lambda uc,a,sz,d:counts.__setitem__(cur[0],counts.get(cur[0],0)+1))
 for a in [0x3b46,0x3b7c,0xb428,0x3eb0,0x3e3a,0xdf6a,0x4584,0xcf72]:
  cur[0]=hex(a);run(u,a)
 print(mode,counts,'total',sum(counts.values()),'circles',(rd(u,0xffff5338,4)-0xffff533c)//10)
