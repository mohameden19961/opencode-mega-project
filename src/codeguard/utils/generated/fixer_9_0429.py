def fix_issue_9_429(code):
    return code.replace('\t', '    ')
def undo_fix_9_429(code):
    return code.replace('    ', '\t')
