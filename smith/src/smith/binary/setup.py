from sys import platform


def configuration(parent_package="", top_path=None):
    from numpy.distutils.misc_util import Configuration

    config = Configuration("smith/binary", parent_package, top_path)

    # -------------
    # Binary
    #

    # config azeotrope
    directory = "./resources/azeotrope/"  # from smith
    source_files = []
    source_files.append(
        [
            directory + "models_d.f90",
            directory + "mod_F2.pyf",
            directory + "F2_d.f90",
            directory + "func.f90",
        ]
    )

    config.add_extension(
        name="mod_F2", sources=source_files  # name of module in pyf file
    )

    return config


if __name__ == "__main__":
    from numpy.distutils.core import setup

    setup(configuration=configuration)
