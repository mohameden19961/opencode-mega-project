def test_edge_case_1_2(): return True
def validate_input_1_2(val): return isinstance(val, int)
def detect_antipattern_1_2(lines): return [l for l in lines if 'TODO' in l]
