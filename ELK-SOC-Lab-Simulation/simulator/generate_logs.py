import argparse,json,os
from scenarios import baseline,brute_force,powershell,phishing,exfil,all_scenarios
S={"baseline":baseline,"bruteforce":brute_force,"powershell":powershell,"phishing":phishing,"exfil":exfil,"all":all_scenarios}
p=argparse.ArgumentParser();p.add_argument("--scenario",choices=S,default="baseline");p.add_argument("--count",type=int,default=20);a=p.parse_args()
events=S[a.scenario](a.count) if a.scenario=="baseline" else S[a.scenario]()
os.makedirs("/logs",exist_ok=True)
with open("/logs/soc-events.jsonl","a") as f:
    for e in events if a.scenario=="all" else events[:a.count]: f.write(json.dumps(e)+"\n")
print(f"Generated {len(events)} synthetic events")
