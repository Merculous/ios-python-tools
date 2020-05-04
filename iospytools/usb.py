try:
    import usb.core
except ImportError as error:
    print('Oof, got error:', error)
    raise


class USB:
    def __init__(self):
        super().__init__()

        self.dev = usb.core.find()
