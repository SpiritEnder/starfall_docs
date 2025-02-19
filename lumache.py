"""
Lumache - Python library for cooks and food lovers.

This is a Python docstring, we can use Markdown syntax here because
our API documentation library understands it (mkdocstrings).

    # Import lumache
    import lumache

    # Call its only function
    get_random_ingredients(kind=["cheeses"])

"""

__version__ = "0.1.0"


class aa(Exception):
    """Raised if the kind is invalid."""

    pass


def get_random_ingredients(asd="po",kind=None):
    """
    Return a list of random ingredients as strings.

    :param kind: Optional "kind" of ingredients.
    :param asd: test蔼四大
    :type kind: list[str] or None
    :type asd: 一般 or 很好
    :raise lumache.InvalidKindError: If the kind is invalid.
    :return: The ingredients list.
    :rtype: list[str]
    """
    return ["shells", "gorgonzola", "parsley"]
