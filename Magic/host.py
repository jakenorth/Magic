#########################################
# Python 3.x                            #
# Requires Flask - "pip3 install flask" #
#########################################

# Imports
from flask import *
from render import render_course_page, render_timeline
from parse import Course, parse_file

# App Setup
storage_path = "store"
app = Flask(__name__,template_folder=storage_path)

# Generic Render
def render(path,**variables):
	extention = path.split(".")[-1]
	if extention == "html":
		f_render = render_template
		return f_render(path,**variables)
	mimemap = {
		"txt":"text",
		"js":"text/javascript",
		"css":"text/css",
		"md":"text",
		"jpeg":"image/jpeg",
		"jpg":"image/jpg",
		"png":"image/png",
		"gif":"image/gif",	}
	print(path)
	return send_file(storage_path+"/"+path,mimetype=mimemap[extention])

### Routes
## Course Rendering
@app.route("/c/<course_id>")
def render_course(course_id):
	return render("render/CourseFrame.html",
			course_id=course_id,title="Course " + course_id,len=len(parse_file("courses/"+course_id+".mgs").pages))

@app.route("/c/<course_id>/p/<page_id>")
def send_page(course_id, page_id):
	return render_course_page(course_id,int(page_id))
@app.route("/t/<course_id>/p/<page_id>")
def send_timeline(course_id,page_id):
	return render_timeline(course_id,int(page_id))

## Other Pages
@app.route("/")
def temp_home():
	message = """
	Welcome to the future homepage of Magic.  Right now we are using wix as our temporary homepage. <br>
	<a href="https://jakewnorth.wixsite.com/magic">Go to the temporary homepage</a><br>
	<a href="/c/jld">Preview the first course</a>
	"""
	return message

@app.route("/favicon.ico")
def send_favicon():
	return render("assets/stars.jpg")

@app.errorhandler(404)
def error404(e):
	return render("assets/404.jpg")

## Utilities

@app.route("/sleep/<seconds>")
def sleepseconds(seconds):
	import time
	time.sleep(int(seconds))
	return "done"

@app.route("/assets/<path>")
def send_asset(path):
	try:
		return render("assets/" + path)
	except:
		return render("assets/404.jpg")

@app.route("/throw/<error>")
def send_error(error):
	return "FATAL ERROR: " + error +"<br>Contact Jake for more info"

## Decaching - remove for production
@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

# Runner
app.run(host="0.0.0.0",port=80)