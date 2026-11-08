exec(open('v36/render_indicators05.py').read().split("if __name__")[0].replace("'bomb':0x94f2", "'bomb':0x94f2,'lift':0x8c78").replace("if kind=='bomb':", "if kind=='lift':w(u,0xffff7dca,0xb2)\n elif kind=='bomb':"))
a=panel('lift',Path('v36/release_test05/Cyber-Cop_v36_test05.bin').read_bytes());b=panel('lift',R)
changed=[(x,y) for y in range(128) for x in range(192) if a.getpixel((x,y))!=b.getpixel((x,y))]
print('Lift changed pixels',len(changed),'bounds',(min(x for x,y in changed),min(y for x,y in changed),max(x for x,y in changed),max(y for x,y in changed)))
assert len(changed)==20
im=Image.new('RGB',(384,128));im.paste(a);im.paste(b,(192,0));im.resize((768,256),Image.Resampling.NEAREST).save('v36/lift_indicator06.png')
