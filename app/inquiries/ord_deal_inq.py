from ..models import db, EltOrdDeal

class OrdDealInq(EltOrdDeal):
    _title = 'Order Deal Inquiry'

    _filters = ( 'sec_symbol',
                 'order_date' )

    _display_columns = ('client_code',
                        ( 'sec_symbol', { 'text': 'Symbol', 'not_print': True} ),
                        ('qty', { 'type': 'integer', 'summaryType': 'sum' }),
                        'x_order_no', 
                        'confirm_no',
                        ('commission', { 'summaryType': 'avg' }),
                        ('fee', { 'summaryType': 'max' }),
                        ('ae_code', { 'summaryType': 'count'}),
                        'order_no',
                        ('fullname_lc', { 'text': 'Fullname' }),
                        # ('client_firstname_lc', { 'text': 'Firstname' }),
                        ('net_amount', { 'summaryType': 'min' } ),
                        'order_date')

    # grid only options
    _grid_header_group = ''
    _group_field = 'sec_symbol'
    _paginated = True # default
    _grid_size = 100 # default for grid
    _grand_summary = ('list of columns')
    _page_summary = ('list of columns')
    # ---------------------------------------------

    # pdf options
    _pdf_size = 'A4'
    _pdf_layout = 'l' # landscape or 'p', portrait
    # ---------------------------------------------

    _hide_group_column = 'column name'
    _group_header_template = 'Group By {sec_symbol}'
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
