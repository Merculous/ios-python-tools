class Template(object):
    def __init__(self, template: str):
        super().__init__()

        self.template = template

    def parse(self):
        data = self.template.split('{{keys')[1].split('}}')[0].splitlines()
        new_list = list(filter(None, data))  # Remove all ''
        info = list()
        for stuff in new_list:
            new_str = stuff.replace('|', '').replace('=', '').split()
            info.append({new_str[0]: new_str[1]})

        return info
