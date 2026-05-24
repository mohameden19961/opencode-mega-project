def undo_fix_1_24(code):
    return code.replace('    ', '\t')
    return code.replace('\t', '    ')
