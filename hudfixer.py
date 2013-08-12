#!/usr/bin/env python
from __future__ import division
import re

# Single screen resolution
TARGET_SCREEN_RESOLUTION = 1920

# Max value LOL will allow vertically from the anchor point
# e.g. if anchor point is 1,1 and Rect start is 0,0 then
# rect will be placed MAGIC_VALUE pixels from the right-most
# value
MAGIC_VALUE = 1440

RATIO = TARGET_SCREEN_RESOLUTION / MAGIC_VALUE

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

def get_abs_scaled_rect(rect, res_w, res_h):
	return Rect(
		Vec2(
			rect.start.x / res_w,
			rect.start.y / res_h
		),
		Vec2(
			rect.end.x / res_w,
			rect.end.y / res_h
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
def reanchor_centrally(rect, anchor_src):
	conversion_ratio = 1 + (RATIO - 1)/2

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
		new_rect.start.x = rect.start.x * conversion_ratio
		new_rect.end.x = rect.end.x * conversion_ratio
	elif(anchor_src.x != 0.5):
		raise NotImplementedError()

	return new_rect

def parse_fragment(fragment):
	parsed = dict()
	lines = fragment.split("\n")
	for line in lines:
		line = line.strip()
		if(line):
			key, value = re.match("(\w+):\s*(.*)", line).groups()
			if(key == 'Rect'):
				rect_spec = re.match("\s*([\d\.]+),([\d\.]+)[\s\-]+([\d\.]+),([\d\.]+)[\s\/]+(\d+)x(\d+)", value).groups()
				value = LolRect(
					Vec2(*[float(x) for x in rect_spec[0:2]]),
					Vec2(*[float(x) for x in rect_spec[2:4]]),
					*[int(x) for x in rect_spec[4:6]]
				)
			elif(key == 'Anchor'):
				anchor_spec = re.match("\s*([\d\.]+)[\s,]*([\d\.]+)", value).groups()
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
		fragment = fragment + "%s: %s\n" % (key, value)
	return fragment

def compile_fragments(fragments):
	separator = "//////////////////////////////////////////\n"
	fragments = [compile_fragment(f) for f in fragments]
	return separator.join(fragments)

def process(fragment):
	pass