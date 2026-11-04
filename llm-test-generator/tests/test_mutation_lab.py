from mutants.mutation_lab import run_mutations

def test_mutation_lab_kills_injected_defects():
    report=run_mutations()
    assert report['off_by_one']['killed'] is True
    assert report['no_lower_bound']['killed'] is True
    assert report['always_valid']['killed'] is True
    assert report['mutation_score']==1.0
