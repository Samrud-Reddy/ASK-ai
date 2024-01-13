import json
import os
from pathlib import Path
from pdf2image.pdf2image import convert_from_path
import pytesseract
from PIL import Image


class Chapter:
    """An class representing a chapter
        Attributes:
            start (int): The start of the chapter 
            end (int): The end of the chapter 
            name (str): The name of the chapter 
    """
    def __init__(self, start: int, end: int, name: str):
        self.start = start 
        self.end = end
        self.name = name

    def is_in_chapter(self, page: int) -> bool:
        return self.start <= page or self.end > page


class Paragraph:
    """An class representing a paragraph
        Attributes:
            lines (list[list[str]]): A list of strings each element being a list of words which might have nones
            textbook_name (str): The name of the text book the paragraph came from
            subject_name (str): The name of the subject
            page (int): The page the paragraph comes from
            para_no (int): The paragraph number in the block
            height (float): The height in pixels of the text
            chapter_name (str): The name of the chapter the paragraph came from
            text (str): The litreal text of the paragraph
    """
    def __init__(self, lines: list[list[str]], textbook_name: str, subject_name:str, page: int, para_no: int, height: float, chapter: str|None = None) -> None:
        """Initializes a paragraph
            Args:
                lines (list[list[str]]): A list of strings each element being a list of words which might have nones
                textbook_name (str): The name of the text book the paragraph came from
                page (int): The page the paragraph comes from
                para_no (int): The paragraph number in the block
                height (float): The height in pixels of the text
                chapter (str): The chapter from where the paragraph came from
        """
        new_par = []
        for line in lines:
            new_line = []
            for word in line:
                if word:
                    new_line.append(word)

            if new_line:
                new_par.append(" ".join(new_line))

        self.lines = new_par

        self.textbook_name = textbook_name
        self.page = page
        self.para_no = para_no
        self.height = height
        
        self.subject_name = subject_name
        self.chapter_name:str|None = chapter
    
        self.text = self.get_text()

    def get_text(self) -> str:
        """Converts lines to text"""
        return "\n".join(self.lines)

    def get_json(self):
        """Gets the json of the paragraph"""
        return json.dumps(self)

    def __str__(self) -> str:
        return "\n".join(self.lines)


    def __repr__(self) -> str:
        """Returns the reprentasion of this class"""
        return f"   Paragraph from {self.textbook_name}, page {self.page}, para number {self.para_no} and height {self.height}\n{self.__str__()}"
            

class Textbook:
    """A class representing textbooks

    Attributes:
        name (str): The textbook name
        subject_name (str): The subject name of the textbook
        target_folder (str): The folder where the pdf of the same name is located
        starting_page (int): The page from where to start the image to text conversion
        ending_page (int): The page from where to end the image to text conversion
        chapters (list[Chapter]): The list of all the chapters in the textbooks
        pages (str): The folder where to store the temprary image files
    """

    def __init__(self, name: str, subject_name:str, target_folder: Path, starting_page: int, ending_page: int, chapters: list[Chapter] = [], pages: str = "pages") -> None:
        """Initialize a new textbook instance.
        Args:
            name (str): The text book name
            subject_name (str): The subject name of the textbook
            target_folder (str): The folder where the pdf of the same name is located
            starting_page (int): The page from where to start the image to text conversion
            ending_page (int): The page from where to end the image to text conversion
            chapters (list[Chapter]): The list of all the chapters in the textbooks
            page (int): The folder where to store the temprary image files
        """

        if (not target_folder.is_dir()) or (not target_folder.exists()):
            raise Exception("Input is not a folder")

        self.name: str = name
        self.target_folder: Path = target_folder
        self.subject_name: str = subject_name

        self.starting_page: int = starting_page
        self.ending_page: int = ending_page

        self.chapters: list[Chapter] = chapters
        

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
        

    def make_paragraphs(self, page: int, treshold: int = 50) -> list[Paragraph]:
        """Converts an image to a list of paragraphs
        Args:
            page (str): the page number to convert
            treshold (int): The allowence treshold from 0 to 100, 0 being everything and 100 being nothing
        """
        file_name = str(self.pages) + "/" + str(page) + ".jpg"
        data = pytesseract.image_to_data(Image.open(file_name) , lang="eng", output_type=pytesseract.Output.DICT)

        out = []
        cur_par = []
        cur_par_heights = []
        cur_line = []
        
        last_level = 5

        data = Textbook.invert_dict_list(data)

        row = data[0]
        for row in data:
            if row["conf"] <= treshold:
                row["text"] = None
            else:
                cur_par_heights.append(row["height"])

            if row["level"] < last_level:
                if not Textbook.aray_has_nothing(cur_line):
                    cur_par.append(cur_line)

                if row["level"] < 4:
                    if not Textbook.aray_has_nothing(cur_par):
                        avg = sum(cur_par_heights) / (len(cur_par_heights) if cur_par_heights else 1)
                        out.append(Paragraph(cur_par, self.name, self.subject_name, page, row["par_num"], avg))

                    cur_par_heights = []
                    cur_par = []
                cur_line = []

            last_level = row["level"]
            cur_line.append(row["text"])


        avg_height = sum(cur_par_heights) / len(cur_par_heights)
        cur_par.append(cur_line)
        out.append(Paragraph(cur_par, self.name, self.subject_name, page, row["par_num"], avg_height))


        return out

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
        """Stitches all alternate images vertically
        """
        cur_page = self.starting_page

        while cur_page + 1 <= self.ending_page:
            self.append_images_vertically(Path(str(self.pages) + "/" + str(cur_page) + ".jpg"),
                                          Path(str(self.pages) + "/" + str(cur_page+1) + ".jpg"),
                                          Path(str(self.pages) + "/" + str(cur_page) + "&" + str(cur_page+1) + ".jpg"))

            os.remove(Path(str(self.pages) + "/" + str(cur_page) + ".jpg"))
            os.remove(Path(str(self.pages) + "/" + str(cur_page + 1) + ".jpg"))
            

            cur_page += 2
