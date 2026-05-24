def undo_fix_36_1771(code):
    return code.replace('\t', '    ')
    return code.replace('    ', '\t')
