from .. import db, Client

class SampleInq(Client):
    _title = 'Client Inquiry'

    _filters = 'client_code', \
               'status', \
               'birth_date'

    _grid_display_columns = 'client_code', \
        { 'Client Name TH': { convert: lambda r: r.client_firstname_lc + ' ' + r.client_lastname_lc } }, \
        { 'Client Name TH': { convert: lambda r: r.client_firstname_lc + ' ' + r.client_lastname_lc } }, \
        { 'Client Name TH': { convert: lambda r: r.client_firstname_lc + ' ' + r.client_lastname_lc } }, \
        { 'Client Name TH': { convert: lambda r: r.client_firstname_lc + ' ' + r.client_lastname_lc } }, \
        { 'Client Name TH': { convert: lambda r: r.client_firstname_lc + ' ' + r.client_lastname_lc } }, \

    _grid_header_group = ''
    _group_field = ''

    _paginated = True # default
    _page_size = 100 # default

    _grand_summary = ('list of columns')
    _page_summary = ('list of columns')

    _hide_group_column = 'column name'
    _group_header_template = 'template multi line string'
    _group_footer_template = 'template multi line string'

    _sortable = False # not allow sorting on any column in grid

    @classmethod
    def hand_query(cls, params):
        # do unbelievable complex query !
        # ..
        total = cls.query.count('*')
        data =  cls.query.limit(20)

        result = { 'success': True, 'data': data, 'total': total }
        return
