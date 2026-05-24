def fix_issue_4_196(code):
def undo_fix_4_196(code):
    return code.replace('    ', '\t')
    return code.replace('\t', '    ')
