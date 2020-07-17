#!/usr/bin/env python3

from urllib.parse import quote, urlencode

_base_url = "https://img.shields.io/static/v1"


def create_table_row(data:list=[], columns = 0):
  #print("row", data)
  temp = "|".join(data)
  if columns > 0: 
    missing = columns - len(data)

    if missing > 0:
      temp = temp + (missing * "|")

  return "|{}|\n".format(temp)
  
  
def create_table_header(data:list, columns = 0):
  return create_table_row(data, columns) + "|" + "|".join([":-:"] * columns) + "|\n"
  
def make_title(title, level=1):
  return "{} {}\n".format("#"* level, title)

def make_table(data):
  numb_columns = len(data[0])
  header = create_table_header(data[0], numb_columns)
  body = ""
  for r in data[1:]:
      body += create_table_row(r, numb_columns)
  return header + body

def make_badge(label="", message="", color="green", cache_seconds:int=3600):
  query = {
            "label": label,
            "message": message,
            "color":color,
            "cacheSeconds": cache_seconds
          }
  params = urlencode(query)
  final_url = "{}?{}".format(_base_url, params)
  badge = "![]({})".format(final_url)

  return badge

if __name__ == "__main__":
  dat = []
  dat.append(["A","B","C"])
  dat.append(["1","2","3"])
  dat.append(["4",make_badge("hello","world!","blue", 300),"6"])
  dat.append(["7","8","9"])
  dat.append(["10","11","12"])
  
  f = open("test_file.md", "w")
  f.write(make_title("Hello World!"))
  f.write(make_table(dat))
  f.close()
# general 
#  last updated 
#  update interval 
#  size of db on disk

# per config input
#  human readable name
#  enable/disable, move disabled down
#  last updated
#  time since last update
#  statusup/down
#  # new data since last check
#  total count


# per archive type
#  total number of data
#  last updated
