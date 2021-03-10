from tkinter import *
from tkinter import ttk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfFileReader
import os
import fitz
import io
from PIL import Image

class Notebook:
    def __init__(self,master):
        master.title("PDF Tool.")
        master.resizable(False, False)

        notebook = ttk.Notebook(root)
        notebook.grid()

        #Make frame1
        frame1 = ttk.Frame(notebook)
        notebook.add(frame1, text='Page Counter')

        #Make frame2
        frame2 = ttk.Frame(notebook)
        notebook.add(frame2, text='Image Extractor')

#----------------------------------------------------------------------------------------------------------------------

        #Work on frame 1
        self.extra_info = BooleanVar()

        ttk.Label(frame1, text="PDF Page Counter", font=('Times New Roman', 16, 'bold')).grid(row=0, column=0,
                                                                                              sticky='nw', padx=10)
        ttk.Label(frame1, wraplength=250,
                  text="Choose some .pdf files. This application will state the number of slides in them!",
                  font=('Times New Roman', 12)).grid(row=1, column=0, sticky='nw', padx=10)

        # Button for choosing ppt files
        ttk.Button(frame1, text='Browser...', command=self.fileOpener).grid(row=3, column=0, padx=10, pady=10,
                                                                            sticky='w')

        # Checkbutton to choose details.
        Checkbutton(frame1, text='Do you want a Summary?', var=self.extra_info).grid(row=2, column=0, padx=10, pady=10,
                                                                                     sticky='w')

#---------------------------------------------------------------------------------------------------------------------
        # Work on frame 2.

        ttk.Label(frame2, text="PDF Image Extractor", font=('Times New Roman', 16, 'bold')).grid(row=0, column=0,
                                                                                                 sticky='nw', padx=10)
        ttk.Label(frame2, wraplength=250,
                  text="Select a .pdf file. This application will extract all images from it!",
                  font=('Times New Roman', 12)).grid(row=1, column=0, sticky='nw', padx=10)

        ttk.Button(frame2, text='Browser...', command=self.path_selector).grid(row=3, column=0, padx=10, pady=10,
                                                                               sticky='w')

#----------------------------------------------------------------------------------------------------------------------
    #Section of Methods

    def count_files(self, files):
        library = {}

        # Save all files in a dictionary  with initial count of slides set to 0
        for file in files:
            if os.path.abspath(file).endswith('.pdf'):
                library[os.path.abspath(file)] = PdfFileReader(open(os.path.abspath(file), 'rb')).getNumPages()

            else:
                messagebox.showinfo(title="Unidentified Files",
                                    message='Error! Please choose .pdf files.')

        details = ""

        for key, value in library.items():
            details += f"Pages:{value}\t\tFile:{os.path.basename(key)}\n"

        # Trigger
        if (self.extra_info.get()):
            details += "-------------------------------\n"
            total = 0
            for count in library.values():
                total += count
            details += f"Total {total} pages in {len(library)} pdfs."

        messagebox.showinfo(title="Pages Found", message=details)

        # File opening method.

    def fileOpener(self):
        self.f = filedialog.askopenfilenames()
        self.count_files(self.f)

    def imgExtractor(self, f, p):
        self.file = f

        # Directory with name same as that of pdf file
        self.directory = os.path.basename(self.file[0]).replace('.pdf', '')
        # Parent Directory path
        self.parent_dir = p

        # combined path
        self.path = os.path.join(self.parent_dir, self.directory)

        # Make a directory to store images
        os.mkdir(self.path)
        print("Directory '% s' created" % self.directory)

        pdf_file = fitz.open(self.file[0])
        for page_index in range(len(pdf_file)):
            # get the page itself
            page = pdf_file[page_index]
            image_list = page.getImageList()
            # printing number of images found in this page
            if image_list:
                print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
            else:
                print("[!] No images found on page", page_index)
            for image_index, img in enumerate(page.getImageList(), start=1):
                # get the XREF of the image
                xref = img[0]
                # extract the image bytes
                base_image = pdf_file.extractImage(xref)
                image_bytes = base_image["image"]
                # get the image extension
                image_ext = base_image["ext"]
                # load it to PIL
                image = Image.open(io.BytesIO(image_bytes))
                # save it to local disk
                image.save(open(f"{self.path}/image{page_index + 1}_{image_index}.{image_ext}", "wb"))

    def path_selector(self):
        self.f = filedialog.askopenfilenames()
        print(os.path.basename(self.f[0]))
        messagebox.showinfo(title="Select Path", message="Please select the directory where to store extracted images.")
        self.p = filedialog.askdirectory()
        print(self.p)
        self.imgExtractor(self.f, self.p)





root = Tk()
notebook = Notebook(root)
root.mainloop()