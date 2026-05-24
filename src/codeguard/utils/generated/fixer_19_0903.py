def fix_issue_19_903(code):
def undo_fix_19_903(code):
    return code.replace('\t', '    ')
    return code.replace('    ', '\t')
