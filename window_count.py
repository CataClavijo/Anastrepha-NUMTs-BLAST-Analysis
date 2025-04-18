#!/usr/bin/env python

"""
Process chromosome file and annot file from chromoMap to create a new annot file using windows
"""

import argparse,os,sys
import csv

class MyParser(argparse.ArgumentParser):
        def error(self, message):
                sys.stderr.write('error: %s\n' % message)
                self.print_help()
                sys.exit(2)

parser=MyParser()
#parser = argparse.ArgumentParser()
parser.add_argument('--chromosome_file', help='Path to the input chromosome file. See chromoMap manual for details.')
parser.add_argument('--annot_file', help='Path to the input annotation file. See chromoMap manual for details.')
parser.add_argument('--output_annot_file', help='Path to the output.')
parser.add_argument('--window_size', help='Size of the windows to count the markers.')

if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)

args = parser.parse_args()

if args.chromosome_file:
        chromosome_file = args.chromosome_file

if args.annot_file:
        annot_file = args.annot_file

if args.output_annot_file:
        output_annot_file = args.output_annot_file

if args.window_size:
        window_size = int(args.window_size)


'''
FUNCTIONS
'''

def csv_to_list(file_path):
        with open(file_path, mode ='r')as file:
                csvFile = csv.reader(file,delimiter ='\t')
                final_list = list(csvFile)
        return final_list


'''
MAIN
'''

list_markers = csv_to_list(annot_file)
list_chrm = csv_to_list(chromosome_file)

#Create a dictionary of regions using chromosome info
dict_regions = {}
counter = 0
for chr in list_chrm:
        chrm_id = chr[0]
        chrm_end = int(chr[2])
        for region in range(1,chrm_end,window_size):
                counter = counter + 1
                if chrm_id in dict_regions.keys():
                        dict_regions[chrm_id].append([counter,region,region+500000,0])

                else:
                        dict_regions[chrm_id] = []
                        dict_regions[chrm_id].append([counter,region,region+500000,0])

#Count the number of markers per region
for info in list_markers:
        chr_ID = info[1]
        start = int(info[2])
        regions = dict_regions[chr_ID]
        for index in range(len(regions)):
                if  (start >= regions[index][1]) and (start < regions[index][2]):
                        number_markers = regions[index][3] + 1 
                        new_chrm_info = [regions[index][0],regions[index][1],regions[index][2],number_markers]
                        regions[index] = new_chrm_info
                        new_regions = regions[:]
                        dict_regions[chr_ID] = new_regions
                        break

#Convert dictionary of regions to a list and correct ranges
final_results_list = []
for chrm in dict_regions.keys():
        for region_info in dict_regions[chrm]:
                new_region_info = [str(region_info[0]),chrm,str(region_info[1]),str(region_info[2]-1),str(region_info[3])]
                final_results_list.append(new_region_info)

#Save the result into a csvfile
with open(output_annot_file, 'w') as f:    
        # using csv.writer method from CSV package
        write = csv.writer(f,delimiter ='\t')
        write.writerows(final_results_list)
