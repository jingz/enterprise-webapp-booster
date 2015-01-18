import re

# Enhance Front-End-Like search API for SQLAlchemy Model
class SearchableMixin(object):

    @classmethod
    def search(cls, di, sel=[]):
        """
            SPECS
            SQL         Predication
            =====       ===========
            =           eq
            !=          not_eq 
            LIKE        like
            NOT LIKE    not_like
            <           lt
            >           gt
            <=          lte
            >=          gte
            in          in
            not_in      not_in

        example given "di" argument : { 'name_like': 'jing' }
            generate where clause : name like '%jing%'

        return raw session scoped by the class
        """
        filter_clause, filter_params = cls.build_search_clause(di)
        o = cls.build_sort_clause(di)
        if len(sel) == 0:
            return cls.query.session.query(cls).filter(filter_clause).params(**filter_params).order_by(o)
        else:
            return cls.query.session.query(*sel).filter(filter_clause).params(**filter_params).order_by(o)

    search_opt_regexp = r'(((?<!not)_eq)|(_not_eq)|((?<!not)_like)|(_not_like)|((?<!not)_contains)|(_not_contains)|(_lt)|(_gt)|(_lte)|(_gte)|((?<!not)_in)|(_not_in))$'
    search_opt_mapper = {
        'eq': '=',
        'not_eq': '<>',
        'like': 'like',
        'contains': 'like',
        'not_like': 'not like',
        'not_contains': 'not like',
        'lt': '<',
        'gt': '>',
        'gte': '>=',
        'lte': '<=',
        'in': 'in',
        'not_in': 'not in',
    }

    search_opt_text_mapper = {
        'eq': 'equal to',
        'not_eq': 'not equal to',
        'like': 'contains',
        'contains': 'contains',
        'not_like': 'not contains',
        'not_contains': 'not contains',
        'lt': 'less than',
        'gt': 'greater than',
        'gte': 'greater than and equal to',
        'lte': 'less than and equal to',
        'in': 'in any',
        'not_in': 'not in any',
    }

    @classmethod
    def readable_search_clause(cls, di, transform_key=True):
        text = []
        for k, v in di.items():
            col, opt = cls.grep_search_opt(k)
            if col and opt:
                read_pattern = u"{col} {text_opt} {v}" 
                to = cls.search_opt_text_mapper.get(opt)
                _col = col
                if transform_key:
                    _col = _col.title().replace('_', ' ')
                text.append(read_pattern.format(col=_col, text_opt=to, v=v))
        return u" and ".join(text)

    @classmethod
    def build_search_clause(cls, di):
        filter_clause = []
        filter_params = {}
        for k, v in di.items():
            col, opt = cls.grep_search_opt(k)
            if col and opt:
                __where = "{col} {opt} :{column_param}" 
                sql_opt = cls.search_opt_mapper.get(opt)

                if opt in ('like', 'not_like', 'contains', 'not_contains'):
                    # wrap value with '%' 
                    if isinstance(v, basestring):
                        if re.match('^%.*', v) or re.match('.*%$', v):
                            pass
                        else:
                            v = u"%{0}%".format(v)

                if opt == 'in' or opt == 'not_in':
                    # in is a special case to
                    # serialize value and key into where statement
                    in_params_series = [] # :column_name_key_1 ...
                    n = len(v)
                    i = 1
                    while n != 0:
                        _k = ":%s_%d" % (k, i)
                        in_params_series.append(_k)
                        # set binding params
                        filter_params.setdefault(_k[1:], v[i-1])
                        i += 1
                        n -= 1
                        
                    __where = u"{col} {opt} (%s)" % ", ".join(in_params_series)
                    filter_text = __where.format(col=col, opt=sql_opt)
                    filter_clause.append(filter_text)
                    continue

                if sql_opt is not None:
                    filter_text = __where.format(col=col, opt=sql_opt, column_param=k)
                    filter_clause.append(filter_text)
                    filter_params.setdefault(k, v)
                else:
                    continue
            else:
                continue

        filter_clause = " and ".join(filter_clause)
        return (filter_clause, filter_params)

    @classmethod
    def grep_search_opt(cls, text):
        match = re.search(cls.search_opt_regexp, text);
        if match is not None:
            col, _ = text.split(match.group(0)) # client_code, ''
            opt = match.group(0)[1:] # remove a leading _ 
            # match but the matched column is not in mapper
            if col not in [__col.name for __col in cls.__mapper__.c]:
                col = opt = None
        # could be just column name
        elif text in [__col.name for __col in cls.__mapper__.c]:
            col = text
            opt = 'eq'
        else:
            col = opt = None
        return (col, opt)

    @classmethod
    def build_sort_clause(cls, di):
        orders = []
        for k, v in di.items():
            col, direction, priority = cls.grep_sort_opt(k, v)
            if col is not None:
                orders.append({ 'column': col, 'direction': direction,
                    'priority': priority})

        # sort order by priority
        if len(orders) > 0:
            proc = lambda k: k['priority']
            order_pattern = u"{column} {direction}"
            return ", ".join([order_pattern.format(**d) for d in sorted(orders, key=proc)]) 
        else:
            return ""

    sort_key_regexp = r'^sort_by_(.*)'
    sort_value_regexp = r'(asc|desc)_?((?<=)\d+)?' # asc_1
    @classmethod
    def grep_sort_opt(cls, key_text, value_text):
        match_key = re.search(cls.sort_key_regexp, key_text)
        match_val = re.search(cls.sort_value_regexp, value_text, re.IGNORECASE)
        if match_key is not None and match_val is not None:
            col = match_key.group(1) # client_code
            direction, priority = match_val.group(1), match_val.group(2)
            if direction is None: 
                direction = "ASC"

            if priority is None:
                priority = 99
            else:
                priority = int(priority)

            # match but the matched column is not in mapper
            if col not in [__col.name for __col in cls.__mapper__.c]:
                col = direction = priority = None
        else:
            col = direction = priority = None

        return (col, direction, priority)

    @classmethod
    def sanitize(cls, params):
        sanitize_dict = {}
        for col in cls.__mapper__.c:
           v = params.get(col.name)
           if v is not None:
               sanitize_dict.setdefault(col.name, v)
        return sanitize_dict
