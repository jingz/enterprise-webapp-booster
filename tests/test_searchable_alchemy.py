#! ../venv/bin/python
# -*- coding: utf-8 -*-
from enlighten import create_app
from enlighten.models import *
import re

class TestModels:
    def setup(self):
        app = create_app('enlighten.settings.DevConfig', env='dev')
        self.app = app.test_client()
        db.app = app
        # db.create_all()

    def teardown(self):
        pass
        # db.session.remove()
        # db.drop_all()

    def test_sanitize_contained_keys(self):
        di = { 'client_code': 123, 'id': 2 }
        res = Client.sanitize(di)
        assert len(res.keys()) == 2

    def test_sanitize_not_contained_keys(self):
        di = { 'this_is_not_a_field': 'test' }
        res = Client.sanitize(di)
        assert len(res.keys()) == 0

    def test_grep_search_opt(self):
        col, opt = Client.grep_search_opt('client_code_like')
        assert col == 'client_code'
        assert opt == 'like'

        col, opt = Client.grep_search_opt('client_code_not_like')
        assert col == 'client_code'
        assert opt == 'not_like'

        col, opt = Client.grep_search_opt('client_code_eq_like')
        assert col is None
        assert opt is None

        col, opt = Client.grep_search_opt('client_code_eq')
        assert col == 'client_code'
        assert opt == 'eq'

        col, opt = Client.grep_search_opt('client_code_not_eq')
        assert col == 'client_code'
        assert opt == 'not_eq'

        col, opt = Client.grep_search_opt('xxxx')
        assert col is None
        assert opt is None

    def test_simple_build_search_clause(self):
        test_params = { 'client_code_eq': '12345' }
        clause, params = Client.build_search_clause(test_params)
        assert clause == "client_code = :client_code_eq"
        assert params == test_params

        test_params = { 'client_code_not_eq': '12345'}
        clause, params = Client.build_search_clause(test_params)
        assert clause == "client_code <> :client_code_not_eq"
        assert params == test_params

    def test_simple_build_search_clause_without_opt(self):
        test_params = { 'client_code': '12345' }
        clause, params = Client.build_search_clause(test_params)
        assert clause == "client_code = :client_code"
        assert params == test_params


    def test_build_search_with_in_operator(self):
        test_params = { 'client_code_in': ['12345', '99999'] }
        clause, params = Client.build_search_clause(test_params)
        assert clause == "client_code in (:client_code_in_1, :client_code_in_2)"
        assert params == { 'client_code_in_1': '12345', 
                            'client_code_in_2': '99999' }

    def test_build_search_with_in_operator_and_integer(self):
        test_params = { 'client_code_in': [12345, 99999] }
        clause, params = Client.build_search_clause(test_params)
        assert clause == "client_code in (:client_code_in_1, :client_code_in_2)"
        assert params == { 'client_code_in_1': 12345, 
                            'client_code_in_2': 99999 }

    def test_build_search_with_not_in_operator_and_integer(self):
        test_params = { 'client_code_not_in': [12345, 99999] }
        clause, params = Client.build_search_clause(test_params)
        assert clause == "client_code not in (:client_code_not_in_1, :client_code_not_in_2)"
        assert params == { 'client_code_not_in_1': 12345, 
                            'client_code_not_in_2': 99999 }

    def test_build_search_with_like_operator_and_integer(self):
        test_params = { 'client_code_like': '12345' }
        clause, params = Client.build_search_clause(test_params)
        assert clause == "client_code like :client_code_like"
        assert params == { 'client_code_like': '%12345%' }

        test_params = { 'client_code_like': '%12345%' }
        clause, params = Client.build_search_clause(test_params)
        assert clause == "client_code like :client_code_like"
        assert params == { 'client_code_like': '%12345%' }

        test_params = { 'client_code_like': '12345%' }
        clause, params = Client.build_search_clause(test_params)
        assert clause == "client_code like :client_code_like"
        assert params == { 'client_code_like': '12345%' }

    def test_build_search_with_not_like_operator_and_integer(self):
        test_params = { 'client_code_not_like': '12345' }
        clause, params = Client.build_search_clause(test_params)
        assert clause == "client_code not like :client_code_not_like"
        assert params == { 'client_code_not_like': '%12345%' }

        test_params = { 'client_code_not_like': '%12345%' }
        clause, params = Client.build_search_clause(test_params)
        assert clause == "client_code not like :client_code_not_like"
        assert params == { 'client_code_not_like': '%12345%' }

        test_params = { 'client_code_not_like': '%12345' }
        clause, params = Client.build_search_clause(test_params)
        assert clause == "client_code not like :client_code_not_like"
        assert params == { 'client_code_not_like': '%12345' }

    def test_build_search_with_lt_operator_and_integer(self):
        test_params = { 'client_code_lt': '12345' }
        clause, params = Client.build_search_clause(test_params)
        assert clause == "client_code < :client_code_lt"
        assert params == { 'client_code_lt': '12345' }

        test_params = { 'client_code_lte': '12345' }
        clause, params = Client.build_search_clause(test_params)
        assert clause == "client_code <= :client_code_lte"
        assert params == { 'client_code_lte': '12345' }

    def test_build_search_with_gt_operator_and_integer(self):
        test_params = { 'client_code_gt': '12345' }
        clause, params = Client.build_search_clause(test_params)
        assert clause == "client_code > :client_code_gt"
        assert params == { 'client_code_gt': '12345' }

        test_params = { 'client_code_gte': '12345' }
        clause, params = Client.build_search_clause(test_params)
        assert clause == "client_code >= :client_code_gte"
        assert params == { 'client_code_gte': '12345' }

    def test_build_search_with_gt_and_lt_operator_and_integer(self):
        test_params = { 'client_code_gt': '12345', 'client_code_lt': '99999' }
        clause, params = Client.build_search_clause(test_params)
        assert clause == "client_code > :client_code_gt and client_code < :client_code_lt"
        assert params == { 'client_code_gt': '12345', 'client_code_lt': '99999' }

    def test_not_build_search_clause(self):
        clause, params = Client.build_search_clause({ 'xx_eq': '12345' })
        assert clause == ""
        assert params == {}

    def test_search(self):
        code = Client.query.first().client_code
        if code:
            c = Client.search({ 'client_code_eq': code })
            assert c.one().client_code == code

    def test_search_not_eq(self):
        code = Client.query.first().client_code
        if code:
            clients = Client.search({'client_code_not_eq': code })
            assert code != clients.first().client_code

    def test_search_in(self):
        code = Client.query.first().client_code
        if code:
            c = Client.search({ 'client_code_in': [code, '123123'] })
            assert c.first().client_code == code
            assert c.count() == 1

    def test_search_in_without_key(self):
        code = Client.query.first().client_code
        if code:
            c = Client.search({ 'client_code': code })
            assert c.first().client_code == code
            assert c.count() == 1


    # def test_search(self):
    #     test_client_code = '03075'
    #     c = Client.search({'client_code_eq': '03075'}).one()
    #     assert c.client_code == test_client_code

