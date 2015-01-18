from app.models import db
from mixins import BaseMixin, UserstampMixin, TimestampMixin
from types import LambdaType

class AppMenu(BaseMixin, UserstampMixin, TimestampMixin, db.Model):
    __tablename__ = 'app_menu'

    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, nullable=True)
    code = db.Column(db.String(10))
    text = db.Column(db.String())
    url = db.Column(db.String())

    @classmethod
    def build_menu_tree(cls, lmenu, root_node=None, formatter=None):
        ''' build menu tree from list of menu
            it can custom format tree by giving formatter - lambda fn
            accepting an the object menu and its children as arguments and returning dict
        '''

        # if root node is None
        # find root first, the list should containt a root, parent_id is None
        if root_node is None:
            root_node = [o for o in lmenu if o.parent_id is None][0]
            if root_node is None: raise error('root node is not found!')
            menu_tree = cls.build_menu_tree(lmenu, root_node, formatter=formatter)
        else:
            # find childrens from lmenu
            children = [o for o in lmenu if o.parent_id == root_node.id]

            # default format
            menu_tree = {}
            menu_tree['code'] = root_node.code
            menu_tree['text'] = root_node.text
            menu_tree['url'] = root_node.url
            if isinstance(formatter, LambdaType):
                menu_tree = formatter(root_node, children)

            if len(children) > 0:
                menu_tree['children'] = [cls.build_menu_tree(lmenu, o, formatter=formatter) for o in children]

        return menu_tree
