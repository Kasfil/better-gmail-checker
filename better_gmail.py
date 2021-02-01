"""better_gmail.py

Better gmail module

Handle integration to qtile bar through widget
"""
from pathlib import Path
from libqtile.widget import base #pylint: disable=E0401
from .auth import BetterGmailChecker #pylint: disable=E0402

class BetterGmail(base.ThreadPoolText):
    """Better gmail qtile bar widget"""
    orientations = base.ORIENTATION_HORIZONTAL
    defaults = [
        ('label_id', 'INBOX', 'Gmail Label ID to check'),
        ('display_format', '﫮 {MessageUnread}/{MessageTotal}', 'Display format'),
        ('color_unread', 'ffffff', 'Color when there is unread message(s)'),
        ('color_no_unread', 'ffffff', 'Color when there is no unread message(s)'),
        ('update_interval', 10, 'Interval for each request')
    ]

    def __init__(self, **config) -> None:
        base.ThreadPoolText.__init__(self, '', **config)
        self.add_defaults(BetterGmail.defaults)
        self.first_attemp = True
        self.gmail_status = None

    def get_update(self):
        """main get gmail status"""
        unread_message = self.gmail_status.messages_unread()
        total_message = self.gmail_status.messages_total()

        self._set_color(unread_message)

        return self.display_format.format(**{
            'MessageUnread': unread_message,
            'MessageTotal': total_message
        })

    def _set_color(self, unread_message):
        if unread_message > 0:
            self.layout.colour = self.color_unread
        else:
            self.layout.colour = self.color_no_unread

    def poll(self):
        """Main function to interact with qtile bar through widget"""
        # check if credentials.json exists
        file_dir = Path(__file__).resolve().parent
        credential_file = Path(file_dir, 'credentials.json').resolve()
        if not credential_file.is_file() and self.first_attemp:
            # show temporary text while authenticate in next tick
            self.first_attemp = False
            return "Waiting for authentication"

        self.gmail_status = BetterGmailChecker(self.label_id)
        return self.get_update()
