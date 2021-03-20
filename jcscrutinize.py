import argparse
import os
import sys

from scrutiny.device import Device, DeviceType
from scrutiny.javacard.toolwrappers.gppro import GPProInfo, GPProList
from scrutiny.javacard.toolwrappers.jcalgtest import JCAlgTestSupport,\
    JCAlgTestPerformance, JCAlgTestVariable
from scrutiny.utils import isdir, errmsg


def prepare_results(card_name):
    """
    Creates directory in results/
    :param card_name: card name
    :return: True on success
    """
    dirname = "results/" + card_name
    if isdir(dirname):
        print(dirname, "already exists, skipping the creation.")
        return True
    try:
        print("Creating", dirname + ".")
        os.mkdir(dirname)

        return True
    except FileExistsError as ex:
        return errmsg(dirname, "creating", ex)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("device_name",
                        help="the name of the device to be used")
    parser.add_argument("-a", "--atr",
                        help="check card's ART",
                        action="store_true")
    parser.add_argument("-i", "--info",
                        help="check card's basic information",
                        action="store_true")
    parser.add_argument("-l", "--list-applets", dest="list",
                        help="list card's installed applets",
                        action="store_true")
    parser.add_argument("-e", "--essentials",
                        help="perform essential checks: "
                        "ATR, basic information and list installed applets "
                        "(same as -acl)",
                        action="store_true")
    parser.add_argument("-s", "--support",
                        help="check supported JCAPI methods",
                        nargs="?", const=None, metavar="file_in")
    parser.add_argument("-p", "--performance",
                        help="test performance (SLOW)",
                        nargs="?", const=None, metavar="file_in")
    parser.add_argument("-v", "--variable-performance",
                        help="test variable data-langth performance "
                        "(VERY SLOW)",
                        nargs="?", const=None, metavar="file_in")
    parser.add_argument("-j", "--jcalgtest",
                        help="run JCAlgTest in interactive mode",
                        nargs="?", const=None, metavar="file_in")

    args = parser.parse_args()
    if args.essentials:
        args.atr = True
        args.info = True
        args.list = True

    device_name = args.device_name.replace(" ", "_")

    device = Device(device_name, DeviceType.JAVA_CARD)

    prepare_results(device_name)

    tool_wrappers = [GPProInfo(device_name),
                     GPProList(device_name),
                     JCAlgTestSupport(device_name, install=False),
                     JCAlgTestPerformance(device_name, install=False),
                     JCAlgTestVariable(device_name, install=False)]

    for tool in tool_wrappers:
        tool.run()
        device.add_modules(tool.parse())

    with open("results/" + device_name + ".json", "w") as output:
        output.write(str(device))

    sys.exit(0)
