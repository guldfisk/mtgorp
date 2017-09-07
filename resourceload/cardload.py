from orp.persist import PicklePersistor
from resourceload.locate import Locator
from orp.relationships import ManyToMany
import os

class O(object):
	def __init__(self, v, vv):
		self.value = v
		self.wauw = vv

class User(object):
	def __init__(self):
		self.roles = ManyToMany(self, 'users')
		# self.roles = O(1, 2)

class Role(object):
	def __init__(self):
		self.users = ManyToMany(self, 'roles')

user_1 = User()
user_2 = User()

role_1 = Role()
role_2 = Role()

users = (user_1, user_2)
roles = (role_1, role_2)

user_1.roles.add(role_1)
user_1.roles.add(role_2)

users_roles = (users, roles)

persistor = PicklePersistor(os.path.join(Locator.path, 'test.ord'))

persistor.save(users_roles)

users, roles = persistor.load()

user_1, user_2 = users
role_1, role_2 = roles

print(user_1.roles, role_1.users)

# print(users[0].roles, roles[0].users)