def fix_issue_37_1832(code):
def undo_fix_37_1832(code):
    return code.replace('    ', '\t')
    return code.replace('\t', '    ')
