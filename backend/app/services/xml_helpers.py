def string_prop(name, value):

    return (
        f'<stringProp name="{name}">'
        f'{value}'
        f'</stringProp>'
    )


def bool_prop(name, value):

    value = str(value).lower()

    return (
        f'<boolProp name="{name}">'
        f'{value}'
        f'</boolProp>'
    )


def int_prop(name, value):

    return (
        f'<intProp name="{name}">'
        f'{value}'
        f'</intProp>'
    )


def open_tag(tag, attrs=None):

    if not attrs:
        return f"<{tag}>"

    attr_string = " ".join(
        [f'{k}="{v}"' for k, v in attrs.items()]
    )

    return f"<{tag} {attr_string}>"


def close_tag(tag):

    return f"</{tag}>"