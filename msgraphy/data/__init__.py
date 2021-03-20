import re
from dataclasses import dataclass
import typing

pattern = re.compile(r'(?<!^)(?=[A-Z])')


def __camel_to_snake__(name):
    return pattern.sub('_', name).lower()


def graphdataclass(cls, *args, **kwargs):
    new_cls = dataclass(cls, *args, **kwargs)

    old_init = new_cls.__init__

    def new_init(self, *args, **kwargs):
        missing = dict()
        if len(args) > 0 and isinstance(args[0], dict):
            data_dict = args[0]
            args = args[1:]

            self.__API_DATA__ = data_dict
            self.__at__ = dict()
            fields = new_cls.__dataclass_fields__

            for key in set(data_dict.keys()):
                if key.startswith("@"):
                    self.__at__[key] = data_dict.pop(key)

            for key, value in data_dict.items():
                prop_name = __camel_to_snake__(key)
                if prop_name in fields:
                    field_type = fields[prop_name].type
                    generic_origin = typing.get_origin(field_type)
                    generic_types = typing.get_args(field_type)
                    if hasattr(field_type, '__dataclass_fields__'):
                        kwargs[prop_name] = field_type(value)
                    elif generic_origin == list and len(generic_types) > 0:
                        generic_type = generic_types[0]
                        kwargs[prop_name] = [generic_type(i) for i in value]
                    else:
                        kwargs[prop_name] = value
                else:
                    missing[key] = (prop_name, value)

        self.api_missing_fields = missing
        self.api_missing_props = [x[0] for x in missing.values()]

        old_init(self, *args, **kwargs)

    new_cls.__init__ = new_init

    return new_cls
