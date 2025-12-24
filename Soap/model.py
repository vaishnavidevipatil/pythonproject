from spyne import Unicode
from spyne.model.complex import ComplexModel, Array

# User model
class User(ComplexModel):
    id = Unicode
    name = Unicode
    email = Unicode
    description = Unicode

# Response Message
class ResponseData(ComplexModel):
    user = User
    users = Array(User)
    success = Unicode
    message = Unicode