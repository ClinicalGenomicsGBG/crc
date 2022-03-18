#!/apps/bio/software/anaconda2/envs/hcp/bin/python3

# Please note, this is an early version. All the verbose-stuff will be reduced at later stages.
# TODO: functions for copy finished data to web folder
# TODO: Information to slims?
# TODO: What to do with original folders?

import os
import glob
import smtplib
import argparse
import subprocess
from email.message import EmailMessage

mail_to = ""  # Change this, and uncomment argument before EOF
pythonpath = "/apps/bio/software/anaconda2/envs/hcp/bin/python3"  # since server (as for now) has python2 installed

parser = argparse.ArgumentParser(description='Wrapper to find non-processed folders, run ALU_parser on them.')
parser.add_argument("-p", "--path", help="Path to folder with sequence-subfolders.", action="store", default=".")
# /seqstore/remote/share/crc
parser.add_argument("-r", "--run", help="Run for real. If not specified, just dry-run without any changes.",
                    action="store_true")
parser.add_argument("-v", "--verbose", help="Show more information while running.", action="store_true")
args = parser.parse_args()
sendmail = False
seqpath = args.path


def email_general(msg_to, msg_from, subject, body, attachment=None):
    msg = EmailMessage()
    msg.set_content(f'{body}\n'
                    f'\n'
                    f'Kind regards,\n'
                    f'Clinical Genomics Gothenburg')
    msg['Subject'] = f'{subject}'
    msg['From'] = msg_from
    msg['To'] = msg_to
    # msg['Cc'] = "clinicalgenomics@gu.se"
    if attachment:  # Add attachment if provided
        csv_filename = os.path.basename(attachment)
        with open(attachment, 'rb') as f:
            data = f.read()
            msg.add_attachment(data, maintype='text', subtype='plain', filename=csv_filename)
    s = smtplib.SMTP('smtp.gu.se')
    s.send_message(msg)
    s.quit()


def vcfparse(updated_file, v):
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
    destination = seqpath + "/saved/"
    filename = folderpath.split('/').pop() + ".tgz"
    print("zip path: tar zcf " + destination + filename + " " + folderpath)
    subprocess.call(['tar', 'zcf', destination + filename, folderpath])


if not args.run:
    print("Not parsing any found files, specify -r to actually run")
folderList = next(os.walk(seqpath + '/.'))[1]
if args.verbose:
    print("List of folders in dir: ")
    for folder in folderList:
        print(folder)
    print("--- END OF LIST ---")

for folder in folderList:
    if "DNA" in folder and "_" not in folder:
        # Skipping folders with _ in the names... this is actually not needed.
        path = seqpath + '/' + folder
        if glob.glob(path + '/*melt*.vcf*'):  # depending on how we want to run this. just an example.
            if args.verbose:
                print("Processed files found in folder " + folder + ", not running again.")
        else:
            if args.verbose:
                print("No processed files found in folder " + folder + ", continuing.")
            if args.run:
                if args.verbose:
                    print("running on folder: " + path)
                print("Folder: " + folder + " Path: " + path)
                alurunner()
                sendtoslims()
                compressfiles(path)
                sendmail = True
            else:
                if args.verbose:
                    print("Not running on folder " + path + ", use -r to actually run")

if sendmail:
    mail_from = ""
    mail_subject = "the crc files are done"
    mail_body = "Hi!\nThe CLC-files are processed and ready for download."  # Change to a better mail
    #  email_general(msg_to, msg_from, subject, body) # Uncomment to actually send mail.
    if args.verbose:
        print("mailto: " + mail_to + "; mail from: " + mail_from +
              "; subject: " + mail_subject + ";\n--- mail body ---\n" + mail_body)
