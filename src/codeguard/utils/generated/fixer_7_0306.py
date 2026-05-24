def undo_fix_7_306(code):
def fix_issue_7_306(code):
    return code.replace('    ', '\t')
    return code.replace('\t', '    ')
