from app.models import db
from mixins import BaseMixin, UserstampMixin, TimestampMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import event

class User(BaseMixin, UserstampMixin, TimestampMixin, db.Model):

    #-#-#-#-#---------------------------------------------------------
    __tablename__ = 'user'

    # username: username
    username = db.Column(db.String(20), nullable=False)

    # password: encrypted password
    password = db.Column(db.String)

    # first_name: user first name
    first_name = db.Column(db.String(100))

    # last_name: user last name
    last_name = db.Column(db.String(100))

    # email: user email address
    email = db.Column(db.String(100))

    # branch_id: reference to user branch (if applicable)
    branch_id = db.Column(db.Integer)

    # soft_password_expiration_date: first date that require user to change password
    soft_password_expiration_date = db.Column(db.Date)

    # hard_password_expiration_date: date that user will be automatically disabled
    hard_password_expiration_date = db.Column(db.Date)

    # failed_login_count: a number of consecutive login fail
    failed_login_count = db.Column(db.Integer)

    # status: user status
    #   1) Active   --> A
    #   2) Closed   --> C
    status = db.Column(db.String(1), nullable=False, default='A')
    #-#-#-#-#---------------------------------------------------------

    # created_at = db.Column(db.DateTime, default=db.func.now())
    # updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    roles = db.relationship('Role', 
                            secondary='user_role', 
                            backref=db.backref('users'))

    perms = db.relationship('ApiPermission', 
                            secondary='user_permission', 
                            backref=db.backref('users'))

    not_allow_perms = db.relationship('ApiPermission',
            secondary='user_not_allow_permission',
            backref=db.backref('not_allow_users'))

    # def __init__(self, username, password, status, created_by):
    #     self.username = username
    #     self.set_password(password)
    #     self.status = status
    #     self.created_by = self.updated_by = created_by

    def get_menu_list(self):
        ms = []
        for role in self.roles:
            for menu in role.menus:
                # TODO check uniq menu id
                ms.append(menu)
        return ms

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.status == 'A'

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def set_password(self, clear_password):
        self.password = generate_password_hash(clear_password, method='pbkdf2:sha512:10000')

    def verify_password(self, clear_password):
        return check_password_hash(self.password, clear_password)

    def get_roles(self):
        """ return all roles attached to this user """
        return [ user_role.role for user_role in self.user_roles ]

    def get_all_detail_permissions(self):
        """ return unique detail permissions from all roles attached to this user """
        roles = self.get_roles()
        all_detail_perms = []
        for role in roles:
            all_detail_perms.extend( role.get_resolved_detail_permissions() )
        return { perm: True for perm in all_detail_perms }.keys()

    def get_menu(self):
        """ return personalized menu for this user based on roles
            attached to this user
        """
        roles = self.get_roles()
        all_group_perms = []
        for role in roles:
            all_group_perms.extend( role.get_group_permissions() )
        all_group_perms = { perm: True for perm in all_group_perms }.keys()
        return get_reduced_menu(menu, all_group_perms)

    #def __repr__(self):
    #    return '<User %r>' % self.username
    
    @classmethod
    def authenticate(cls, username, given_password):
        user = cls.query.filter_by(username=username).first()
        if bool(user) and user.verify_password(given_password):
            return user
        return None


# after create instance from user
@event.listens_for(User, 'init')
def receive_init(inst, args, kwargs):
    ''' set nescessary values
    '''
    pwd = kwargs.pop('password', None)
    if pwd: inst.set_password(pwd)
    inst.status = 'A'
    return inst
