from parse import Course, parse_file
from flask import *

def safe_md_to_html(object):
	"""Returns parsed markdown of object if it is a string, otherwise returns object"""
	if type(object) is str:
		# Conditional is for compatability with current template system
		# Soon to be removed
		if len(object.split("\n")) > 1:
			return block_md_to_html(inline_md_to_html(object))
		else:
			return inline_md_to_html(object)
	else:
		return object

def inline_md_to_html(md_str):
	"""Translates inline markdown formatting to html"""
	translations = {
		"_"   : "i",
		"*"  : "b",
		"~"  : "del"
	}
	html_str = ""
	open_md_tags = []
	for char in md_str:
		if char in translations.keys():
			tag = translations[char]
			if char in open_md_tags:
				open_md_tags.remove(char)
				html_str += "</" + tag + ">"
			else:
				open_md_tags.append(char)
				html_str += "<" + tag + ">"
		else:
			html_str += char
	return html_str

def block_md_to_html(md_str):
	"""Translates block-level markdown formatting to html"""
	html_str = ""
	# Remove unneccessary whitespace
	if md_str[0] == "\n":
		md_str = md_str[1:]
	if md_str[-1] == "\n":
		md_str = md_str[:-1]
	# line-by-line parsing
	for i, line in enumerate(md_str.split("\n")):
		if line.startswith("---"):
			html_str += "<hr>"
		elif line.startswith("#"):
			heading_level = 0
			for i, char in enumerate(line):
				if char == "#":
					heading_level += 1
				else:
					break
			body = line[i:]
			tagname = "h" + str(heading_level)
			html_str += "<{tagname}>{body}</{tagname}>".format(tagname=tagname, body=body)
		else:
			html_str += "<p>{line}</p>".format(line=line)
	return html_str

def render_course_page(course_id,page_id):
	"""Returns page page_id of course course_id in flask-renderable format"""
	course = parse_file("courses/"+course_id+".mgs")
	if page_id < len(course.pages):
		template,data = course.pages[page_id]
	else:
		return "ERROR: Page Outta Range"
	first = False
	last=False
	title = course.title
	if page_id==0:
		first=True
	if page_id == len(course.pages)-1:
		last=True
	for key in data.keys():
		data[key] = safe_md_to_html(data[key])
	return render_template("render/"+template+".html",course_id=course_id,page_id=page_id,first=first,last=last,title=title,**data)

def render_timeline(course_id,page_id):
	"""DEPRICATED - Returns timeline for page page_id of course course_id in flask-renderable format"""
	course = parse_file("courses/"+course_id+".mgs")
	if page_id != 0:
		previous_time = course.pages[page_id-1][1]["time"]
	else:
		previous_time = ""
	current_time = course.pages[page_id][1]["time"]
	try:
		next_time = course.pages[page_id+1][1]["time"]
	except:
		next_time = ""
	return render_template("render/timeline.html",previous=previous_time,current=current_time,next=next_time)