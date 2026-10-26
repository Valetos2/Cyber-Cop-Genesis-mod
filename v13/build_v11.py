"""Build Cyber-Cop v0.11: conservative early occlusion of ordinary wall cells."""
from pathlib import Path
import hashlib, json, sys

SOURCE_HASH = '98838ed8d69349ab64a99e4a4e0ea72843d47b175b69fda36957283932f0aba9'
BASE = 0xF0000  # Verified FF padding in this exact dump.
class Code:
    def __init__(self): self.b=bytearray(); self.labels={}; self.fix=[]
    def label(self,n): self.labels[n]=BASE+len(self.b)
    def emit(self,h): self.b.extend(bytes.fromhex(h))
    def address(self,a): self.b.extend(a.to_bytes(4,'big'))
    def abs(self,op,a): self.emit(op); self.address(a)
    def jump(self,a): self.abs('4ef9',a)
    def call(self,a): self.abs('4eb9',a)
    def branch(self,op,label):
        self.emit(op); self.fix.append((len(self.b),label)); self.emit('0000')
    def port(self,value):
        self.emit('13fc'); self.emit(f'{value:04x}'); self.address(0xa10003)
        self.emit('4e714e71')  # settle after TH transition
    def finish(self):
        for p,n in self.fix:
            self.b[p:p+2]=(self.labels[n]-(BASE+p)).to_bytes(2,'big',signed=True)
        return bytes(self.b)

