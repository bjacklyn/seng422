from django.db.models.signals import post_syncdb
from django.contrib.auth.models import User, Group
import surveys.models

def my_callback(sender, **kwargs):
	manager_group = Group.objects.get_or_create(name='Manager')[0]
	surveyor_group = Group.objects.get_or_create(name='Surveyor')[0]

	for user in User.objects.all():
		user.groups.add(manager_group)
		manager_group.user_set.add(user)

		
post_syncdb.connect(my_callback, sender=surveys.models)
