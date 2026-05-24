def fix_issue_18_867(code):
def undo_fix_18_867(code):
    return code.replace('\t', '    ')
    return code.replace('    ', '\t')