def build(source):
    if hashlib.sha256(source).hexdigest()!=SOURCE_HASH: raise ValueError('Wrong source ROM')
    r=bytearray(source); c=Code()
    c.label('menu_edge')
    # Active-low directions: current OR NOT previous; upper 12 bits untouched.
    c.abs('3039',0xffff0006); c.emit('46400240000f8e40')
    c.abs('2279',0xffff202a); c.jump(0x54d8)

    c.label('poll6')
    c.emit('2f022f0340e7007c0700')  # save D2,D3,SR; mask interrupts
    c.port(0x40)
    c.port(0); c.abs('1039',0xa10003)
    c.port(0x40); c.emit('e548024000c0'); c.abs('1239',0xa10003)
    c.emit('0241003f8041')  # ordinary active-low S A C B R L D U
    c.port(0); c.port(0x40)  # phase 2
    c.port(0); c.abs('1639',0xa10003); c.emit('0243000f') # phase 3 identification
    c.port(0x40); c.abs('1439',0xa10003); c.emit('46020242000f') # M X Y Z active-high
    c.port(0); c.port(0x40)  # phase 4, leave TH high
    c.emit('4a43'); c.branch('6700','six_present')
    c.emit('7400')  # 3-button pad: no extra buttons
    c.label('six_present')
    c.emit('46df')  # restore original interrupt mask
    c.emit('33f9'); c.address(0xffff0010); c.address(0xffff0012)
    c.abs('33c2',0xffff0010)
    c.emit('33f9'); c.address(0xffff0004); c.address(0xffff0006)
    c.abs('33c0',0xffff0004)
    c.emit('261f241f4e75')

    c.label('mode_action')
    c.abs('3039',0xffff0012); c.emit('4640')
    c.abs('c079',0xffff0010); c.emit('02400008')
    c.branch('6700','mode_done')
    c.emit('0cb900007070'); c.address(0xffff26b8)
    c.branch('6700','wake')
    c.emit('0cb900002106'); c.address(0xffff26b8)
    c.branch('6600','mode_done')
    c.abs('4a39',0xffff270e); c.branch('6600','mode_done')
    c.abs('50f9',0xffff270a)  # same menu/input mode as native inventory sleep
    c.jump(0x6fb2)  # native sleep entry; returns to our caller
    c.label('wake'); c.jump(0x709a)  # native wake / energy accounting
    c.label('mode_done'); c.emit('4e75')

    c.label('strafe')
    c.abs('4a39',0xffff26e8); c.branch('6600','normal_move')
    c.abs('3039',0xffff441c)
    c.abs('b079',0xffff4440); c.branch('6e00','normal_move')
    c.abs('3039',0xffff0004)
    c.emit('08000006'); c.branch('6600','normal_move') # A released
    c.emit('46400240000f')
    c.emit('0c400004'); c.branch('6700','strafe_left')
    c.emit('0c400008'); c.branch('6600','normal_move')
    c.label('strafe_right')
    c.abs('41f9',0xffff4412); c.call(0xa268) # unchanged forward acceleration
    c.emit('066801000028026803fe0028317cff0000324e75')
    c.label('strafe_left')
    c.abs('41f9',0xffff4412); c.call(0xa268)
    c.emit('046801000028026803fe0028317c010000324e75')
    c.label('normal_move')
    c.abs('3039',0xffff0004); c.jump(0xa0f0) # replay displaced instruction

    c.label('item_keys')
    # Only native sleep blocks XYZ. No cursor, menu or interaction restriction.
    c.emit('0cb900007070'); c.address(0xffff26b8)
    c.branch('6700','items_done')
    c.abs('3039',0xffff0012); c.emit('4640')
    c.abs('c079',0xffff0010); c.emit('02400007')
    c.emit('08000002'); c.branch('6600','item_left')
    c.emit('08000000'); c.branch('6600','item_right')
    c.emit('08000001'); c.branch('6700','items_done')
    c.call(0x55ba) # the original Use menu-item validity check: zero means enabled
    c.emit('4a40'); c.branch('6600','items_done')
    c.jump(0x72ac)
    c.label('item_left'); c.jump(0x6e82)
    c.label('item_right'); c.jump(0x6e86)
    c.label('items_done'); c.emit('4e75')

    c.label('quick_interact')
    c.emit('0cb900002106'); c.address(0xffff26b8)
    c.branch('6600','quick_cancel')
    c.abs('4a39',0xffff270e); c.branch('6600','quick_cancel')
    c.abs('3039',0xffff0004)
    c.abs('4a79',0xffff0010); c.branch('6600','quick_cancel')
    c.emit('08000006'); c.branch('6600','quick_released')
    c.emit('024000ff0c4000bf'); c.branch('6600','quick_cancel')
    c.emit('08390006'); c.address(0xffff0007) # previous physical A
    c.branch('6700','quick_done') # held: retain eligibility, never rearm
    c.abs('50f9',0xffff0022); c.emit('4e75')
    c.label('quick_released')
    c.abs('4a39',0xffff0022); c.branch('6700','quick_done')
    c.abs('4239',0xffff0022)
    c.emit('024000ff0c4000ff'); c.branch('6600','quick_done')
    c.call(0x55a8); c.emit('4a40'); c.branch('6600','quick_pickup')
    c.abs('50f9',0xffff270a) # object UI needs native menu input mode
    c.jump(0x727c)
    c.label('quick_pickup')
    c.call(0x557c); c.emit('4a40'); c.branch('6600','quick_done')
    c.jump(0x6ace) # native capacity checks, world removal, HUD updates
    c.label('quick_cancel'); c.abs('4239',0xffff0022)
    c.label('quick_done'); c.emit('4e75')

    c.label('main_input')
    c.call(c.labels['poll6'])
    c.call(0x5370)  # original input handler, skipping original 3-button read
    c.call(c.labels['mode_action'])
    c.call(c.labels['item_keys'])
    c.call(c.labels['quick_interact'])
    c.call(0x67ac)  # displaced original callback processing
    c.jump(0x20b8)

    c.label('wall_depth')
    c.emit('ee4f') # lsr.w #7,d7: finer depth bins
    c.emit('0c4700ff'); c.branch('6300','wall_bin_ok')
    c.emit('3e3c00ff')
    c.label('wall_bin_ok'); c.emit('00478000')
    c.abs('33c7',0xffff2690); c.jump(0xe4d0)
    c.label('pattern_select')
    c.emit('4a43'); c.branch('6b00','wall_pattern')
    c.abs('49f9',0x1366e); c.emit('0243000f'); c.jump(0xe14e)
    c.label('wall_pattern'); c.emit('024300ff')
    table_address_fix=len(c.b)+2
    c.abs('49f9',0); c.jump(0xe14e)
    c.label('wall_with_band')
    # Preserve projected corners BEFORE native E594 sorts/mutates them.
    # A0 (the current render-list object) must survive both draws.
    c.emit('3f07') # preserve face depth below quad on stack
    c.abs('43f9',0xffff2458)
    c.emit('4cd1000f48e7f000') # movem (a1),d0-d3; movem d0-d3,-(sp)
    c.call(c.labels['wall_depth'])
    c.emit('4cdf000f3e1f') # recover original quad and face depth
    c.abs('43f9',0xffff2458); c.emit('48d1000f')
    # Each vertical edge has constant camera-space depth, so interpolating
    # its projected y at fixed wall-height fractions is perspective-correct
    # apart from the original integer projection's rounding.
    for top,bottom in [(2,10),(6,14)]:
        c.emit(f'302900{top:02x}48c0322900{bottom:02x}48c19081')
        # D0 = top-bottom (long), D1 = bottom.
        c.emit('2400d482d480e682d481') # D2=bottom+floor(3*span/8)
        c.emit('2600e588d083e880d081') # D0=bottom+floor(5*span/16)
        c.emit(f'334200{top:02x}334000{bottom:02x}')
    c.emit('e04f0c470025'); c.branch('6300','band_depth_ok')
    c.emit('3e3c0025')
    c.label('band_depth_ok')
    c.abs('45f9',0xe4aa); c.emit('1e3270005247')
    c.abs('33c7',0xffff2690) # original wall shade + 1, visible but distance shaded
    c.jump(0xe4d0)
    # 0014/0015 are unused bytes immediately before the original DMA workspace
    # at 0016. 0014: intro active, 0015: front-end mapping (2=release latch).
    c.label('intro_enter')
    c.emit('33fcffff'); c.address(0xffff0014)
    c.call(0x26b8); c.jump(0x38c)

    c.label('wait_frame')
    c.abs('4a39',0xffff0014); c.branch('6700','wait_native')
    c.emit('2f002f01'); c.call(0x53a8)
    c.emit('08000007'); c.branch('6700','intro_skip')
    c.emit('221f201f')
    c.label('wait_native')
    c.emit('3f00'); c.abs('3039',0xffff2798); c.jump(0x2938)

    c.label('intro_skip')
    # At 0386 execution is at the top-level, SP=FFFFFFFE. Abandon only the
    # intro's synchronous wait/animation call frames, not an interrupt frame.
    c.abs('4ff9',0xfffffffe)
    c.abs('4239',0xffff0014)
    c.emit('23fc0000b426'); c.address(0xffff2794)
    c.call(0x26b8) # immediate black before rebuilding the menu assets
    c.emit('7001'); c.call(0x150b4) # title/menu music, same as original 04DE
    c.call(0x2576) # restore base font/patterns
    c.jump(0x4fa) # shared title/cursor resource loading, through 057E

    c.label('intro_assets_ready')
    c.abs('4a39',0xffff0014); c.branch('6700','menu_enter')
    c.abs('41f9',0x33ada); c.jump(0x584) # displaced LEA, normal intro

    c.label('menu_enter')
    c.abs('4239',0xffff0014)
    c.emit('13fc0002'); c.address(0xffff0015) # swallow held skip/confirm
    c.emit('23fc0000b426'); c.address(0xffff2794)
    c.jump(0x6dc)

    c.label('front_pad')
    # Called in place of original final MOVE.W D0,pad. The previous pad word
    # was already copied by 53D8; keep current and previous equally normalized.
    c.abs('4a39',0xffff0014); c.branch('6600','front_store')
    c.abs('4a39',0xffff0015); c.branch('6700','front_store')
    c.emit('0c390002'); c.address(0xffff0015)
    c.branch('6600','front_map')
    c.emit('3200024100900c410090'); c.branch('6700','front_unlatch')
    c.emit('00400090'); c.branch('6000','front_store')
    c.label('front_unlatch'); c.abs('50f9',0xffff0015)
    c.label('front_map')
    c.emit('08000007'); c.branch('6600','front_start_released')
    c.emit('08800004') # active-low B pressed when physical Start is pressed
    c.label('front_start_released'); c.emit('08c00007')
    # C retains the former finish-editor command only at its own poll site.
    c.emit('0c970000fbd8'); c.branch('6600','front_store')
    c.emit('08000005'); c.branch('6600','front_store')
    c.emit('08800007')
    c.label('front_store'); c.abs('33c0',0xffff0004); c.emit('4e75')

    c.label('game_enter')
    c.abs('4279',0xffff0014)
    c.abs('4239',0xffff0022)
    c.abs('50f9',0xffff26f3); c.jump(0x1f1a)

    c.label('bayer_select')
    c.emit('4a43'); c.branch('6a00','bayer_solid')
    c.emit('024300ffe94b') # bin * 16 (first shift by 4)
    c.emit('d643') # *32: four rows repeated twice for wrap-free rotation
    bayer_table_fix=len(c.b)+2
    c.abs('49f9',0); c.emit('d8c34e75')
    c.label('bayer_solid')
    c.abs('49f9',0x1366e); c.emit('0243000f'); c.jump(0xe14e)

    c.label('bayer_span')
    c.abs('4a79',0xffff2690); c.branch('6a00','span_native')
    c.emit('2f0c3601464302430003e54bd8c3') # save A4, row=(~y)&3
    span_call_fix=len(c.b)+2
    c.call(0)
    c.emit('285f4e75')
    c.label('span_native')
    c.b[span_call_fix:span_call_fix+4]=c.labels['span_native'].to_bytes(4,'big')
    c.emit('48e7e310'); c.abs('4bf9',0x6348); c.jump(0xe07c)

    c.label('bayer_center')
    c.abs('4a79',0xffff2690); c.branch('6b00','center_pattern')
    c.abs('43f9',0xffff2458); c.jump(0xd67a)
    c.label('center_pattern')
    # The original central-rectangle clipping, retaining inclusive bounds.
    c.abs('43f9',0xffff2458); c.emit('30290006')
    c.branch('6b00','center_done'); c.emit('0c40007f')
    c.branch('6f00','center_top_ok'); c.emit('303c007f')
    c.label('center_top_ok'); c.emit('3429000a')
    c.branch('6a00','center_bottom_nonnegative'); c.emit('7400')
    c.label('center_bottom_nonnegative'); c.emit('0c42007f')
    c.branch('6e00','center_done'); c.emit('36009042')
    c.branch('6b00','center_done'); c.emit('5240')
    c.abs('45f9',0x6348); c.emit('d643d64324723000321134290004b242')
    c.branch('6d00','center_x_ordered'); c.emit('c342')
    c.label('center_x_ordered'); c.emit('4a41')
    c.branch('6a00','center_left_ok'); c.emit('7200')
    c.label('center_left_ok'); c.emit('0c4100bf')
    c.branch('6e00','center_done'); c.emit('4a42')
    c.branch('6b00','center_done'); c.emit('0c4200bf')
    c.branch('6f00','center_right_ok'); c.emit('343c00bf')
    c.label('center_right_ok')
    c.emit('36010243fff8ed4b38020244fff8ed4c')
    c.emit('3a0102450007da45da45'); c.abs('4df9',0x136ae)
    c.emit('2a3650003c0202460007dc46dc462c366020')
    # A2 is top row at x=0; its byte phase selects screen y modulo 4.
    c.emit('2e0a0487ffff89340247000fd8c7')
    c.emit('4bf2400045f23000') # A5=last column, A2=first column
    c.emit('2205b5cd'); c.branch('6700','center_single')
    c.emit('2f06') # retain last-column keep mask across column fills
    c.label('center_column_loop')
    c.emit('264a')
    column_call_fix=len(c.b)+2; c.call(0)
    c.emit('45ea0200b5cd'); c.branch('6700','center_last')
    c.emit('7200'); c.branch('6000','center_column_loop')
    c.label('center_last'); c.emit('221f264a')
    column_jump_fix=len(c.b)+2; c.jump(0)
    c.label('center_single'); c.emit('8286264a') # merge both keep masks
    column_single_fix=len(c.b)+2; c.jump(0)
    c.label('center_done'); c.emit('4e75')

    c.label('pattern_column')
    for fix in [column_call_fix,column_jump_fix,column_single_fix]:
        c.b[fix:fix+4]=c.labels['pattern_column'].to_bytes(4,'big')
    # Inputs D0=height, D1=keep-mask, A3=output, A4=rotated 4-row pattern.
    # D0,D1,A2,A4,A5 survive. Four 8-pixel rows per unrolled group.
    c.emit('4cd4003c4a81'); c.branch('6700','column_full') # D2-D5 patterns
    c.emit('2e014687c487c687c887ca87') # mask patterns once per partial column
    c.emit('3c00e44e'); c.branch('6700','partial_tail')
    c.emit('5346'); c.label('partial_loop')
    for reg in range(2,6):
        c.emit('2e13ce81'); c.emit(f'{0x8e80|reg:04x}'); c.emit('26c7')
    # DBRA uses the same word-relative encoding as other branches.
    c.branch('51ce','partial_loop')
    c.label('partial_tail'); c.emit('3c0002460003')
    c.branch('6700','column_done')
    for reg in range(2,5):
        c.emit('2e13ce81'); c.emit(f'{0x8e80|reg:04x}'); c.emit('26c7')
        if reg<4:
            c.emit('5346'); c.branch('6700','column_done')
    c.emit('4e75')
    c.label('column_full'); c.emit('3c00e44e')
    c.branch('6700','full_tail'); c.emit('5346'); c.label('full_loop')
    for reg in range(2,6):c.emit(f'{0x26c0|reg:04x}')
    c.branch('51ce','full_loop')
    c.label('full_tail'); c.emit('3c0002460003')
    c.branch('6700','column_done')
    for reg in range(2,5):
        c.emit(f'{0x26c0|reg:04x}')
        if reg<4:
            c.emit('5346'); c.branch('6700','column_done')
    c.label('column_done'); c.emit('4e75')

    c.label('wall_patterns')
    c.b[table_address_fix:table_address_fix+4]=c.labels['wall_patterns'].to_bytes(4,'big')
    # Fade across each original shade band. Eight-pixel horizontally repeated
    # patterns; no per-pixel arithmetic in the existing rasterizer.
    old=list(source[0xe4aa:0xe4d0])
    order=[0,4,2,6,1,5,3,7]
    for index in range(256):
        depth=index*128; slot=min(depth//256,len(old)-1); shade=old[slot]
        first=slot
        while first and old[first-1]==shade:first-=1
        end=slot+1
        while end<len(old) and old[end]==shade:end+=1
        lower=old[end] if end<len(old) else shade
        fraction=0 if lower==shade else min(8,((depth-first*256)*8)//((end-first)*256))
        pixels=[shade]*8
        for j in order[:fraction]:pixels[j]=lower
        c.emit(''.join(format(x,'x') for x in pixels))
    c.label('bayer_patterns')
    c.b[bayer_table_fix:bayer_table_fix+4]=c.labels['bayer_patterns'].to_bytes(4,'big')
    bayer=[[0,8,2,10],[12,4,14,6],[3,11,1,9],[15,7,13,5]]
    for index in range(256):
        depth=index*128; slot=min(depth//256,len(old)-1); shade=old[slot]
        first=slot
        while first and old[first-1]==shade:first-=1
        end=slot+1
        while end<len(old) and old[end]==shade:end+=1
        lower=old[end] if end<len(old) else shade
        fraction=0 if lower==shade else min(16,((depth-first*256)*16)//((end-first)*256))
        for row in range(8):
            c.emit(''.join(format(lower if bayer[row%4][x%4]<fraction else shade,'x') for x in range(8)))
    c.label('fast_sort')
    c.emit('48e7fffe') # preserve all general registers
    c.abs('49f9',0xffff4fd8) # a4 base
    c.abs('2a79',0xffff4fd4) # a5 end
    c.emit('264c588b') # a3=base+4
    c.label('sort_outer')
    c.emit('b7cd'); c.branch('6c00','sort_done')
    c.emit('2053') # movea.l (a3),a0: retain pointer being inserted
    c.emit('3410226bfffc3811b842') # key d2; previous depth d4
    c.branch('6c00','sort_next')
    c.emit('7000220b928c') # low=0; high=a3-a4
    c.label('sort_search')
    c.emit('b240'); c.branch('6f00','sort_found')
    c.emit('3600d641e24b0243fffc') # middle rounded to pointer boundary
    c.emit('227430003811b842')
    c.branch('6d00','sort_high')
    c.emit('30035840'); c.branch('6000','sort_search')
    c.label('sort_high'); c.emit('3203'); c.branch('6000','sort_search')
    c.label('sort_found')
    c.emit('45f40000224b') # a2=base+low, a1=current
    c.label('sort_shift')
    c.emit('22a9fffc5989b3ca'); c.branch('6200','sort_shift')
    c.emit('2288') # insert retained pointer
    c.label('sort_next'); c.emit('588b'); c.branch('6000','sort_outer')
    c.label('sort_done'); c.emit('4cdf7fff4e75')
    # Cache the composed pixel pair when vertical scaling repeats a source row.
    sprite_loops=[(0xeac2,0xead2),(0xeae4,0xeaf4),(0xeb06,0xeb16),(0xeb28,0xeb38)]
    for entry,calc_end in sprite_loops:
        tag=f'sprite_{entry:x}'
        c.label(tag)
        c.emit('3e280014be680018') # original source height vs projected height
        c.branch('6c00',tag+'_native')
        c.emit('2f0d');c.abs('4bf9',0xeb4a) # preserve a5; transparency mask table
        c.emit('3e1c') # first source-row increment
        c.label(tag+'_calculate')
        c.emit(source[entry+2:calc_end].hex())
        c.branch('6700',tag+'_advance')
        c.emit('18350000') # mask for cached pair
        c.label(tag+'_write')
        c.emit('c9138113') # and.b d4,(a3); or.b d0,(a3)
        c.label(tag+'_advance')
        c.emit('584b') # addq.w #4,a3 (address operation is long on 68000)
        c.branch('51cd',tag+'_repeat') # dbra d5
        c.emit('2a5f4e75')
        c.label(tag+'_repeat')
        c.emit('3e1c');c.branch('6600',tag+'_calculate')
        c.emit('4a00');c.branch('6600',tag+'_write')
        c.branch('6000',tag+'_advance')
        c.label(tag+'_native')
        c.jump(entry)
    c.label('fast_sort_v10')
    c.emit('48e7fffe') # preserve all general registers
    c.abs('49f9',0xffff4fd8) # a4 base
    c.abs('2a79',0xffff4fd4) # a5 end
    c.emit('264c588b') # a3=base+4
    c.label('sort10_outer')
    c.emit('b7cd'); c.branch('6c00','sort10_done')
    c.emit('2053') # movea.l (a3),a0: retain pointer being inserted
    c.emit('3410226bfffc3811b842') # key d2; previous depth d4
    c.branch('6c00','sort10_next')
    c.emit('7000220b928c') # low=0; high=a3-a4
    c.label('sort10_search')
    c.emit('b240'); c.branch('6f00','sort10_found')
    c.emit('3600d641e24b0243fffc') # middle rounded to pointer boundary
    c.emit('227430003811b842')
    c.branch('6d00','sort10_high')
    c.emit('30035840'); c.branch('6000','sort10_search')
    c.label('sort10_high'); c.emit('3203'); c.branch('6000','sort10_search')
    c.label('sort10_found')
    c.emit('45f40000224b') # a2=base+low, a1=current
    c.emit('220b928ae4895341') # d1=(current-destination)/4-1
    c.label('sort10_shift')
    c.emit('23610004'); c.branch('51c9','sort10_shift') # copy -(a1) to 4(a1)
    c.emit('2288') # insert retained pointer
    c.label('sort10_next'); c.emit('588b'); c.branch('6000','sort10_outer')
    c.label('sort10_done'); c.emit('4cdf7fff4e75')
    c.label('wall_center_depth')
    # CF38 only consumes D7 and the clear N flag. Keep the other registers.
    c.emit('48e7fc38') # d0-d5/a2-a4
    c.abs('45f9',0xffff261a)
    c.abs('47f9',0x11508)
    c.emit('3028000c906a000c34280008946a0008')
    c.abs('3839',0xffff260c)
    c.emit('3a334000c5c5') # sine * dx
    c.emit('49eb01003a344000c1c5') # cosine * dz
    c.emit('d082d08048404a40')
    c.branch('6e00','center_depth_positive')
    c.emit('7064')
    c.label('center_depth_positive');c.emit('3e00')
    c.emit('4cdf1c3f023c00f74e75') # restore registers; N=0
    # Four cardinal occluders, rebuilt every map pass in formerly unused RAM.
    # Record: distance, minimum target distance, lower/upper transverse bounds.
    c.label('occlusion_begin')
    c.emit('48e7fffe');c.abs('51f9',0xffff0023);c.abs('41f9',0xffff0024);c.emit('7000')
    for _ in range(8):c.emit('20c0')
    c.abs('3039',0xffff2624);c.branch('6f00','occlusion_ready')
    c.emit('0c400200');c.branch('6c00','occlusion_ready')
    c.abs('3c39',0xffff2622);c.abs('3e39',0xffff2626)
    c.emit('0c465000');c.branch('6400','occlusion_ready')
    c.emit('0c473200');c.branch('6400','occlusion_ready')
    c.emit('3007e048d040');c.abs('47f9',0xffff404a)
    c.abs('45f9',0xffff305a);c.emit('d4f300003006e048d4c0')
    c.emit('0c120081');c.branch('6700','occlusion_ready')
    c.abs('41f9',0xffff0024)
    for direction,(axis,sign,step,limit,trans_step,trans_limit) in enumerate([
        (0,1,1,79,-80,49),(0,-1,-1,79,-80,49),
        (1,1,-80,49,1,79),(1,-1,80,49,1,79)]):
        tag=f'occluder_{direction}'
        pos=6+axis;trans=7-axis
        c.label(tag)
        c.emit(f'{0x3000|pos:04x}e048')
        if sign>0:c.emit(f'4440064000{limit:02x}')
        c.emit('4a40');c.branch('6700',tag+'_next')
        c.emit('5340');c.emit(f'{0x3600|pos:04x}024300ff')
        if sign>0:c.emit('444306430100')
        c.emit('224a') # a1 = camera cell
        c.label(tag+'_scan')
        c.emit(f'd2fc{step&65535:04x}0c110081')
        c.branch('6700',tag+'_found')
        c.emit('06430100');c.branch('51c8',tag+'_scan')
        c.branch('6000',tag+'_next')
        c.label(tag+'_found')
        c.emit('0c430100');c.branch('6d00','occlusion_disabled')
        c.emit(f'{0x3800|trans:04x}024400ff4444064400403a0406450080')
        c.emit(f'{0x3200|trans:04x}e0494a41');c.branch('6700',tag+'_upper')
        c.emit('53412649')
        c.label(tag+'_lower_loop')
        c.emit(f'd6fc{(-trans_step)&65535:04x}0c130081')
        c.branch('6600',tag+'_upper')
        c.emit('04440100');c.branch('51c9',tag+'_lower_loop')
        c.label(tag+'_upper')
        c.emit(f'{0x3200|trans:04x}e0494441064100{trans_limit:02x}4a41')
        c.branch('6700',tag+'_store')
        c.emit('53412649')
        c.label(tag+'_upper_loop')
        c.emit(f'd6fc{trans_step&65535:04x}0c130081')
        c.branch('6600',tag+'_store')
        c.emit('06450100');c.branch('51c9',tag+'_upper_loop')
        c.label(tag+'_store')
        c.emit('4a44');c.branch('6c00',tag+'_next')
        c.emit('4a45');c.branch('6f00',tag+'_next')
        c.emit('308306430100314300023144000431450006');c.abs('50f9',0xffff0023)
        c.label(tag+'_next');c.emit('5088') # a0 += 8
    c.branch('6000','occlusion_ready')
    c.label('occlusion_disabled')
    c.abs('51f9',0xffff0023)
    c.abs('41f9',0xffff0024);c.emit('7000')
    for _ in range(8):c.emit('20c0')
    c.label('occlusion_ready')
    c.emit('4cdf7fff');c.abs('47f9',0xffff261a);c.jump(0x3b82)

    c.label('wall_visibility')
    c.abs('4a39',0xffff0023);c.branch('6700','wall_native')
    c.emit('48e7fffe')
    c.emit('0c130081');c.branch('6600','wall_keep')
    c.emit('3c280008');c.abs('9c79',0xffff2622)
    c.emit('3e28000c');c.abs('9e79',0xffff2626)
    c.abs('43f9',0xffff0024)
    for direction,(axis,sign) in enumerate([(0,1),(0,-1),(1,1),(1,-1)]):
        tag=f'visibility_{direction}'
        c.emit('4a51');c.branch('6700',tag+'_next')
        c.emit(f'{0x3000|6+axis:04x}')
        if sign<0:c.emit('444004400100')
        c.emit('b0690002');c.branch('6d00',tag+'_next')
        c.emit(f'{0x3200|7-axis:04x}3401c5d13600c7e90004b483')
        c.branch('6f00',tag+'_next')
        c.emit('06410100c3d13600c7e90006b283')
        c.branch('6d00','wall_hidden')
        c.label(tag+'_next');c.emit('5089')
    c.label('wall_keep')
    c.emit('4cdf7fff');c.label('wall_native');c.abs('2279',0xffff5724);c.jump(0xcf08)
    c.label('wall_hidden');c.emit('4cdf7fff4e75')
    blob=c.finish()
    assert len(blob)<0x10000 and set(source[BASE:BASE+len(blob)])=={255}
    turns=[(0xa2c2,-32),(0xa2d2,32),(0xa15a,-16),(0xa166,16),
           (0xa306,-16),(0xa316,16)]
    for off,value in turns:r[off:off+2]=value.to_bytes(2,'big',signed=True)
    r[BASE:BASE+len(blob)]=blob
    r[0x54d2:0x54d8]=bytes.fromhex('4ef9')+c.labels['menu_edge'].to_bytes(4,'big')
    r[0xa0ea:0xa0f0]=bytes.fromhex('4ef9')+c.labels['strafe'].to_bytes(4,'big')
    r[0x20b0:0x20b8]=bytes.fromhex('4ef9')+c.labels['main_input'].to_bytes(4,'big')+bytes.fromhex('4e71')
    r[0xe498:0xe49e]=bytes.fromhex('4ef9')+c.labels['wall_depth'].to_bytes(4,'big')
    r[0xe146:0xe14e]=bytes.fromhex('4ef9')+c.labels['pattern_select'].to_bytes(4,'big')+bytes.fromhex('4e71')
    # Intro entry, frame waits, shared asset setup and menu handoff.
    for off,end,label in [(0x386,0x38c,'intro_enter'),(0x2930,0x2938,'wait_frame'),
                           (0x57e,0x584,'intro_assets_ready'),(0x6d2,0x6dc,'menu_enter'),
                           (0x53e2,0x53e8,'front_pad'),(0x1f14,0x1f1a,'game_enter')]:
        r[off:end]=bytes.fromhex('4ef9')+c.labels[label].to_bytes(4,'big')+bytes.fromhex('4e71')*((end-off-6)//2)
    # Disable old asynchronous stack-unwinding intro skip: handled at safe waits.
    assert source[0x5d4:0x5d8]==(0xa9e).to_bytes(4,'big')
    r[0x5d4:0x5d8]=(0xb426).to_bytes(4,'big')
    r[0xe498:0xe49e]=bytes.fromhex('4ef9')+c.labels['wall_with_band'].to_bytes(4,'big')
    r[0x3eb0:0x3eb6]=bytes.fromhex('4ef9')+c.labels['fast_sort_v10'].to_bytes(4,'big')
    for slot,entry in [(0xe998,0xeb28),(0xe99c,0xeb06),(0xe9a0,0xeac2),(0xe9a4,0xeae4)]:
        assert int.from_bytes(source[slot:slot+4],'big')==entry
        r[slot:slot+4]=c.labels[f'sprite_{entry:x}'].to_bytes(4,'big')
    assert source[0xcf38:0xcf3e]==bytes.fromhex('4eb900004c86')
    r[0xcf38:0xcf3e]=bytes.fromhex('4eb9')+c.labels['wall_center_depth'].to_bytes(4,'big')
    r[0x3b7c:0x3b82]=bytes.fromhex('4ef9')+c.labels['occlusion_begin'].to_bytes(4,'big')
    r[0xcf02:0xcf08]=bytes.fromhex('4ef9')+c.labels['wall_visibility'].to_bytes(4,'big')
    stripes=bytes(r)
    for off,end,label in [(0xe146,0xe14e,'bayer_select'),(0xe074,0xe07c,'bayer_span'),(0xd674,0xd67a,'bayer_center')]:
        r[off:end]=bytes.fromhex('4ef9')+c.labels[label].to_bytes(4,'big')+bytes.fromhex('4e71')*((end-off-6)//2)
    return stripes,bytes(r),c.labels,len(blob)

def ips(source,target):
    out=bytearray(b'PATCH'); i=0
    while i<len(source):
        if source[i]==target[i]:i+=1;continue
        start=i
        while i<len(source) and source[i]!=target[i] and i-start<65535:i+=1
        out+=start.to_bytes(3,'big')+(i-start).to_bytes(2,'big')+target[start:i]
    return bytes(out)+b'EOF'

if __name__=='__main__':
    source=Path(sys.argv[1]).read_bytes();dest=Path(sys.argv[2]);dest.mkdir(parents=True,exist_ok=True)
    full,walls,labels,size=build(source)
    for name,data in [('Cyber-Cop_v11_stripes',full),('Cyber-Cop_v11',walls)]:
        (dest/(name+'.bin')).write_bytes(data)
        (dest/(name+'.ips')).write_bytes(ips(source,data))
    (dest/'symbols.json').write_text(json.dumps({'labels':labels,'code_size':size},indent=2))
    print(json.dumps({'labels':{k:hex(v) for k,v in labels.items()},'size':size}))
