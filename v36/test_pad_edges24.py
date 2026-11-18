"""Drive TH reads, VBlank latch and gameplay consumers with controller traces."""
exec(open('v36/test_core.py').read().split('levels=json')[0])
import sys
SAMPLE=V['buffer26_sample']
CONSUME=V['buffer26_consume']
VIEW=0xffff26b8
J1=0xa10003
PRIMARY=(0xffff0004,0xffff0006)
EXTRA=(0xffff0010,0xffff0012)
SITES=(0xf9108,0xf9126,0xf9156,0xf916c)
SAVED=Path(sys.argv[2]).read_bytes()[0x2478:0x12478] if len(sys.argv)==3 else None

def pad(rom,fixture=None):
    u=machine(rom)
    if fixture is not None:u.mem_write(0xffff0000,fixture)
    for addr in (0x1755e,0x2930,0x4d18,0x1646):
        u.mem_write(addr,b'\x4e\x75')
    w(u,VIEW,0x2106,4);w(u,0xffff270a,0,1);w(u,0xffff0014,0)
    w(u,0xffff0140,0xff);w(u,0xffff0144,0)
    w(u,0xffff014e,0xa6,1);w(u,0xffff0150,255,1)
    w(u,PRIMARY[0],0xff);w(u,EXTRA[0],0)
    if fixture is None:
        u.mem_write(0xffff2f50,bytes(range(1,53)))
        w(u,0xffff2740,14);w(u,0xffff21ba,15)
    raw=[0x33,0x3f,0,15]
    def io(uc,addr,size,data):w(u,J1,raw[SITES.index(addr)],1)
    for addr in SITES:u.hook_add(UC_HOOK_CODE,io,begin=addr,end=addr)
    def tick(base=0,extended=0,valid=True,consume=True):
        raw[:]=[0x33^((base>>2)&0x30),0x3f^(base&0x3f),0 if valid else 3,15^extended]
        run(u,SAMPLE)
        if not consume:return None
        run(u,CONSUME)
        assert rd(u,0xffff0148)==rd(u,0xffff014a)==0
        return (rd(u,PRIMARY[1])&~rd(u,PRIMARY[0])&0xff,rd(u,EXTRA[0])&~rd(u,EXTRA[1])&15)
    tick();tick()
    return u,tick

if len(sys.argv)==3:
    old=Path(sys.argv[1]).read_bytes()
    for key in (4,1):
        positions=[]
        for rom in (old,R):
            u,tick=pad(rom,SAVED)
            for value,valid in [(key,True),(key,True),(0,False),(key,True),(key,True),(0,False),(key,True)]:
                tick(extended=value,valid=valid)
                run(u,V['item_keys'])
                positions.append(rd(u,0xffff2740))
                if rom==R:
                    run(u,V['item_keys'])
                    assert rd(u,0xffff2740)==positions[-1]
        assert positions[0]!=14 and positions[3]!=positions[0] and len(set(positions[7:]))==1,positions
    print('PASS user GST inventory: forced invalid responses reproduce false repeat on test15; test16 makes one step')
for base,extended in [(16,0),(32,0),(128,0),(0,4),(0,2),(0,1),(0,8)]:
    target=(base,extended)
    u,tick=pad(R)
    assert tick(base,extended)==target
    for _ in range(5):assert tick(base,extended)==(0,0)
    w(u,PRIMARY[0],0xffff);w(u,EXTRA[0],0) # view transition resets legacy input
    assert tick(base,extended)==(0,0)
    assert tick()==(0,0) # one released sample is a dropout
    assert tick(base,extended)==(0,0)
    assert tick(base,extended,valid=False)==(0,0)
    assert tick(base,extended)==(0,0)
    assert tick()==tick()==(0,0)
    assert tick(base,extended)==target
    # A quick tap received across VBlanks before the gameplay tick is delivered once.
    tick();tick()
    tick(base,extended,consume=False);tick(consume=False);tick(consume=False)
    assert tick()==target
    assert tick()==(0,0)
    # A retains native level and release, with no new latency.
    tick(64);assert not (rd(u,PRIMARY[0])&64)
    tick();assert rd(u,PRIMARY[0])&64
u,tick=pad(R)
assert tick(extended=8)==(0,8)
for i in range(5):
    tick(valid=False)
    assert rd(u,0xffff0144)==8
for i in range(2):tick(valid=False)
assert rd(u,0xffff0144)==0
# Mouse Off sleep used to wake on Start's held level. Check the actual gate.
u,tick=pad(R)
held_wake=0x709a
wait=0x7112
tick(128);tick(128)
run(u,0x708e,wait)
tick();tick()
run(u,0x708e,wait) # Start release is not wake either
w(u,VIEW,0x7070,4)
tick(128);tick(128);tick();tick() # latest snapshot lost the press, latch retains it
run(u,0x708e,held_wake)
assert not (rd(u,PRIMARY[1])&128)
print('PASS all seven consumed press edges, quick taps, rearm, dropout and Start sleep gate; A remains held input')
