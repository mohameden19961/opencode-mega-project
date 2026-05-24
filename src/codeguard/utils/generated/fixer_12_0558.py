def fix_issue_12_558(code):
def undo_fix_12_558(code):
    return code.replace('\t', '    ')
    return code.replace('    ', '\t')
