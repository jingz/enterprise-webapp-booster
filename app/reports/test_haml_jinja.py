#! ../venv/bin/python

from jinja2 import Environment
from hamlish_jinja import HamlishExtension

env = Environment(extensions=[HamlishExtension])


tpl = '''
<?xml version="1.0" encoding="utf-8" standalone="no" ?>
<!DOCTYPE document SYSTEM "rml.dtd">
%document filename="example.pdf"
    %stylesheet

    %pageDrawing
        %drawCentredString x="4.lin" y="5.8lin"
            Hello World!
'''

env.hamlish_mode = 'debug'
env.hamlish_file_extensions = ('.haml',)
env.hamlish_enable_div_shortcut = True

print env.hamlish_from_string(tpl).render()
