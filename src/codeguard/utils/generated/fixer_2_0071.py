def undo_fix_2_71(code):
def fix_issue_2_71(code):
    return code.replace('    ', '\t')
    return code.replace('\t', '    ')
