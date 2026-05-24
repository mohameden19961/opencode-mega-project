def fix_issue_31_1520(code):
    return code.replace('    ', '\t')
    return code.replace('\t', '    ')
def undo_fix_31_1520(code):
