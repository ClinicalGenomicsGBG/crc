#!/Users/vilmacanfjorden/miniconda3/bin/python

import os
import argparse
import csv

##############################################

parser = argparse.ArgumentParser(prog="vcf_to_fasta")
parser.add_argument("--vcf", \
                        required=True, \
                        help="vcf file")
args = parser.parse_args()
base = os.path.basename(args.vcf)
updated_file = os.path.splitext(base)[0]+'_updated'+'.vcf'
##############################################
def vcf():
    new_vcf = open(updated_file, 'w')
    with open(args.vcf, "r") as vcf:
        info_list = []
        for line in vcf:
            # ALU repeats and LINE repeats
#            if "ALU" in line and not line.startswith('#'):
#                info = line.split(';')
#                matching = [s for s in info if "MEINFO" in s]
#                match = str(matching).split(',')
#                end = match[2]
#                info.insert(1, f"END={end}")
#                info_list.append(';'.join(info))
            if "ALU" in line and not line.startswith('#'):
                info = line.split(';')
                matching = [s for s in info if "SVLEN" in s]
                match = str(matching).split('=')
                length = match[1]
                pos = (line.split('\t'))[1]
                end = int(pos) + int((length).strip("']"))
                info.insert(1, f"END={end}")
                info_list.append(';'.join(info))
            elif "LINE1" in line and not line.startswith('#'):
                info = line.split(';')
                matching = [s for s in info if "SVLEN" in s]
                match = str(matching).split('=')
                length = match[1]
                pos = (line.split('\t'))[1]
                end = int(pos) + int((length).strip("']"))
                info.insert(1, f"END={end}")
                info_list.append(';'.join(info))
            else:
                info_list.append(line)
    new_vcf.write(''.join(str(e) for e in info_list))
    new_vcf.close()
vcf()
