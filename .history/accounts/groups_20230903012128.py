from django.contrib.auth.models import Group, Permission
from accounts.models import CustomUser

# Create a new group
superuser_group, created = Group.objects.get_or_create(name='Superusers')
user1 = CustomUser.objects.get(email='chanel@gmail.com')
superuser_group.user_set.add(user1)

# Add permissions to the group
all_permissions = Permission.objects.all()
for permission in all_permissions:
    superuser_group.permissions.add(permission)