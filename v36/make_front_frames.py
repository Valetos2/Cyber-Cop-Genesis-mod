# Build sparse bevel overlays from the exact native button pixels, not resized screenshots.
b=src;v=bytearray(65536)
for address,dest in [(0x30714,0),(0x4d066,0x500),(0x8e4fa,0x48c0)]:
 n=int.from_bytes(b[address:address+2],'big');v[dest:dest+n]=b[address+2:address+2+n]
v[0xe000:0xf000]=b[0x51428:0x52428]
def native_pixel(x,y):
 p=0xe000+(y//8*64+x//8)*2;t=int.from_bytes(v[p:p+2],'big');xx=x%8;yy=y%8
 if t&0x800:xx=7-xx
 if t&0x1000:yy=7-yy
 q=v[(t&2047)*32+yy*4+xx//2];return q>>4 if xx%2==0 else q&15
frames=bytearray()
for x,y,width in [(128,88,32),(160,88,32),(32,56,22),(54,56,20),(74,56,22)]:
 pixels=[[0]*32 for _ in range(16)]
 for yy in range(11):
  for xx in range(width):
   if yy in (0,10) or xx in (0,width-1):
    color=native_pixel(x+xx,y+yy);assert 9<=color<=15
    pixels[yy][xx]=24-color
 # Genesis sprite column-major tile order.
 for tx in range(4):
  for ty in range(2):
   for yy in range(8):
    for xx in range(0,8,2):frames.append(pixels[ty*8+yy][tx*8+xx]*16+pixels[ty*8+yy][tx*8+xx+1])
front_frames=asset('front_pressed_frames36',frames)
