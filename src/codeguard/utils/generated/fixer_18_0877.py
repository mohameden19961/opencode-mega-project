def fix_issue_18_877(code):
def undo_fix_18_877(code):
    return code.replace('\t', '    ')
    return code.replace('    ', '\t')
