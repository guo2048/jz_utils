import inspect


_instances = {}


def singleton(cls):
    def get_instance(*args, **kwargs):
        init_signature = inspect.signature(cls.__init__)
        inputs = []
        defaults = {}
        for name, param in init_signature.parameters.items():
            if name == "self":
                continue
            if param.kind == param.POSITIONAL_OR_KEYWORD:
                inputs.append(name)
                defaults[name] = param.default
        defaults.update(kwargs)
        values = []
        for arg in args:
            values.append(arg)
        idx = len(values)
        while idx < len(inputs):
            values.append(defaults[inputs[idx]])
            idx += 1
        normalized_args = tuple(values)
        key = (cls, normalized_args)

        if key not in _instances:
            _instances[key] = cls(*args, **kwargs)
        return _instances[key]

    return get_instance


def clean_instances():
    global _instances
    _instances = {}
