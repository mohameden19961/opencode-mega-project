def fix_issue_14_672(code):
    return code.replace('    ', '\t')
def undo_fix_14_672(code):
    return code.replace('\t', '    ')
