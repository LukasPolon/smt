class Asserts:
    """ I don't like Python native assert keyword, so this class mimics
        asserts from unittest library.
    """

    def assertEqual(self, first, second, quiet=False):
        """ Checks if both given elements are identical."""

        if first != second:
            raise AssertionError(
                f"Elements \"{first if not quiet else '<hidden>'}\" "
                f"and \"{second if not quiet else '<hidden>'}\" are not equal."
            )

    def assertNotEqual(self, first, second, quiet=False):
        """ Checks if given elements are not identical. """

        if first == second:
            raise AssertionError(
                f"Elements \"{first if not quiet else '<hidden>'}\" "
                f"and \"{second if not quiet else '<hidden>'}\" are equal."
            )

    def assertTrue(self, item, quiet=False):
        """ Checks if given item is True."""
        if not item:
            raise AssertionError(
                f"Element: \"{item if not quiet else '<hidden>'}\" is not True."
            )

    def assertFalse(self, item, quiet=False):
        """ Checks if given item is False."""
        if item:
            raise AssertionError(
                f"Element: \"{item if not quiet else '<hidden>'}\" is not False."
            )

    def assertIn(self, item, structure, quiet=False):
        """ Checks if given item exists in a given structure."""
        if item not in structure:
            raise AssertionError(
                f"Element: {item if not quiet else '<hidden>'} does not exist "
                f"in structure: {structure if not quiet else '<hidden>'}."
            )

    def assertNotIn(self, item, structure, quiet=False):
        """ Checks if given item does not exists in a given structure."""
        if item in structure:
            raise AssertionError(
                f"Element: {item if not quiet else '<hidden>'} exist "
                f"in structure: {structure if not quiet else '<hidden>'}."
            )
