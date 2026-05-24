def fix_issue_17_803(code):
    return code.replace('\t', '    ')
    return code.replace('    ', '\t')
