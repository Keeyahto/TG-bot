__all__ = ['start_cmd',
           'help_cmd',
           'buy_course_cmd',
           'cancel_cmd',
           'test_cmd',
           'upload_course_cmd',
           'moderator_login_cmd',
           'admin_login_cmd',
           ]
_commands = {
    'start_cmd': 'start',
    'help_cmd': 'help',
    'buy_course_cmd': 'Купить курс',
    'cancel_cmd': 'cancel',
    'test_cmd': 'test',
    'upload_course_cmd': 'Загрузить курсы',
    'moderator_login_cmd': 'moderator',
    'admin_login_cmd': 'admin',
    'my_account': 'Мой аккаунт'
}


class Command(str):
    def __init__(self, cmd, scope='default'):
        self.cmd = cmd
        self.scope = scope

    def __repr__(self):
        return self.cmd

    def __str__(self):
        return self.cmd

    def get_command(self, lower=False, prefix=False):
        cmd = self.cmd
        if prefix:
            cmd = self.prefix_cmd(cmd)
        if lower:
            cmd = cmd.lower()
        return cmd

    def get_scope(self):
        return self.scope

    @staticmethod
    def prefix_cmd(cmd):
        return '/' + cmd


for var, cmd in _commands.items():
    exec(f'{var} = Command("{cmd}")')
