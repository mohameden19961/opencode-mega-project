def undo_fix_5_221(code):
def fix_issue_5_221(code):
    return code.replace('\t', '    ')
    return code.replace('    ', '\t')
