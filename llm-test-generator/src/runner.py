from urllib.parse import urlparse
import httpx
ALLOWED_HOSTS={"127.0.0.1","localhost"}
def execute_case(case,base_url:str,timeout:float=5.0)->dict:
 parsed=urlparse(base_url)
 if parsed.scheme!="http" or parsed.hostname not in ALLOWED_HOSTS: raise ValueError("Runner only permits http://localhost or http://127.0.0.1 test targets")
 if not case.path.startswith("/") or "://" in case.path or ".." in case.path: raise ValueError("Unsafe generated path")
 url=base_url.rstrip("/") + case.path
 with httpx.Client(timeout=timeout) as client:
  response=client.request(case.method,url,headers=case.headers,json=case.body)
 return {"name":case.name,"operation_id":case.operation_id,"status":response.status_code,"expected_status":case.expected_status,"passed":response.status_code==case.expected_status}
