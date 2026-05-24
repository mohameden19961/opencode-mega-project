def undo_fix_10_452(code):
    return code.replace('    ', '\t')
    return code.replace('\t', '    ')
def fix_issue_10_452(code):
