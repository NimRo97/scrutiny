import argparse
import os
import subprocess

from jcpeg.card import Card
from jcpeg.gppro import GPPro
from jcpeg.jcalgtest import JCAlgTest
from jcpeg.utils import isdir, errmsg

GP_PRO = "java -jar bin/gp.jar"

JCALGTEST = "java -jar bin/AlgTestJClient.jar"

CAPS = "cap/"
ALGTEST_305 = "AlgTest_v1.8.0_jc305.cap"
ALGTEST_304 = "AlgTest_v1.8.0_jc304.cap"
ALGTEST_222 = "AlgTest_v1.8.0_jc222.cap"

def prepare_results(card_name):
    dirname = "results/" + card_name
    if isdir(dirname):
       print(dirname, "already exists, skipping the creation.")
       return True
    try:
        print("Creating", dirname + ".")
        os.mkdir(dirname)
        return True
    except Exception as e:
        return errmsg(dirname, "creating", e)

def install_jcalgtest():
    for applet in [ALGTEST_305, ALGTEST_304, ALGTEST_222]:
        cmd_line = GP_PRO + " -install " + CAPS + applet
        process = subprocess.Popen(cmd_line, shell=True)
        out = process.communicate()[0]
        if process.returncode == 0:
            break

def run_jcalgtest(card_name):
    
    install_jcalgtest()
    
    cmd_line = JCALGTEST
    process = subprocess.Popen(cmd_line, shell=True)
    out = process.communicate()[0]
    rc = process.returncode
    

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("card_name",
                        help="the name of the card to be used")
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

    card_name = args.card_name.replace(" ", "_")
    
    prepare_results(card_name)
    
    gppro = GPPro(card_name)
    jcalgtest = JCAlgTest(card_name)

    card = Card(card_name)

    #if args.info:
    #    gppro.run_info()

    gppro.run()
    card.add_modules(gppro.parse())

    jcalgtest.run_support()

    #print(card)
    
    exit(0)
