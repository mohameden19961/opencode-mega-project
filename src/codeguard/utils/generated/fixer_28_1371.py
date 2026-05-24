def fix_issue_28_1371(code):
    return code.replace('\t', '    ')
    return code.replace('    ', '\t')
