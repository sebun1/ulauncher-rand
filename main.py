import logging, random, base64
from os import urandom
log = logging.getLogger(__name__)

from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.item.ExtensionSmallResultItem import ExtensionSmallResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.ActionList import ActionList


class PlugRand(Extension):

    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class KeywordQueryEventListener(EventListener):
    function_titles = [
            'Random Number',
            'Random Integer',
            'Coin Flip',
            'Dice Roll',
            'Random Bytes'
            ]
    function_descriptions = [
            '(num) Generate a random number (0 - 1)',
            '(int) Generate a random integer (0 - 99)',
            '(coin) Flip a coin (Heads or Tails)',
            '(dice) Roll a die (1 - 6)',
            '(byte) Generate random bytes (default 32)'
            ]
    function_id = [
            'num',
            'int',
            'coin',
            'dice',
            'byte'
            ]

    def on_event(self, event, extension):
        arg = event.get_argument()
        if arg:
            cmd, _, args = arg.strip().partition(' ')
        else:
            cmd = ''
            args = ''
        cmd = cmd.lower()
        items = []

        if cmd == 'num' or cmd == 'number' or cmd.startswith('n'):
            log.info('Random Number')
            items.append(ExtensionResultItem(icon='images/icon.png',
                                             name=self.function_titles[0],
                                             description=RandFunctions().cmd_desc('num', args),
                                             on_enter=ExtensionCustomAction(('num', args), keep_app_open=True)))
        if cmd == 'int' or cmd.startswith('i'):
            log.info('Random Number')
            items.append(ExtensionResultItem(icon='images/icon.png',
                                             name=self.function_titles[1],
                                             description=RandFunctions().cmd_desc('int', args),
                                             on_enter=ExtensionCustomAction(('int', args), keep_app_open=True)))
        elif cmd == 'coin' or cmd.startswith('c'):
            log.info('Coin Flip')
            items.append(ExtensionResultItem(icon='images/icon.png',
                                             name=self.function_titles[2],
                                             description=RandFunctions().cmd_desc('coin', args),
                                             on_enter=ExtensionCustomAction(('coin', args), keep_app_open=True)))
        elif cmd == 'dice' or cmd == 'die' or cmd.startswith('d'):
            log.info('Dice Roll')
            items.append(ExtensionResultItem(icon='images/icon.png',
                                             name=self.function_titles[3],
                                             description=RandFunctions().cmd_desc('dice', args),
                                             on_enter=ExtensionCustomAction(('dice', args), keep_app_open=True)))
        elif cmd == 'byte' or cmd == 'bytes' or cmd.startswith('b'):
            log.info('Random Bytes')
            items.append(ExtensionResultItem(icon='images/icon.png',
                                             name=self.function_titles[4],
                                             description=RandFunctions().cmd_desc('byte', args),
                                             on_enter=ExtensionCustomAction(('byte', args), keep_app_open=True)))
        elif cmd == 'all' or cmd.startswith('a'):
            log.info('All functions')
            for cmd_, title, desc in zip(self.function_id, self.function_titles, self.function_descriptions):
                res = RandFunctions().by_cmd(cmd_)
                items.append(ExtensionResultItem(icon='images/icon.png',
                                                 name=res,
                                                 description=title,
                                                 on_enter=CopyToClipboardAction(res)))
        elif cmd == '':
            log.info('No command, show options')
            for cmd_, title, desc in zip(self.function_id, self.function_titles, self.function_descriptions):
                items.append(ExtensionResultItem(icon='images/icon.png',
                                                 name=title,
                                                 description=desc,
                                                 on_enter=ExtensionCustomAction((cmd_, None))))
        else:
            pass
        # log.info(f'Invalid Command with \"{cmd}\"')
            # items.append(ExtensionSmallResultItem(icon='images/icon.png',
                                                    #                                       name='Invalid Command',
                                                    #                                       on_enter=HideWindowAction()))

        return RenderResultListAction(items)

class ItemEnterEventListener(EventListener):

    def on_event(self, event, extension):
        cmd, args = event.get_data()
        res = RandFunctions().by_cmd(cmd, args)
        items = []
        items.append(ExtensionResultItem(icon='images/icon.png',
                                         name=res,
                                         description='Enter to Copy and Regenerate',
                                         on_enter=ActionList((
                                             CopyToClipboardAction(res),
                                             ExtensionCustomAction((cmd, args), keep_app_open=True)
                                             ))))
        return RenderResultListAction(items)

class RandFunctions:
    def __init__(self):
        pass

    def cmd_desc(self, cmd, args=None):
        if cmd == 'num':
            if args:
                try:
                    start, _, end = args.partition(' ')
                    end = '?' if end == '' else end
                    return 'Generate a random number ({} - {})'.format(start, end)
                except ValueError:
                    pass
            return 'Generate a random number (0 - 1)'
        if cmd == 'int':
            if args:
                try:
                    start, _, end = args.partition(' ')
                    end = '?' if end == '' else end
                    return 'Generate a random integer ({} - {})'.format(start, end)
                except ValueError:
                    pass
            return 'Generate a random integer (0 - 99)'
        elif cmd == 'coin':
            return 'Flip a coin (Heads or Tails)'
        elif cmd == 'dice':
            return 'Roll a dice (1 - 6)'
        elif cmd == 'byte':
            if args:
                try:
                    n, _, ub64 = args.partition(' ')
                    n = int(n)
                    return 'Generate random bytes ({} bytes)'.format(n)
                except ValueError:
                    pass
            return 'Generate random bytes (default 32)'

    def by_cmd(self, cmd, args=None):
        if cmd == 'num':
            if args:
                try:
                    start, _, end = args.partition(' ')
                    return self.random_number(float(start), float(end))
                except ValueError:
                    log.warning('Invalid Arguments')
                    pass
            return self.random_number()
        if cmd == 'int':
            if args:
                try:
                    start, _, end = args.partition(' ')
                    return str(random.randint(int(start), int(end)))
                except ValueError:
                    log.warning('Invalid Arguments')
                    pass
            return str(random.randint(0, 100))
        elif cmd == 'coin':
            return self.coin_flip()
        elif cmd == 'dice':
            return self.dice_roll()
        elif cmd == 'byte':
            if args:
                try:
                    n, _, ub64 = args.partition(' ')
                    n = int(n)
                    return self.random_bytes(n, ub64=(True if ub64.lower() == 'true' or ub64.lower() == '1' else False))
                except ValueError:
                    log.warning('Invalid Arguments')
                    pass
            return self.random_bytes()
        else:
            return ''

    def random_number(self, start=0.0, end=1.0):
        return str(random.uniform(start, end))

    def coin_flip(self):
        return 'Heads' if random.random() > 0.5 else 'Tails'

    def dice_roll(self):
        return str(random.randint(1, 6))

    def random_bytes(self, n=32, ub64=False):
        return (base64.b64encode(urandom(64))).decode('utf-8') if ub64 else urandom(n).hex()

if __name__ == '__main__':
    PlugRand().run()
