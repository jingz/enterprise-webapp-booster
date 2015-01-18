#! ../env/bin/python
# -*- coding: utf-8 -*-
from enlighten import create_app
from enlighten.models import *


class TestEltAppMenu:
    def setup(self):
        app = create_app('enlighten.settings.DevConfig', env='dev')
        self.app = app.test_client()
        db.app = app
        # db.create_all()

    def teardown(self):
        db.session.remove()
        # db.drop_all()

    def test_build_menu_tree(self):
        lmenu = [ { 'id': 1, 'parent_id': None, 'code': 'ROOT', 'text': 'ROOT', 'url': None },
                { 'id': 2, 'parent_id': 1, 'code': 'TEST001', 'text': 'test 001', 'url': '#/test/1' },
                { 'id': 3, 'parent_id': 1, 'code': 'TEST002', 'text': 'test 002', 'url': '#/test/2' },
                { 'id': 4, 'parent_id': 3, 'code': 'TEST003', 'text': 'test 003', 'url': '#/test/3' } ]

        lmenu = [EltAppMenu(**o) for o in lmenu]
        tree = EltAppMenu.build_menu_tree(lmenu)

        assert tree['code'] == 'ROOT'
        assert len(tree['childrens']) == 2
        assert tree['childrens'][1]['code'] == 'TEST002'
        assert len(tree['childrens'][1]['childrens']) == 1

