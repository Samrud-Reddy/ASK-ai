from pdf2image import convert_from_path
import pytesseract
from PIL import Image

import numpy as np
# target_folder = "textbooks\\chemistry\\AS&A levels"
pytesseract.pytesseract.tesseract_cmd = r"C:\\Users\\samru\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe"


# starting_page = 13
# ending_page = 884

# ending_page = 13

def make_img(pdf, target_folder, start, end):
  images = convert_from_path(pdf, first_page=start, last_page=end)

  for i, item in enumerate(images):
    # Save pages as images in the pdf
    item.save(target_folder+'\\pages\\'+ "test" +'.jpg', 'JPEG')

def debug_string(path):
  data = pytesseract.image_to_data(Image.open(path), lang="eng", output_type=pytesseract.Output.DICT)
  out = ""
  for i in range(len(data["level"])):
    if data["conf"][i] != -1:
      out += (str(data['text'][i])) + "\n"
      out += (f"Level:{data['level'][i]}     Block_num:{data['block_num'][i]}        Para:{data['par_num'][i]}       line_num:{data['line_num'][i]}        word_num:{data['word_num'][i]}       Confidance:{data['conf'][i]}") + "\n\n"

  with open("read.txt", "w+") as f:
    f.write(out)

def invert_dict_list(data):
  converted_data = []

  for i in range(len(data["level"])):
    row = {}
    for key in data:
      row[key] = data[key][i]
    
    converted_data.append(row)
  
  return converted_data





def stringify_image(path, treshold = 70):
  data = pytesseract.image_to_data(Image.open(path), lang="eng", output_type=pytesseract.Output.DICT)

  out = []

  cur_page = []
  cur_block = []
  cur_par = []
  cur_line = []

  data = invert_dict_list(data)

  for row in data:

    #Sets all unconfidant values to None
    if row["conf"] < treshold:
      row["text"] = None

    match row["level"]:
      #Word
      case 5:
        pass
      #Line
      case 4:
        if cur_line:
          cur_par.append(cur_line)
          cur_line = []

      
      #Paragraph
      case 3:
        if cur_par:
          cur_block.append(cur_par)
          cur_par = []


      #Block
      case 2:
        if cur_block:
          cur_page.append(cur_block)
          cur_block = []


      #Page
      case 1:
        if cur_page:
          out.append(cur_page)
          cur_page = []


    cur_line.append(row["text"])
    
  cur_par.append(cur_line)
  cur_block.append(cur_par)
  cur_page.append(cur_block)
  out.append(cur_page)

  # removed none
  out = [[[[[value for value in dim4 if value is not None] for dim4 in dim3] for dim3 in dim2] for dim2 in dim1] for dim1 in out]

  #removes arrays that only contain empty arrays
  # out = to_lazy(out)

  return out

def to_lazy(out):
  for page in out:
    for block in page:
      if block[0] == []:
        out.remove(block)



out = stringify_image("C:\\Users\\samru\\Desktop\\Code\\ASK ai\\textbooks\\chemistry\\AS&A levels\\pages\\test.jpg")


print(out)
# with open("read.txt", "+w") as f:
#   f.write(stringify_image("C:\\Users\\samru\\Desktop\\Code\\ASK ai\\textbooks\\chemistry\\AS&A levels\\pages\\test.jpg"))
