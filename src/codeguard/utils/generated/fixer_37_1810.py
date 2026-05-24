def fix_issue_37_1810(code):
def undo_fix_37_1810(code):
    return code.replace('\t', '    ')
    return code.replace('    ', '\t')
