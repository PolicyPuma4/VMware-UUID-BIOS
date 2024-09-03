import os
import re


def get_virtual_machines():
    machines = []
    with open(os.path.join(os.environ["APPDATA"], "VMware", "inventory.vmls")) as file:
        for line in file.read().splitlines():
            matches = re.findall(r"^index[0-9]*.id\ =\ \"(.*)\"$", line)
            if len(matches) == 0:
                continue

            machines.append(matches[0])

    return machines
