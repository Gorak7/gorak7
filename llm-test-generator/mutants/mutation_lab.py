"""Small deterministic mutation lab; mutants are pure local functions."""
def expected_speed_ok(speed): return 1 <= speed <= 5
def mutant_off_by_one(speed): return 1 <= speed < 5
def mutant_no_lower_bound(speed): return speed <= 5
def mutant_always_valid(speed): return True

def run_mutations():
    tests=[(0,False),(1,True),(3,True),(5,True),(6,False)]
    mutants={"off_by_one":mutant_off_by_one,"no_lower_bound":mutant_no_lower_bound,"always_valid":mutant_always_valid}
    report={}
    for name,fn in mutants.items():
        killed=any(fn(value)!=expected for value,expected in tests)
        report[name]={"killed":killed,"cases":len(tests)}
    killed=sum(item["killed"] for item in report.values())
    report["mutation_score"]=killed/len(mutants) if mutants else 0.0
    return report
if __name__=="__main__":
    import json;print(json.dumps(run_mutations(),indent=2))
