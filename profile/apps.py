from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'profile'

    def ready(self):
        import profile.signals