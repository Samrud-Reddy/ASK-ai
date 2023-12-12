from pdf2image import convert_from_path
import pytesseract
from PIL import Image
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

def stringify_image(path, treshold = 70):
  data = pytesseract.image_to_data(Image.open(path), lang="eng", output_type=pytesseract.Output.DICT)

  #Remove low conf
  to_remove = []
  for i in range(len(data["level"])):  
    if data["conf"][i] < treshold:
      to_remove.append(i)
  
  to_remove.reverse()
  for i in to_remove:
    for key in data:
      data[key].pop(i)

  
  out = []
  prev_block_no = data["block_num"][0]
  prev_line_no = data["line_num"][0]

  curr_block_list = []
  curr_line = ""

  for i in range(len(data["level"])):  
    text = data["text"][i]

    curr_block_no = data["block_num"][i]
    curr_line_no = data["line_num"][i]

    if prev_block_no != curr_block_no:
      if curr_block_list == []:
        curr_block_list.append(curr_line)
        
      out.append(curr_block_list)
      
      curr_line = text
      curr_block_list = []

      prev_block_no = curr_block_no
      prev_line_no = curr_line_no
      continue
      
    if prev_line_no != curr_line_no:
      curr_line += " "+text

      prev_line_no = curr_line_no
      continue

    curr_line += " " + text

  
  out = [i[0] for i in out]

  out = "\n\n".join(out)

  return out




with open("read.txt", "+w") as f:
  f.write(stringify_image("C:\\Users\\samru\\Desktop\\Code\\ASK ai\\textbooks\\chemistry\\AS&A levels\\pages\\test.jpg"))
