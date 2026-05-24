def undo_fix_12_578(code):
    return code.replace('    ', '\t')
    return code.replace('\t', '    ')
def fix_issue_12_578(code):
