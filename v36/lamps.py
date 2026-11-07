# Only original Amiga lamp coordinates whose Genesis cell is empty and whose
# surrounding3x3 wall pattern agrees are eligible. Other level data is untouched.
lamp_lists=json.loads((OUT/'original_lamps.json').read_text())
ptrs=[asset('original_lamps_'+str(f),struct.pack('>'+str(len(xs)+1)+'H',*(xs+[65535]))) for f,xs in enumerate(lamp_lists)]
lamp_table=asset('original_lamps',struct.pack('>16I',*ptrs))
c.label('original_lamps36');c.call(0x4a40);c.call(0x4a06);c.emit('48e7fffe');tstcamp();c.branch('6600','original_lamps36_done');c.abs('4a79',0xffff026c);c.branch('6600','original_lamps36_done')
c.abs('3039',0xffff2606);c.emit('e548');c.abs('43f9',lamp_table);c.emit('22710000');c.abs('41f9',0xffff305a)
c.label('original_lamps36_loop');c.emit('3019');c.branch('6b00','original_lamps36_done');c.emit('4a300000');c.branch('6600','original_lamps36_loop');c.emit('11bc00820000');c.branch('6000','original_lamps36_loop')
c.label('original_lamps36_done');c.emit('4cdf7fff');c.jump(0x4966);patch(0x495e,'original_lamps36',8)
