import os,pty,subprocess,select,time
EOF=object()
class spawn:
 def __init__(self,exe,args,env,encoding,timeout):
  self.fd,slave=pty.openpty();self.p=subprocess.Popen([exe]+args,env=env,stdin=slave,stdout=slave,stderr=slave);os.close(slave);self.timeout=timeout;self.logfile=None;self.pending='';self.before=''
 def sendline(self,s):os.write(self.fd,(s+'\n').encode())
 def expect(self,needle):
  deadline=time.monotonic()+self.timeout
  while True:
   if needle is not EOF and needle in self.pending:
    self.before,self.pending=self.pending.split(needle,1);return
   if time.monotonic()>deadline:raise TimeoutError(self.pending[-2000:])
   if select.select([self.fd],[],[],.2)[0]:
    try:b=os.read(self.fd,65536)
    except OSError:b=b''
    if not b:
     if needle is EOF:self.before=self.pending;return
     raise EOFError(self.pending)
    s=b.decode(errors='replace');self.pending+=s
    if self.logfile:self.logfile.write(s);self.logfile.flush()
