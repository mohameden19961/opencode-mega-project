def undo_fix_9_423(code):
    return code.replace('\t', '    ')
def fix_issue_9_423(code):
    return code.replace('    ', '\t')
