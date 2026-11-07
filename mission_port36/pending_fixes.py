"""Validated small patches to apply in the future integrated build, not a campaign ROM."""
def darken_scanman_inset(rom,labels):
    start=labels['scan_inset35c_pixel'];end=labels['scan_contrast35_done']
    old=bytes.fromhex('720402400001');new=bytes.fromhex('720002400001')
    region=bytes(rom[start:end]);assert region.count(old)==1
    pos=start+region.index(old);rom[pos:pos+len(old)]=new
    return pos
