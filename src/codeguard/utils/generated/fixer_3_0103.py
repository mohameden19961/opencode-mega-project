def fix_issue_3_103(code):
def undo_fix_3_103(code):
    return code.replace('    ', '\t')
    return code.replace('\t', '    ')
