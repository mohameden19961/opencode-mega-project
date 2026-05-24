def undo_fix_27_1318(code):
    return code.replace('\t', '    ')
    return code.replace('    ', '\t')
