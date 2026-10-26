exec(open('v34/common.py').read())
# Native polling stub feeds normalized events. Record text and plane clear commands.
def ui(events,start=None,stop=None,init=None):
 u=machine();w(u,0xffff0004,65535);w(u,0xffff0014,0,1);w(u,0xffff0015,255,1)
 if init:init(u)
 it=iter(events);tiles={};clears=[]
 def hk(uc,a,s,d):
  if a==stop:uc.emu_stop();return
  if a==0x31b0:clears.append((uc.reg_read(UC_M68K_REG_D2)&65535,uc.reg_read(UC_M68K_REG_D1)&65535));ret(uc)
  elif a in [0x1612,0x1646,0x2930,0xf7b2,0x150b4]:ret(uc)
  elif a==0x35fe:tiles[uc.reg_read(UC_M68K_REG_D2)&65535]=uc.reg_read(UC_M68K_REG_D0)&65535;ret(uc)
  elif a==0x53a8:
   try:mask=next(it)
   except StopIteration:uc.emu_stop();return
   w(uc,0xffff0006,rd(uc,0xffff0004));w(uc,0xffff0004,mask);uc.reg_write(UC_M68K_REG_D0,mask);ret(uc)
 u.hook_add(UC_HOOK_CODE,hk);u.reg_write(UC_M68K_REG_A7,0xfffffe00);w(u,0xfffffe00,STOP,4);u.emu_start(start or L['options14'],STOP,count=2000000)
 return u,tiles,clears
