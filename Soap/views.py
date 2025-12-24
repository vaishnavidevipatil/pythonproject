import uuid
from spyne import ServiceBase, rpc
from spyne.model.primitive import Unicode, Boolean
from spyne.model.complex import Iterable
from model import User

# In-memory storage (XML only, no JSON)
USERS = {}


class UserService(ServiceBase):

    @rpc(Unicode, Unicode, Unicode, _returns=Unicode)
    def add_user(ctx, name, email, description):
        user_id = str(uuid.uuid4())
        USERS[user_id] = User(
            id=user_id,
            name=name,
            email=email,
            description=description
        )
        return user_id

    @rpc(Unicode, _returns=User)
    def get_user(ctx, user_id):
        return USERS.get(user_id)

    @rpc(Unicode, Unicode, Unicode, Unicode, _returns=Boolean)
    def update_user(ctx, user_id, name, email, description):
        if user_id in USERS:
            USERS[user_id] = User(
                id=user_id,
                name=name,
                email=email,
                description=description
            )
            return True
        return False

    @rpc(Unicode, _returns=Boolean)
    def delete_user(ctx, user_id):
        return USERS.pop(user_id, None) is not None

    @rpc(_returns=Iterable(User))
    def list_users(ctx):
        return USERS.values()
