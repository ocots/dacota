from sys import platform


def configuration(parent_package="", top_path=None):
    from numpy.distutils.misc_util import Configuration

    config = Configuration("smith/ternary", parent_package, top_path)

    # -------------
    # Ternary
    #

    # config azeotrope
    directory = "./resources/azeotrope/"
    source_files = []
    source_files.append(
        [
            directory + "models_d.f90",
            directory + "mod_F3d.pyf",
            directory + "F3_d.f90",
            directory + "func.f90",
        ]
    )

    config.add_extension(
        name="mod_F3",  # name of pyf file or module in pyf file
        sources=source_files,
    )

    # config univol.extremities
    directory = "./resources/univol/extremities/"
    source_files = []
    source_files.append(
        [
            directory + "models_d.f90",
            directory + "extrem.pyf",
            directory + "extremities_d.f90",
            directory + "func.f90",
        ]
    )

    config.add_extension(
        name="extrem",  # name of pyf file or module in pyf file
        sources=source_files,
    )

    # config univol.curve
    directory = "./resources/univol/curve/"
    source_files = []
    source_files.append(
        [
            directory + "models_d.f90",
            directory + "curve_interface.pyf",
            directory + "curve_d.f90",
            directory + "func.f90",
        ]
    )

    config.add_extension(
        name="curve_interface",  # name of pyf file or module in pyf file
        sources=source_files,
    )

    return config


if __name__ == "__main__":
    from numpy.distutils.core import setup

    setup(configuration=configuration)
