exec(open('v34/common.py').read())
ROM=Path('v35c/Cyber-Cop_v35c.bin').read_bytes()
def pack(data):
 d=bytearray(data);d[11]=sum(d[:11])&255
 return bytes(v for b in d for v in [97+(b>>4),107+(b&15)])
for save in ['Cyber-Cop_v14.gs7','Cyber-Cop_v14.gs8','Cyber-Cop_v14.gs9','Cyber-Cop_v15.gs0','Cyber-Cop_v16.gs1']:
 u=machine(ROM);u.mem_write(0xffff0000,Path('upload',save).read_bytes()[0x2478:0x12478]);run(u,0x8faa)
 original=bytes(u.mem_read(0xffff25b4,24));raw=bytes(u.mem_read(0xffff259a,12));assert raw[10]&3==0;assert pack(raw)==original
 # Native decoder ignores low bits0/1 of payload byte10 after checking the checksum.
 states=[]
 for campaign in [0,1]:
  data=bytearray(raw);data[10]|=campaign
  v=machine(ROM);v.mem_write(0xffff2580,pack(data));run(v,0xe94,0x124a)
  # Inventory and reconstructed character data, excluding password scratch/text itself.
  states.append((bytes(v.mem_read(0xffff2a24,0x600)),bytes(v.mem_read(0xffff2606,10)),rd(v,0xffff216e)))
 assert states[0]==states[1],save
 print('PASS',save,'campaign bit0 preserves original decode; zero preserves original password exactly')
print('Only format compatibility tested. Routing/serialization not implemented.')
