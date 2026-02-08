from django.core.management import call_command
from django.core.management.commands import shell

class Command(shell.Command):
    help = 'Override the default shell command to use IPython if available'
    
    def handle(self, *args, **options):
        call_command('shell_plus',*args,**options)