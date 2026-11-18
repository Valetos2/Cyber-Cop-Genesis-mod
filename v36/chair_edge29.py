# Chair $93 uses standing rotation frames $AF..$B6. The rightmost pixel
# column of the profile ($B1) has two isolated 3-pixel fragments in the
# original ROM; the scaler is reading them correctly. Clear just those
# transparent-background nibbles in place, preserving the adjacent column.
frame=0xb1
table=assets['sprite_offsets36']
start=0x8eef0+struct.unpack_from('>I',r,table+frame*4)[0]
end=0x8eef0+struct.unpack_from('>I',r,table+(frame+1)*4)[0]
stride=62
assert end-start==16*stride
for row in (30,31,32,40,41,42):
 p=start+15*stride+row
 assert r[p]&15
 r[p]&=0xf0
