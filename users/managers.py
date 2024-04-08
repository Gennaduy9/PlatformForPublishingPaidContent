from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username=None, email=None, phone_number=None, password=None, **extra_fields):
        """
        Создает и сохраняет пользователя с указанным адресом электронной почты и паролем.
        """
        if not username:
            if not email and not phone_number:
                raise ValueError('Указанный адрес электронной почты/номер телефона должен быть установлен.')

        if email:
            email = self.normalize_email(email)

            if not username:
                username = email

            user = self.model(
                email=email,
                username=username,
                **extra_fields
            )

        if phone_number:
            if not username:
                username = phone_number

            user = self.model(
                username=username,
                phone_number=phone_number
                             ** extra_fields
            )

        # проверяем является ли пользователь суперпользователем
        if extra_fields.get('is_superuser'):
            user = self.model(
                username=username,
                **extra_fields
            )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username=username, email=email, password=password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self._create_user(
            username=username,
            password=password,
            **extra_fields
        )
