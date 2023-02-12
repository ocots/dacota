from .errors import *


class Options:
    """
    This class is the generic class to define solvers options.
    """

    def __init__(self, *args, **kwargs):
        """

        Doc de __init__

        """
        # On donne les valeurs par defaut de options
        self.options = dict()

        self.name = ""

        # args   -- tuple of anonymous arguments
        # kwargs -- dictionary of named arguments
        self.update(*args, **kwargs)

    def update(self, *args, **kwargs):
        """

        Doc de update

        """
        for dico in args:
            if isinstance(dico, dict):
                self.__private_update(dico)
            else:
                raise ArgumentTypeError(
                    "Options requires arguments of type dict or a \
                        list of param=value."
                )

        self.__private_update(kwargs)

    def __private_update(self, dictionary):
        """

        Doc de __private_update

        """
        for key, val in dictionary.items():
            if key in self.options:
                if isinstance(self.options[key], val.__class__):
                    self.options[key] = val
                else:
                    raise ArgumentTypeError(
                        self.name
                        + " option "
                        + key
                        + " must be of type: "
                        + str(self.options[key].__class__)
                        + " instead of type: "
                        + str(val.__class__)
                        + "!"
                    )
            else:
                raise OptionNameError(
                    key + " is not a valid " + self.name + " option.\n"
                )

    def get(self, key):
        """

        Doc de get

        """
        try:
            value = self.options[key]
        except KeyError as err:
            raise OptionNameError(
                key + " is not a " + self.name + " option.\n"
            )

        return value

    def __str__(self):
        """

        Doc de __str__

        """
        keys = sorted(self.options.keys())
        string = self.__class__.__name__ + ":\n\n"
        for key in keys:
            string = (
                string
                + "\t"
                + key.ljust(20)
                + " = "
                + str(self.options[key])
                + "\n"
            )

        return string
