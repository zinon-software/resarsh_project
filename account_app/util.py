
from django.contrib.auth.models import BaseUserManager


class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError('يجب أن يكون لدى المستخدمين عنوان بريد إلكتروني')
		if not username:
			raise ValueError('يجب أن يكون لدى المستخدمين اسم مستخدم')

		user = self.model(
			email=self.normalize_email(email),
			username=username,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user




