def undo_fix_6_290(code):
    return code.replace('\t', '    ')
def fix_issue_6_290(code):
    return code.replace('    ', '\t')
