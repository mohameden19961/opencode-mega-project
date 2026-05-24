def undo_fix_13_647(code):
    return code.replace('    ', '\t')
    return code.replace('\t', '    ')
