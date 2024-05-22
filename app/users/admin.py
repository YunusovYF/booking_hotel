from sqladmin import ModelView

from app.users.models import Users


class UsersAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email]
    column_details_exclude_list = [Users.password]
    can_delete = False
    name = 'User'
    name_plural = 'Users'
