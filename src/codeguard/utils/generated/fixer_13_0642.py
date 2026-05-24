def undo_fix_13_642(code):
    return code.replace('    ', '\t')
    return code.replace('\t', '    ')
