class Enumeration(object):
    """
    A small helper class for more readable enumerations,
    and compatible with Django's choice convention.
    You may just pass the instance of this class as the choices
    argument of model/form fields.

    Example:
        MY_ENUM = Enumeration([
            (100, 'MY_NAME', 'My verbose name'),
            (200, 'MY_AGE', 'My verbose age'),
        ])
        assert MY_ENUM.MY_AGE == 100
        assert MY_ENUM[1] == (200, 'My verbose age')
        assert MY_ENUM.verbose(100) == 'My verbose name'
    """

    def __init__(self, enum_list):
        self.enum_list = [(item[0], item[2]) for item in enum_list]
        self.enum_dict = {item[1]: item[0] for item in enum_list}
        self.verbose_dict = {item[2]: item[0] for item in enum_list}

    def __contains__(self, v):
        return (v in self.enum_list)

    def __len__(self):
        return len(self.enum_list)

    def __getitem__(self, v):
        if isinstance(v, str):
            return self.enum_dict[v]
        elif isinstance(v, int):
            return self.enum_list[v]

    def __getattr__(self, name):
        return self.enum_dict[name]

    def __getdesp__(self, key):
        for item in self.enum_list:
            if item[0] == key:
                return item[1]

    def __iter__(self):
        return self.enum_list.__iter__()

    def get_key_from_desc(self, desc):
        for item in self.enum_list:
            if item[1] == desc:
                return item[0]

    def get_key_from_dict(self, v):
        for key, value in self.enum_dict.items():
            if value == v:
                return key

    def values(self):
        return self.enum_dict.values()

    def keys(self):
        return self.enum_dict.keys()

    def verbose(self, value):
        value_to_verbose_dict = dict(self.enum_list)
        assert (len(value_to_verbose_dict) == len(self.enum_list))
        return value_to_verbose_dict.get(value, '')

    def get_array_pair(self):
        return [{'key': key, 'value': value, 'verbose': self.verbose(value)} for key, value in self.enum_dict.items()]
