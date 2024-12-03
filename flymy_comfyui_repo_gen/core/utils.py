import re


def normalize_u(string):
    replace_chars = {" ": "_", "-": "_"}
    avail_regex = re.compile(rf"[\w+{''.join(set(replace_chars.values()))}]+")
    for k, v in replace_chars.items():
        string = string.replace(k, v)
    if not avail_regex.fullmatch(string):
        raise ValueError(
            f"Repository name does not satisfy regex {avail_regex=}, "
            "to clarify reason - use https://regex101.com"
        )
    return string


def replace_symbols_with_underscore(text):
    # Regex pattern: match any character that is not a letter or digit
    pattern = r"[^a-zA-Z0-9]"
    # Replace all matched characters with an underscore
    result = re.sub(pattern, "_", text)
    return result


def to_pascal_case(string: str) -> str:
    components = string.split("_")
    return "".join(x.title() for x in components)


def to_snake_case(string: str) -> str:
    string = re.sub(r"\s+", " ", string.strip())
    string = re.sub(r"(?<=[a-zA-Z0-9])([A-Z])", r"_\1", string)
    string = re.sub(r"[^a-zA-Z0-9_]", "_", string)
    return string.lower()
