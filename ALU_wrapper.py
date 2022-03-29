#!/usr/bin/env python3

# TODO: functions for copy finished data to web folder
# TODO: Send information to slims
# TODO: What to do with original folders?

import os
import glob
import logging
import argparse
import subprocess
from CGG.tools import emailer

parser = argparse.ArgumentParser(description='Wrapper to find non-processed folders, run ALU_parser on them.')
parser.add_argument("-p", "--path", help="Path to folder with sequence-subfolders.", action="store", default=".")
# TODO: Get default from config-file
parser.add_argument("-m", "--mailto", help="Mail address to message if files are changed.",
                    action="store", default="")  # TODO: get default or leave empty for no mail?
parser.add_argument("-r", "--run", help="Run for real. If not specified, just dry-run without any changes.",
                    action="store_true")
parser.add_argument("--loglevel", choices=['info', 'warning', 'error', 'debug'],
                    default="warning", help='Level of logging')
args = parser.parse_args()
logging.basicConfig(level=args.loglevel.upper())
seqpath = args.path
msg_to = args.mailto
finished = False


def vcfparse(updated_file, v):
    # TODO: Rev this part / rewrite
    new_vcf = open(updated_file, 'w')
    with open(v, "r") as vcf:
        info_list = []
        for line in vcf:
            if ("ALU" in line or "LINE1" in line) and not line.startswith('#'):
                info = line.split(';')
                matching = [s for s in info if "SVLEN" in s]
                match = str(matching).split('=')
                length = match[1]
                pos = (line.split('\t'))[1]
                end = int(pos) + int(length.strip("']"))
                info.insert(1, f"END={end}")
                info_list.append(';'.join(info))
            else:
                info_list.append(line)
    new_vcf.write(''.join(str(e) for e in info_list))
    new_vcf.close()


def alurunner():
    vcf_list = glob.glob(path + '/*SV*.vcf*')
    print(vcf_list)
    for v in vcf_list:
        updated_file = path + '/' + os.path.splitext(os.path.basename(v))[0] + '_melt_updated' + '.vcf'
        print(v)
        vcfparse(updated_file, v)


def sendtoslims():
    # TODO: Connect, send, what to send?
    pass


def compressfiles(folderpath):
    destination = seqpath + "/saved/"  # This needs changing. Now set to sub-folder saved under input-path (seqpath).
    filename = folderpath.split('/').pop() + ".tar.gz"
    subprocess.call(['tar', 'zcf', destination + filename, folderpath])


def mailout():
    msg_from = "crc@gu.se"  # TODO: Get from config-file
    msg_subject = "The crc files are done!"
    msg_body = "Hi!\nThe CLC-files are processed and ready for download."  # TODO: Change to a better mail
    emailer.send_email(msg_to, msg_from, msg_subject, msg_body)


folderList = next(os.walk(seqpath + '/.'))[1]
for folder in folderList:
    logging.info("Folder: " + folder)
    if "DNA" in folder and "_" not in folder:
        # Skipping folders with _ in the names. This is not actually needed.
        path = seqpath + '/' + folder
        if glob.glob(path + '/*melt*.vcf*'):  # TODO: Get regex from config-file
            logging.debug("Processed files found in folder " + folder + ", not running again.")
        else:
            logging.debug("No processed files found in folder " + folder + ", continuing.")
            if args.run:
                logging.debug("running on folder: " + folder + "; path: " + path)
                alurunner()
                sendtoslims()
                compressfiles(path)
                finished = True
            else:
                logging.debug("Not running on folder " + path + ", use -r to actually run")

if finished:
    mailout()
