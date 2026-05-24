def fix_issue_40_1978(code):
    return code.replace('    ', '\t')
    return code.replace('\t', '    ')
