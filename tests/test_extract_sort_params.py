#! ../venv/bin/python
# -*- coding: utf-8 -*-
from enlighten import create_app
from enlighten.models import *

class TestExtractSortParams:
    def setup(self):
        app = create_app('enlighten.settings.DevConfig', env='dev')
        self.app = app.test_client()
        db.app = app

    def test_basic_sort(self):
        res = Client.grep_sort_opt("sort_by_title", "asc_1")
        assert res == ("title", "asc", 1)

        res = Client.grep_sort_opt("sort_by_not_title", "asc_1")
        assert res == (None, None, None)

    def test_build_sort(self):
        params = { 'sort_by_title': 'asc_1' }
        res = Client.build_sort_clause(params)
        assert res == "title asc"

        params = { 'sort_by_title': 'asc' }
        res = Client.build_sort_clause(params)
        assert res == "title asc"

    def test_not_build_sort(self):
        params = { 'sort_by_not_column_in_client': 'asc' }
        res = Client.build_sort_clause(params)
        assert res == ""

    def test_build_capital_sort(self):
        params = { 'sort_by_title': 'ASC_1' }
        res = Client.build_sort_clause(params)
        assert res == "title ASC"

    def test_not_match_key_build_sort(self):
        params = { 'title': 'asc' }
        res = Client.build_sort_clause(params)
        assert res == ""

    def test_build_multi_sort(self):
        params = { 'sort_by_title': 'asc_1', 'sort_by_client_code': 'desc_2' }
        res = Client.build_sort_clause(params)
        assert res == "title asc, client_code desc"

        params = { 'sort_by_title': 'asc_2', 'sort_by_client_code': 'desc_1' }
        res = Client.build_sort_clause(params)
        assert res == "client_code desc, title asc"
