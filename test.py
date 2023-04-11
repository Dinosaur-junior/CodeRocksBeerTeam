from database import Database

db = Database()
for i in db.roles_get_all():
    print(i)
db.users_update_info(200109375, 'role', 1)