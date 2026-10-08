from datetime import datetime,timezone
import random,uuid
HOSTS=["WIN-CLIENT-01","WIN-SRV-01","LINUX-WEB-01"];USERS=["alice","bob","svc-backup"]
def base(cat,msg,**kw):
    x={"@timestamp":datetime.now(timezone.utc).isoformat(),"event":{"kind":"event","category":cat,"dataset":"soc.simulator"},"host":{"name":random.choice(HOSTS)},"user":{"name":random.choice(USERS)},"message":msg,"observer":{"name":"SOC-LAB"},"event_id":str(uuid.uuid4())};x.update(kw);return x
def baseline(n): return [base("system","Routine system activity") for _ in range(n)]
def brute_force(): return [base("authentication","Failed login",source={"ip":"10.10.20.55"},event={"kind":"event","category":"authentication","outcome":"failure","dataset":"soc.simulator"}) for _ in range(6)]+[base("authentication","Successful login after repeated failures",source={"ip":"10.10.20.55"},event={"kind":"event","category":"authentication","outcome":"success","dataset":"soc.simulator"})]
def powershell(): return [base("process","powershell.exe -EncodedCommand SQBFAFgA",process={"name":"powershell.exe","command_line":"powershell.exe -EncodedCommand SQBFAFgA"},threat={"indicator":{"type":"encoded_command"}})]
def phishing(): return [base("email","User received invoice.zip attachment",threat={"indicator":{"type":"phishing_attachment"}},email={"attachment":{"name":"invoice.zip"}})]
def exfil(): return [base("network","Large outbound transfer",source={"ip":"10.10.20.21"},destination={"ip":"198.51.100.25","port":443},network={"bytes":125000000},threat={"indicator":{"type":"unusual_transfer"}})]
def all_scenarios(): return baseline(10)+brute_force()+powershell()+phishing()+exfil()
