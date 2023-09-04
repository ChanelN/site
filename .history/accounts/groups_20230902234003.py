from django.contrib.auth.models import Group, Permission

# Create a new group
group = Group.objects.create(name='Superusers')

# Add permissions to the group
permissions = Permission.objects.filter(codename__in=[
    'can_add_customuser',
    'can_change_customuser',
    'can_delete_customuser',
    'can_change_permission',
    'can_add_bid',
    'can_delete_bid',
    'can_change_bid',
    'can_add_item',
    'can_change_item',
    'can_delete_item',
])
group.permissions.set(permissions)