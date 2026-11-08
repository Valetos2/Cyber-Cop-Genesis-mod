# Retain native shaded B1 lens geometry; recolour only the 6x4 lit lens.
def shade_lens(bank,tile,mapping):
 template=src[0x183f2+0xb1*128:0x183f2+0xb2*128]
 for y in range(4,8):
  for x in range(5,11):
   off=x//8*64+y*4+x%8//2;shift=0 if x&1 else 4
   value=template[off]>>shift&15;at=bank+tile*128+off
   r[at]=(r[at]&~(15<<shift))|(mapping[value]<<shift)
# Keypad's unused lens shades A/B become red. Active green remains C/D/E.
keybank=asset('keypad_shaded_bank36e',src[0x183f2:0x203f2])
shade_lens(keybank,0xb2,{12:10,13:11,14:1})
r[0x18052+20:0x18052+24]=struct.pack('>HH',0x200,0x500)
r[0x9464:0x9468]=struct.pack('>I',keybank)
# Airlock already contains dark/mid reds8/A and bright red1.
airbank=asset('airlock_shaded_bank36e',src[0x183f2:0x203f2])
shade_lens(airbank,0xb2,{12:8,13:10,14:1})
r[0x7736:0x773a]=struct.pack('>I',airbank)
# Bomb has its own bank; armed red B1 is left byte-for-byte intact.
# Unused A becomes dark yellow; existing white7 supplies the highlight.
# B is used by the bomb display and must retain its native red.
r[0x1813a+20:0x1813a+22]=struct.pack('>H',0x440)
shade_lens(0x196000,0xe1,{12:10,13:1,14:7})
# Lift denial uses the same red B2 lens; A/B are unused by its remaining tiles.
r[0x18222+20:0x18222+24]=struct.pack('>HH',0x200,0x500)
r[0x8cb8:0x8cbc]=struct.pack('>I',keybank)
