#!/usr/bin/env python

import os
import sys
import getopt
import re
import json

from enlighten import create_app
from enlighten.models import *
from enlighten.inquiries import *
from sqlalchemy.sql import sqltypes
from string import Template

env = os.environ.get('ENLIGHTEN_ENV', 'dev')
config_name = 'enlighten.settings.%sConfig' % env.capitalize()
app = create_app(config_name, env)

# parsing option
optlist, args = getopt.getopt(sys.argv[1:], 'n:')
optdict = dict(optlist)

model = optdict.get('-n', 'OrdDealInq')

# CamelCase -> camel_case
def convert(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

with app.app_context():
    m = eval(model)
    _title = getattr(m, '_title', 'No Title')
    _filters = getattr(m, '_filters', ())
    _display_columns = getattr(m, '_display_columns', ())
    _group_field = getattr(m, '_group_field', None)
    # TODO
    _grid_header_group = getattr(m, '_grid_header_group', None)
    _paginated = getattr(m, '_paginated', True)
    _page_size = getattr(m, '_page_size', 100)
    _grand_summary = getattr(m, '_grand_summary', ())
    _page_summary = getattr(m, '_page_summary', ())
    _hide_group_column = getattr(m, '_hide_group_column', '')
    _group_header_template = getattr(m, '_group_header_template', '')
    _group_footer_template = getattr(m, '_group_footer_template', '')

    def __make_inline_conf(conf):
        if len(conf) > 0:
            inline = [":{0}({1})".format(k, v) for k, v in conf.iteritems()]
            return " ".join(inline)
        else:
            return ""

    # Prepare filter code
    filter_code = []
    for i, c in enumerate(_filters):
        filt_name, conf = None, {}
        if isinstance(c, tuple):
            filt_name, conf = c
        else:
            filt_name = c

        filt_in_model = getattr(m.__mapper__.c, filt_name, None)
        filt_id = filt_name.replace('_', '-')
        if filt_in_model is not None:
            _type = filt_in_model.type if not conf.get('type') else conf.get('type')
            if conf.get('type'):
                del conf['type']

            inline_conf = __make_inline_conf(conf)

            if isinstance(_type, sqltypes.DateTime) or _type == 'datetime':
                date_template = '''
          - fieldcontainer#${filt_id}@{ %s }:
            - datefield#${filt_id}-gte@{ :name(${filt_name}_gte) }
            - datefield#${filt_id}-lte@{ :name(${filt_name}_lte) }''' % inline_conf
                __temp = Template(date_template)
                __code = __temp.substitute({'filt_id': filt_id, 'filt_name': filt_name})
                filter_code.append(__code)
            elif isinstance(_type, sqltypes.Date) or _type == 'date':
                date_template = '''
          - fieldcontainer#${filt_id}@{ %s }:
            - datefield#${filt_id}-gte@{ :name(${filt_name}_gte) }
            - datefield#${filt_id}-lte@{ :name(${filt_name}_lte) }''' % inline_conf
                __temp = Template(date_template)
                __code = __temp.substitute({'filt_id': filt_id, 'filt_name': filt_name})
                filter_code.append(__code)
            elif _type == 'single_date':
                date_template = '''
          - datefield#${filt_id}@{ :name(${filt_name}_eq) %s }''' % inline_conf
                __temp = Template(date_template)
                __code = __temp.substitute({'filt_id': filt_id, 'filt_name': filt_name})
                filter_code.append(__code)
            elif _type == 'combo' or _type == 'list':
                __temp = '''
          - combo#%s@{ %s }''' % (filt_id, inline_conf)
                filter_code.append(__temp)
            elif isinstance(_type, sqltypes.Numeric) or _type == 'float':
                __temp = '''
          - numberfield#%s@{ %s }''' % (filt_id, inline_conf)
                filter_code.append(__temp)
            elif isinstance(_type, sqltypes.Integer) or _type == 'integer':
                __temp = '''
          - numberfield#%s@{ %s }''' % (filt_id, inline_conf)
                filter_code.append(__temp)
            elif isinstance(_type, sqltypes.Boolean) or _type == 'boolean':
                __temp = '''
          - checkbox#%s@{ %s }''' % (filt_id, inline_conf)
                filter_code.append(__temp)
            else:
                __temp = '''
          - textfield#%s@{ %s }''' % (filt_id, inline_conf)
                filter_code.append(__temp)
        else:
                __temp = '''
          - textfield#%s@{ %s }''' % (filt_id, inline_conf)
                filter_code.append(__temp)

    # end for ------------------------------------------------------
    # Prepare display columns
    adding_config = []
    display_column_code = []
    field_code = []
    for i, c in enumerate(_display_columns):
        col_name, conf = None, {}
        if isinstance(c, tuple):
            col_name, conf = c
        else:
            col_name = c

        col_in_model = getattr(m.__mapper__.c, col_name, None)
        col_id = col_name.replace('_', '-')
        if len(conf) > 0:
            __t = '''%s: %s''' % (col_id, json.dumps(conf))
            adding_config.append(__t)
        if col_in_model is not None:
            _type = col_in_model.type if not conf.get('type') else conf.get('type')
            if conf.get('type', None):
                del conf['type']
            inline_conf = __make_inline_conf(conf)

            if isinstance(_type, sqltypes.DateTime) or _type == 'datetime':
                display_column_code.append(("- gdate#%s@{ %s }" % (col_id, inline_conf)))
                field_code.append({ 'name': col_name, 'type': 'datetiem' })
            elif isinstance(_type, sqltypes.Date) or _type == 'date':
                display_column_code.append(("- gdate#%s@{ %s }" % (col_id, inline_conf)))
                field_code.append({ 'name': col_name, 'type': 'date' })
            elif isinstance(_type, sqltypes.Numeric) or _type == 'float':
                display_column_code.append(("- gnumber#%s@{ :format('0,000.00') %s }" % (col_id, inline_conf)))
                field_code.append({ 'name': col_name, 'type': 'float' })
            elif isinstance(_type, sqltypes.Integer) or _type == "integer":
                display_column_code.append(("- gnumber#%s@{ :format('0,000') %s }" % (col_id, inline_conf)))
                field_code.append({ 'name': col_name, 'type': 'integer' })
            elif isinstance(_type, sqltypes.Boolean) or _type == 'boolean':
                display_column_code.append(("- gboolean#%s@{ %s }" % (col_id, inline_conf)))
                field_code.append({ 'name': col_name, 'type': 'boolean' })
            else:
                # string
                display_column_code.append(("- gtext#%s@{ %s }" % (col_id, inline_conf)))
                field_code.append({ 'name': col_name, 'type': 'string' })
        else:
            # string
            display_column_code.append(("- gtext#%s@{ %s }" % (col_id, inline_conf)))
            field_code.append({ 'name': col_name, 'type': 'string' })
    # end for ------------------------------------------------------

    inq_template = '''
:engine:
  :noid: true
:layout:
  div#inq-wrapper@{ :model($model_name) }:
    fieldset@{ :padding(5) :border(false) }:
    - - grid#grd@{ :title(null) :margin(5) }:
        - toolbar:
          - button#export-pdf@{ :text(PDF) }
          - button#export-csv@{ :text(CSV) }
          - button#export-xlsx@{ :text(EXCEL) }
          - tbfill
          - button#expand@{ :text(">") :title(Expand) }
        $display_columns
    - - form#frm-filter:
        $filt_code
        - toolbar:
          - button#search
          - button#clear-filter
:config:
  inq-wrapper:
    plugins: [{ xclass: 'Ext.plugin.ActAsInquiry' }]
  grd:
    plugins: [{ xclass: 'Ext.plugin.MultiSortGrid' }]
    features: [{ ftype: 'groupingsummary' }]
    store: >
      <js>(this.ss = new Ext.data.JsonStore({
              remoteFilter: true,
              remoteGroup: false,
              groupField: '$group_field',
              proxy: { type: 'rest', url: '/inq', reader: { type: 'json', root: 'data' } },
              fields: $fields
          })
      )
      </js>
  paging:
    pageSize: $page_size
    pageSize: <js>this.ss</js>
    '''

    t = Template(inq_template)
    if _paginated:
        display_column_code.append("- paging")

    __display_column_code = ("\n" + " "*8).join(display_column_code)
    if len(filter_code) > 0:
        filter_code.insert(0, "- fieldset#filter@{ :border(true) :width(420) }:")

    print t.substitute(display_columns=__display_column_code,
                      fields=json.dumps(field_code),
                      group_field=_group_field,
                      page_size=_page_size,
                      adding_config=("\n  ").join(adding_config),
                      model_name=m.__name__,
                      filt_code=("").join(filter_code))

    sys.exit(0)
