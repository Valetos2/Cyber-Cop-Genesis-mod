source=open('v36/compare_barrels_lamp04.py').read().split("if __name__")[0]
source=source.replace('def capture():','def capture(raw):').replace('[(39,0x95),(40,0x82),(41,0x9c)]','[(40,raw)]')
source=source[:source.index(" im.save(")]+" return im.tobytes()\n"
exec(source)
for raw in list(range(37,62))+[63]:
 assert capture(raw)==capture(raw|64),hex(raw)
print('PASS all26 world pickup sprites unchanged by damage marker')
