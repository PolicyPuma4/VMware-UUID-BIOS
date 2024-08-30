import os


def get_default_location():
    with open(
        os.path.join(os.environ["APPDATA"], r"VMware\preferences.ini"),
        "r",
    ) as file:
        for line in file.read().splitlines():
            if not line.startswith('prefvmx.defaultVMPath = "'):
                continue

            return line.removeprefix('prefvmx.defaultVMPath = "').removesuffix('"')
