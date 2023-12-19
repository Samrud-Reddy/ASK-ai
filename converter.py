import os
from pathlib import Path
from pdf2image.pdf2image import convert_from_path
import pytesseract
from PIL import Image


class chapter:
    def __init__(self, start: int, end: int, name: str):
        self.start = start 
        self.end = end
        self.name = name

    def is_in_chapter(self, page: int) -> bool:
        return self.start <= page or self.end > page


class Textbook:
    """A class representing textbooks

    Attributes:
        target_folder (str): The folder where the pdf of the same name is located
        starting_page (int): The page from where to start the image to text conversion
        ending_page (int): The page from where to end the image to text conversion
        chapters (list[chapter]): The list of all the chapters in the textbooks
        pages (str): The folder where to store the temprary image files

    Methods:
        __init__: Initializes a new instance of the Textbook class.

    """

    def __init__(self, target_folder: Path, starting_page: int, ending_page: int, chapters: list[chapter] = [], pages: str = "pages") -> None:
        """Initialize a new textbook instance.
        Args:
            target_folder (str): The folder where the pdf of the same name is located
            starting_page (int): The page from where to start the image to text conversion
            ending_page (int): The page from where to end the image to text conversion
            chapters (list[chapter]): The list of all the chapters in the textbooks
            page (int): The folder where to store the temprary image files
        """

        if (not target_folder.is_dir()) or (not target_folder.exists()):
            raise Exception("Input is not a folder")

        self.target_folder: Path = target_folder
        self.starting_page: int = starting_page
        self.ending_page: int = ending_page

        self.chapters: list[chapter] = chapters
        

        self.pdf_path: Path = Path(str(target_folder) + "/" + str(target_folder).split("/")[-1] + ".pdf")

        if (not self.pdf_path.exists()) and self.pdf_path.is_file():
            raise Exception("PDF does not exist")


        self.pages: Path = Path(str(target_folder) + "/" + str(pages))
        if (not self.pages.exists()) and self.pages.is_dir():
            raise Exception("Page folder does not exist")


    def make_an_image(self, page: int):
        """Makes an image
        Args:
            page (int): The page of the image you want to convert
        """
        image = convert_from_path(self.pdf_path, first_page=page, last_page=page)
        image[0].save(str(self.pages) + "/" +str(page)+'.jpg', 'JPEG')


    def convert_all_pages(self):
        """Converts all pages to images
        """
        for i in range(self.starting_page, self.ending_page + 1):
            self.make_an_image(i)
        

    def stringify_image(self, file_name: str, treshold: int = 70):
        """Converts an image to a string
        Args:
            file_name (str): The name of the file to convert, the folder is the one set by self.pages
            treshold (int): The allowence treshold from 0 to 100, 100 being everything and 1 being nothing
        """
        data = pytesseract.image_to_data(Image.open(str(self.pages) + "/" + file_name + ".jpg") , lang="eng", output_type=pytesseract.Output.DICT)

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


    @staticmethod
    def invert_dict_list(data):
        """Converts a dictionary of lists to a list of dictionart
            Args:
                data: A dictionary of lists
        """
        converted_data = []

        for i in range(len(data["level"])):
            row = {}
            for key in data:
                row[key] = data[key][i]
        
            converted_data.append(row)
      
        return converted_data


    @staticmethod
    def flattenlist(nestedlist: list):
        """Converts a multi dimesional list to a single dimesional list
        """
        if len(nestedlist) == 0:
            return nestedlist  
        if isinstance(nestedlist[0], list):  
            return Textbook.flattenlist(nestedlist[0]) + Textbook.flattenlist(nestedlist[1:])  
        return nestedlist[:1] + Textbook.flattenlist(nestedlist[1:])  


    @staticmethod
    def aray_has_nothing(aray: list):
        """Detects if an array has nothing in it or is made up of lists that also that have anything in it
        """
        flattened = Textbook.flattenlist(aray)
    
        if flattened == []:
            return True
        return False

    @staticmethod

    def format_pytessaract_obj(five_dimensional_list: list, delimiters = ["\n\n----\n\n", "\n\n\n", "\n\n", "\n", " "]):

        """Formats the 5 dimesional list returned by stringify_image

            Args:
                five_dimensional_list: 5 dimesional list of pages[blocks[para[lines[words[]]]]]
                delimiters: the seperators in order pages, blocks, lines, words
        """
        result = ""
        for i, dim1 in enumerate(five_dimensional_list):
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
            if i < len(five_dimensional_list) - 1:
                result += delimiters[0]
        return result


    @staticmethod
    def append_images_vertically(image1_path: Path, image2_path: Path, output_path: Path):
        """Stitches images vertically
            Args:
                image1_path (Path): The path to the first image
                image2_path (Path): The path to the second image
                output_path (Path): Path to save the image
        """
        image1 = Image.open(str(image1_path))
        image2 = Image.open(str(image2_path))

        width1, height1 = image1.size
        
        width2, height2 = image2.size

        max_width = max(width1, width2)
        total_height = height1 + height2

        new_image = Image.new('RGB', (max_width, total_height))

        new_image.paste(image1, (0, 0))

        new_image.paste(image2, (0, height1))

        new_image.save(str(output_path), 'JPEG')


    def append_all_images_vertically(self):
        cur_page = self.starting_page

        while cur_page + 1 <= self.ending_page:
            self.append_images_vertically(Path(str(self.pages) + "/" + str(cur_page) + ".jpg"),
                                          Path(str(self.pages) + "/" + str(cur_page+1) + ".jpg"),
                                          Path(str(self.pages) + "/" + str(cur_page) + "&" + str(cur_page+1) + ".jpg"))

            os.remove(Path(str(self.pages) + "/" + str(cur_page) + ".jpg"))
            os.remove(Path(str(self.pages) + "/" + str(cur_page + 1) + ".jpg"))
            

            cur_page += 2
