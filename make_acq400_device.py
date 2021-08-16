#!/usr/bin/python


"""
A script that will create a new tree (must be a NEW tree) and
add a new acq400_device to the tree.

Example usage:
./make_acq400_device.py --model=tr --name=TRANSIENT1 acq2106_188

OR if the user wants to call the tree 'experiment1' and use an IP address
to communicate with the acq400 series device:

./make_acq400_device.py --model=tr --name=TRANSIENT1 --hostname=192.168.0.100 experiment1
"""


import MDSplus
import make_acqtree  # want to use path_check function.
import acq400_hapi
import argparse
import subprocess
import datetime
import os.path
import getpass

def get_args():
    parser = argparse.ArgumentParser(
        description="make_acqtree with MDSplus device support.")

    parser.add_argument('--model', default='tr', type=str,
                        help='One of: tr, st or mr (transient, streaming or multi-rate).')

    parser.add_argument('--devname', default='default', type=str,
                        help='Desired name of MDSplus device. This is what the device will be referred to as in MDSplus.')

    parser.add_argument('--hostname', default='default', type=str,
                        help='Hostname of acq400 device. If using DNS AND you want to use the hostname as the tree name '
                        'then leave this blank, else use IP address or other DNS hostname.')

    parser.add_argument('tree', nargs=1, help="tree name (UUT name)")
    return parser.parse_args()


def make_device(tname, args):

    # Hostname is how the device will be accessed over the network.
    # If the hostname argument is left as default then the tree argument
    # will be used instead. This will only work if the tree is named after the
    # acq400 device e.g. if the tree is called acq2106_xxx.

    hostname = tname if args.hostname == 'default' else args.hostname

    tree = MDSplus.Tree(tname, -1, "NEW")
    uut = acq400_hapi.Acq400(hostname)
    nchan = uut.nchan()
    # Checks whether we're creating a device for acq1001 or acq2106.
    carrier_type = uut.s0.MODEL[0:7]

    # e.g. acq2106_32_tr for 32 channel acq2106 in transient capture mode.
    model = "{}_{}_{}".format(carrier_type, args.model, nchan)
    print("pgm: call tree.addDevice({}, {})".format(args.devname, model))
    tree.addDevice(args.devname, model)
    tree.write()

    tree = MDSplus.Tree(tname, -1, "EDIT")

    # Change node name to tree name
    node = tree.getNode(args.devname).getNode("node")
    node.putData(str(hostname))

    # Create pulse 0.
    MDSplus.Tree.setCurrent(tname, 1)
    MDSplus.Tree(tname, -1).createPulse(1)
    tree.write()
    return None


def create_readme(tname):
    user = getpass.getuser()
    tree_dir = os.path.expanduser("~") + "/TREES/{}/README.txt".format(tname)

    readme_string = "README file for the creation of tree: {}\n".format(tname)
    readme_string += "Command line arguments:\n"
    readme_string += " ".join(sys.argv)
    readme_string += "\nThe script was run at date: {} by user: {}\n".format(datetime.datetime.now(), user)
    readme_string += subprocess.check_output(["git", "log"]).strip().split("\n")[0] + "\n"
    f = open(tree_dir, "a")
    f.write(readme_string)
    f.close()
    return None


def main():
    args = get_args()
    tname = args.tree[0]
    make_acqtree.path_check(tname)
    make_device(tname, args)
    create_readme(tname)
    print("Device created.")
    return None


if __name__ == '__main__':
    main()
