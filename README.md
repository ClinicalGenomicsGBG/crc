# README #

Colorectal cancer related scripts
The wrapper will check if existing files in the path submitted contain modified files,
and will modify according to original script if no modified files found (i.e. will not run
the same files twice). The script will then compress the modified content and send a mail
to signal that the files have been processed.

### TODO: ###
- Add some checks to send alert if something goes wrong
- Add input (or default) path to store compressed content
- Send data to slims

## Usage of wrapper (for future automation)

`ALU_wrapper.py -p [TARGET_DIRECTORY] -r`

Arguments for usage:
```
-p    Path to folder with sequence-subfolders
-r    Run for real. If not specified, just dry-run without any changes
-v    Show more information while running
```

## Usage of original script

`ALU_parser.py -vdir [DIRECTORY_WITH_VCFFILES]` 

Will change files with *_SV* in filename.

### Example:  

**input:** 2020-1544_SV.vcf  

**output:** 2020-1544_SV_melt_updated.vcf  


Takes a list with files, open one file at a time and alters info field if "Alu" is found and add END position

ALU_parser_wolist.py
Takes one file instead of list of files
