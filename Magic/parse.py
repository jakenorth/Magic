# Data Definitions
class Course():
  title = "Untitled Course"
  pages = []
  def __str__(self):
    header = "--- " + self.title + " ---"
    pages = self.pages
    for page in pages:
      title, data = page
      print(title)
      for key in data:
        print("### " + key + ":   " + "\n     ".join(str(data[key]).split("\n")))
      print()


# CONTSTUCT Page :: (template:str, data:dict)

# Utilities
def no_blanks(list_with_blanks):
  new_list = []
  for item in list_with_blanks:
    if not item in ["",[]]:
      new_list.append(item)
  return new_list

def seperate_by(sequence,divider):
  meta_list =[]
  current = []
  for item in sequence:
    if item == divider:
      meta_list.append(current)
      current = []
    else:
      current.append(item)
  meta_list.append(current)
  return meta_list

def keyword_eval(code):
  exec(code)
  del code
  return locals()
# Main
def parse_file(path):
  """Returns a course object from a mgs file"""
  with open(path) as f:
    raw = f.read()
  # Parsing Flow
  lines = raw.split("\n")
  
  title = lines[0]
  lines = lines[1:]

  lines = no_blanks(lines)
  pages = no_blanks(seperate_by(lines, "***"))
  this_course = Course()
  this_course.title = title
  this_course.pages = []
  for page in pages:
    page_template,page_time = page[0].split(" ",1)
    page_data = keyword_eval("\n".join(page[1:]))
    if page_time == "-":
      page_time = "no date"
    page_data["time"] = page_time
    this_course.pages.append((page_template, page_data))
  return this_course