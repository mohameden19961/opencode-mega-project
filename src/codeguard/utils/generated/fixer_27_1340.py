def fix_issue_27_1340(code):
    return code.replace('    ', '\t')
def undo_fix_27_1340(code):
    return code.replace('\t', '    ')
