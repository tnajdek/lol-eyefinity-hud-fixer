#!/usr/bin/env python

class Vec2():
	def __init__(self, x, y):
		self.x = x or 0.0
		self.y = y or 0.0

class Rect():
	def __init__(self, start, end):
		self.start = start
		self.end = end

def get_lol_scaled_rect(rect, res_w, res_h):
	
