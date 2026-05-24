def undo_fix_1_32(code):
    return code.replace('\t', '    ')
    return code.replace('    ', '\t')
