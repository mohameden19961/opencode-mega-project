def fix_issue_18_879(code):
def undo_fix_18_879(code):
    return code.replace('    ', '\t')
    return code.replace('\t', '    ')
