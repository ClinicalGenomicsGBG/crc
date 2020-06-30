# README #

Colorectal cancer related scripts

## Usage

`ALU_parser.py -vdir [DIRECTORY_WITH_VCFFILES]` 

Will change files with *_SV* in filename.

### Example:  

**input:** 2020-1544_SV.vcf  

**output:** 2020-1544_SV_melt_updated.vcf  


Takes a list with files, open one file at a time and alters info field if "Alu" is found and add END position

ALU_parser_wolist.py
Takes one file instead of list of files
