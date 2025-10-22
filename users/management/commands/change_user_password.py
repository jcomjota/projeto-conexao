from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from getpass import getpass
import sys

User = get_user_model()


class Command(BaseCommand):
    help = 'Altera a senha de um usuário'

    def add_arguments(self, parser):
        parser.add_argument(
            'email',
            type=str,
            help='Email do usuário'
        )
        parser.add_argument(
            '--password',
            type=str,
            help='Nova senha (se não fornecida, será solicitada)'
        )

    def handle(self, *args, **options):
        email = options['email']
        password = options.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise CommandError(f'Usuário com email "{email}" não encontrado.')

        if not password:
            password = getpass('Digite a nova senha: ')
            password_confirm = getpass('Confirme a nova senha: ')
            
            if password != password_confirm:
                raise CommandError('As senhas não coincidem.')

        if len(password) < 8:
            raise CommandError('A senha deve ter pelo menos 8 caracteres.')

        user.set_password(password)
        user.save()

        self.stdout.write(
            f'Senha alterada com sucesso para {user.get_full_name()} ({user.email})'
        ) 