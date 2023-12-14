from pdf2image import convert_from_path
import pytesseract
from PIL import Image

import numpy as np
target_folder = "textbooks\\chemistry\\AS&A_levels"
pytesseract.pytesseract.tesseract_cmd = r"C:\\Users\\samru\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe"

# start is 13
# end is 884

starting_page = 13
ending_page = 884

# ending_page = 13

def make_img(pdf, target_folder, start, end):
  images = convert_from_path(pdf, first_page=start, last_page=end)

  for i, item in enumerate(images):
    # Save pages as images in the pdf
    item.save(target_folder+'\\pages\\'+ str(i) +'.jpg', 'JPEG')

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

def flattenlist(nestedlist):  
    if len(nestedlist) == 0:  
        return nestedlist  
    if isinstance(nestedlist[0], list):  
        return flattenlist(nestedlist[0]) + flattenlist(nestedlist[1:])  
    return nestedlist[:1] + flattenlist(nestedlist[1:])  

def aray_has_nothing(aray):
  flattened = flattenlist(aray)

  if flattened == []:
    return True
  return False

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

  # removes none
  out = [[[[[value for value in dim4 if value is not None] for dim4 in dim3] for dim3 in dim2] for dim2 in dim1] for dim1 in out]

  #Removes empty pages
  new_out = []
  for pages in range(len(out)):
    if not aray_has_nothing(out[pages]):
      new_out.append(out[pages])

    out = new_out
  
  #Removes empty blocks
  new_out = []
  for pages in (out):
    new_pages = []
    for block in range(len(pages)):
      if not aray_has_nothing(pages[block]):
        new_pages.append(pages[block])
    new_out.append(new_pages)
  out = new_out

  return new_out

def append_images_vertically(image1_path, image2_path, output_path):
    # Open the images
    image1 = Image.open(image1_path)
    image2 = Image.open(image2_path)

    # Get the size of the first image
    width1, height1 = image1.size
    
    # Get the size of the second image
    width2, height2 = image2.size

    # Calculate the width and height of the combined image
    max_width = max(width1, width2)
    total_height = height1 + height2

    # Create a new image with the calculated size
    new_image = Image.new('RGB', (max_width, total_height))

    # Paste the first image onto the new image
    new_image.paste(image1, (0, 0))

    # Paste the second image below the first one
    new_image.paste(image2, (0, height1))

    # Save the result
    new_image.save(output_path, 'JPEG')

# skipping page 0 because it's page 13 in reality, which is an odd number
for x in range (1, 871, 2):
  append_images_vertically(f"/Users/kushalb/Documents/VSCode/ASK-ai/textbooks/chemistry/AS&A_levels/pages/{x}.jpg", 
  f"/Users/kushalb/Documents/VSCode/ASK-ai/textbooks/chemistry/AS&A_levels/pages/{x+1}.jpg", 
  f"/Users/kushalb/Documents/VSCode/ASK-ai/textbooks/chemistry/AS&A_levels/joint_pages/{x}.jpg")


def format_pytessaract_obj(lst, delimiters = ["\n\n----\n\n", "\n\n\n", "\n\n", "\n", " "]):
    result = ""
    for i, dim1 in enumerate(lst):
        for j, dim2 in enumerate(dim1):
            for k, dim3 in enumerate(dim2):
                for l, dim4 in enumerate(dim3):
                    for m, word in enumerate(dim4):
                        result += word
                        if m < len(dim4) - 1:
                            result += delimiters[4]
                    if l < len(dim3) - 1:
                        result += delimiters[3]
                if k < len(dim2) - 1:
                    result += delimiters[2]
            if j < len(dim1) - 1:
                result += delimiters[1]
        if i < len(lst) - 1:
            result += delimiters[0]
    return result

