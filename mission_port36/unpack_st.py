exec(open('st2/deice.py').read().split("for name in")[0])
out=Path('mission_port36/st_resources');out.mkdir(exist_ok=True)
for file in sorted(Path('st2/files').glob('ILG*')):
 b=file.read_bytes();n=unpack_from('>I',b,8)[0];assert n<0x30000
 u.mem_write(0x40000,b);u.reg_write(UC_M68K_REG_A0,0x40000);u.reg_write(UC_M68K_REG_A7,0x180000);u.mem_write(0x180000,(0x190000).to_bytes(4,'big'));u.emu_start(0xc86,0x190000,count=20000000);assert u.reg_read(UC_M68K_REG_PC)==0x190000
 (out/(file.name+'.bin')).write_bytes(bytes(u.mem_read(0x40000,n)))
print('decoded',len(list(out.glob('*.bin'))))
