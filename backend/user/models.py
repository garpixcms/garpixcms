from garpix_user.models import GarpixUser


class User(GarpixUser):

    USERNAME_FIELDS = ('email', 'username')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
