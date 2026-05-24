def fix_issue_28_1388(code):
def undo_fix_28_1388(code):
    return code.replace('\t', '    ')
    return code.replace('    ', '\t')
