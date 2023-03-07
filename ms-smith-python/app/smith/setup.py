def configuration(parent_package="", top_path=None):
    from numpy.distutils.misc_util import Configuration

    config = Configuration("", parent_package, top_path)

    config.add_subpackage(subpackage_name="smith", subpackage_path="src/smith")
    config.add_subpackage(
        subpackage_name="smith/binary", subpackage_path="src/smith/binary"
    )
    config.add_subpackage(
        subpackage_name="smith/ternary", subpackage_path="src/smith/ternary"
    )

    return config


if __name__ == "__main__":
    from numpy.distutils.core import setup

    setup(configuration=configuration, requires=["numpy"])
