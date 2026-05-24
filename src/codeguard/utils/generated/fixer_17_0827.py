def undo_fix_17_827(code):
    return code.replace('    ', '\t')
def fix_issue_17_827(code):
    return code.replace('\t', '    ')
