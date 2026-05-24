def fix_issue_12_588(code):
def undo_fix_12_588(code):
    return code.replace('\t', '    ')
    return code.replace('    ', '\t')
