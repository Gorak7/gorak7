from mutants.mutation_lab import run_mutations, MUTANTS

def test_http_mutation_lab_kills_every_mutant():
    report=run_mutations()
    assert report["baseline"]=={"passed":9,"total":9}
    assert report["mutants_total"]==len(MUTANTS)==4
    assert report["mutants_killed"]==4
    assert report["mutation_score"]==1.0
    assert all(item["killed"] for item in report["mutants"].values())
    assert report["mutants"]["off_by_one"]["killed_by_inputs"]==[5]
    assert 0 in report["mutants"]["no_lower_bound"]["killed_by_inputs"]
    assert 6 in report["mutants"]["no_upper_bound"]["killed_by_inputs"]
