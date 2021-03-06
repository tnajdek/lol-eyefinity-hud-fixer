from __future__ import division
import re
import sys
import os
from glob import glob
from collections import OrderedDict


# Max value LOL will allow vertically from the anchor point
# e.g. if anchor point is 1,1 and Rect start is 0,0 then
# rect will be placed MAGIC_VALUE pixels from the right-most
# screen edge
MAGIC_VALUE = 1440

class Vec2(object):
	def __init__(self, x, y):
		self.x = x or 0.0
		self.y = y or 0.0

class Rect(object):
	def __init__(self, start, end):
		self.start = start
		self.end = end

class LolRect(Rect):
	def __init__(self, start, end, res_w, res_h):
		super(LolRect, self).__init__(start, end)
		self.res_w = res_w
		self.res_h = res_h

def get_abs_scaled_rect(rect):
	return Rect(
		Vec2(
			rect.start.x / rect.res_w,
			rect.start.y / rect.res_h
		),
		Vec2(
			rect.end.x / rect.res_w,
			rect.end.y / rect.res_h
		)
	)

def get_lol_scaled_rect(rect, res_w, res_h):
	return LolRect(
		Vec2(
			rect.start.x * res_w,
			rect.start.y * res_h
		),
		Vec2(
			rect.end.x * res_w,
			rect.end.y * res_h
		),
		res_w, res_h
	)

# rect must be abs scaled!
def reanchor_centrally(rect, anchor_src, target_resolution):
	RATIO = target_resolution / MAGIC_VALUE
	offset = (RATIO - 1)/2
	new_rect = Rect(
		Vec2(
			rect.start.x,
			rect.start.y
		),

		Vec2(
			rect.end.x,
			rect.end.y
		)
	)
	if(anchor_src.x == 1):
		new_rect.start.x = rect.start.x + offset
		new_rect.end.x = rect.end.x + offset
	elif(anchor_src.x == 0):
		new_rect.start.x = rect.start.x - offset
		new_rect.end.x = rect.end.x - offset
	elif(anchor_src.x != 0.5):
		raise NotImplementedError()

	return new_rect

def parse_fragment(fragment):
	parsed = OrderedDict() # somehow order seems to matter to LOL
	lines = fragment.split(os.linesep)
	for line in lines:
		line = line.strip(" \x00\r")
		if(line and line[0:2] != '//'):
			key, value = re.match("(\w+):\s*(.*)", line).groups()
			if(key == 'Rect'):
				rect_spec = re.match("\s*([\-\d\.]+),([\-\d\.]+)[\s\-]+([\-\d\.]+),([\-\d\.]+)[\s\/]+(\d+)x(\d+)", value).groups()
				value = LolRect(
					Vec2(*[float(x) for x in rect_spec[0:2]]),
					Vec2(*[float(x) for x in rect_spec[2:4]]),
					*[int(x) for x in rect_spec[4:6]]
				)
			elif(key == 'Anchor'):
				anchor_spec = re.match("\s*([\-\d\.]+)[\s,]*([\-\d\.]+)", value).groups()
				value = Vec2(*[float(x) for x in anchor_spec])
			parsed[key] = value
	return parsed

def parse_fragments(fragments):
	fragments_collection = list()
	split_fragments = re.split('/{5,}', fragments)
	for split_fragment in split_fragments:
		parsed_fragment = parse_fragment(split_fragment)
		fragments_collection.append(parsed_fragment)
	return fragments_collection

def compile_fragment(fragment_dict):
	fragment = ''
	for key,value in fragment_dict.iteritems():
		if(key == "Rect"):
			value = "%.2f,%.2f - %.2f,%.2f / %ix%i" % (
						value.start.x, value.start.y,
						value.end.x, value.end.y, 
						value.res_w, value.res_h
			)
		if(key == "Anchor"):
			value = "%.2f,%.2f" % (value.x, value.y)
		fragment = fragment + "%s: %s" % (key, value) + os.linesep
	return fragment

def compile_fragments(fragments, desired_length):
	total_fragments_length = 0;
	compiled_fragments = [compile_fragment(f) for f in fragments]

	for compiled_fragment in compiled_fragments:
		total_fragments_length = total_fragments_length + len(compiled_fragment)

	length_diff = desired_length - total_fragments_length
	separators_count = len(fragments)-1
	if(length_diff<separators_count*2):
		raise Exception("Unable to compensate")

	separator = "/" * (int(length_diff/separators_count)-len(os.linesep))
	separator = separator + os.linesep
	out = separator.join(compiled_fragments)

	missing_bytes = desired_length - len(out)

	out = out + ("/" * missing_bytes)
	
	assert len(out) == desired_length
	return out

def reanchor_centrally_in_raf(raf, target_resolution):
	desired_length = len(raf)
	fragments = parse_fragments(raf)
	for fragment in fragments:
		if('Rect' in fragment and 'Anchor' in fragment):
			try:
				abs_scaled = get_abs_scaled_rect(fragment['Rect'])
				reanchored = reanchor_centrally(abs_scaled, fragment['Anchor'], target_resolution)
				repositioned = get_lol_scaled_rect(reanchored, 1024, 768)
				fragment['Rect'] = repositioned
				fragment['Anchor'] = Vec2(0.5, fragment['Anchor'].y)
			except NotImplementedError:
				print("Found something anchored %f. Not supported - leaving untouched." % fragment['Anchor'].x)
	return compile_fragments(fragments, desired_length)

