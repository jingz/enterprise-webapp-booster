#! ../../venv/bin/python

from jinja2 import Environment
from hamlish_jinja import HamlishExtension

env = Environment(extensions=[HamlishExtension])

tpl = '''
%html
    %head -> %title -> REPORT PDF
    %style
        table { width 50%; }
        th, td {
            text-align: center;
        }
        th {
            font-size: 1.2em;
            padding: 0.3em;
            border-bottom-size: 2px;
        }
    %body -> %table repeat="1"
        %thead -> %tr
            %th -> client name
            %th -> client code
            %th -> id no
            %th -> birth date
            %th -> created date
        %tbody
           -for i in range(10000):
            %tr
                %td -> client name {{ i }}
                %td -> client code 000{{ i }}
                %td -> id no 990{{ i }}
                %td -> birth date bbb{{ i }}
                %td -> created at time {{ i }}
'''

env.hamlish_mode = 'debug'
env.hamlish_file_extensions = ('.haml',)
env.hamlish_enable_div_shortcut = True
print env.hamlish_from_string(tpl).render()
