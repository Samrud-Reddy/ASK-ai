from pdf2image import convert_from_path

target_folder = "textbooks\\chemistry\\AS&A levels"


starting_page = 13
# ending_page = 884

ending_page = 13

images = convert_from_path("C:\\Users\\samru\\Desktop\\Code\\ASK ai\\textbooks\\chemistry\\AS&A levels\\AS&A levels.pdf", first_page=starting_page, last_page=ending_page)

for i in images:
  print("hello")
      # Save pages as images in the pdf
  i.save(target_folder+'\\pages\\'+ '1' +'.jpg', 'JPEG')

  print("hello")