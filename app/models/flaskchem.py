#!/usr/bin/env python
import sys
import re

def translate(text, trans_map):
    out_text = text
    for word in trans_map.keys():
        #out_text = out_text.replace(word, trans_map[word])
        patt = re.compile('([^\.])(%s)' % word)
        out_text = re.sub(patt, '\\1%s' % trans_map[word], out_text)
    return out_text

def translate_flaskchem(content):
    lines = content.split('\n')
    out_lines = ['from app.models import db', '']
    translate_map = {
        'Base': 'db.Model',
    }

    import_lines = [ line for line in lines if ('import' in line) and ('from' in line)]
    kls_words = []
    for import_line in import_lines:
        kls_words.extend( kls_word.strip() for kls_word in import_line.split('import')[1].split(',') )
    for kls_word in kls_words:
        translate_map[kls_word] = 'db.%s' % kls_word

    found_class = False
    for line in lines:
        if line.lstrip().startswith('class'):
            found_class = True
        if not found_class: continue
        out_lines.append(translate(line, translate_map))
            
    return '\n'.join(out_lines)

if __name__ == '__main__':
    try:
        in_file = sys.argv[1]
    except IndexError:
        in_file = None

    if in_file:
        in_fd = open(in_file)
    else:
        in_fd = sys.stdin

    print translate_flaskchem(in_fd.read())
