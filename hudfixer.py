#!/usr/bin/env python
import os
import sys
import fnmatch
import argparse

from hud import reanchor_centrally_in_raf
from utils import mkdir_p, convert_lol_path

HUD_ELEMENTS_RAF_PATH = 'DATA/Menu/HUD/Elements'
SCRIPT_ROOT = os.path.dirname(os.path.realpath(__file__))

parser = argparse.ArgumentParser(description='Tool to modify offest values in raf files in order to make HUD appear on the center monitor on multi-monitor setups such as AMD Eyefinity or Nvidia Surround')
parser.add_argument('raf_root',
	metavar='raf_root',
	type=str,
	help='This is a root folder containing RAF files preserving original raf file paths'
)

parser.add_argument('-r',
	dest="single_screen_resolution",
	default=1920,
	help="Resolution of each screen in the setup"
)

parser.add_argument('-o',
	dest="out_path",
	default=None,
	help="Path where the modified file will be placed, preserving "
)

parser.add_argument('-i',
	dest="inline",
	action='store_true',
	default=False,
	help="If present, changes will be done inline overriding existing files."
)

args = parser.parse_args()


if(not os.path.isdir(args.raf_root)):
	print('"%s" is not a directory, please provide full path to extracted RAF files' % args.source_path)
	sys.exit()

hud_elements_path = os.path.join(args.raf_root, convert_lol_path(HUD_ELEMENTS_RAF_PATH))

if(not os.path.isdir(hud_elements_path)):
	print('Unable to find path "%s", please make sure that RAF files have been extracted correctly' % args.source_path)
	sys.exit()

if(args.inline and args.out_path):
	print("Please specify either inline conversion (-i) or output directory (-o) but not both.")
	sys.exit()

if(args.inline):
	print("Converted files will override source files in \"%s\" " % hud_elements_path)
else:
	if(not args.out_path):
		args.out_path = "extracted"
	print("Converted files will be stored in \"%s\"" % os.path.join(SCRIPT_ROOT, args.out_path))

for filename in os.listdir(hud_elements_path):
	filepath = os.path.join(hud_elements_path, filename)
	if os.path.isfile(filepath) and fnmatch.fnmatch(filename, '*.ini'):
		print "Processing %s" % filepath
		f = open(filepath, "rb")
		raf = f.read()
		f.close()
		output = reanchor_centrally_in_raf(raf, int(args.single_screen_resolution))
		if(args.inline):
			out_filepath = filepath
		else:
			out_filepath = os.path.join(SCRIPT_ROOT, args.out_path, filename)
		mkdir_p(os.path.dirname(out_filepath))
		f = open(out_filepath, "wb")
		print("Writing %s" % out_filepath)
		f.write(output)
		f.close()

print("Operation completed")


