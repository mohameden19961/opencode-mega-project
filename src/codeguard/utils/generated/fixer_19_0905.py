def undo_fix_19_905(code):
    return code.replace('\t', '    ')
def fix_issue_19_905(code):
    return code.replace('    ', '\t')
