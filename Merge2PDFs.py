import PyPDF2
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import uuid

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger")
        # self.root.geometry("500x300")
        
       # Frame for PDF 1
        self.frame1 = ttk.LabelFrame(root, text="PDF 1", padding="10")
        self.frame1.pack(pady=20, padx=10, fill="x")

        self.file1_label = ttk.Label(self.frame1, text="Selected File:")
        self.file1_label.grid(row=0, column=0, sticky="w")

        self.file1_pages_label = ttk.Label(self.frame1, text="Pages in PDF:")
        self.file1_pages_label.grid(row=1, column=0, sticky="w")

        self.file1_label_value = tk.StringVar()
        self.file1_pages_value = tk.StringVar()

        ttk.Label(self.frame1, textvariable=self.file1_label_value).grid(row=0, column=1, sticky="w")
        ttk.Label(self.frame1, textvariable=self.file1_pages_value).grid(row=1, column=1, sticky="w")

        self.file1_page_label = ttk.Label(self.frame1, text="Page Range:")
        self.file1_page_label.grid(row=2, column=0, sticky="w")

        self.file1_page_entry = ttk.Entry(self.frame1)
        self.file1_page_entry.grid(row=2, column=1, sticky="w", padx=5)

        self.file1_button = ttk.Button(self.frame1, text="Choose File", command=self.choose_file1)
        self.file1_button.grid(row=0, column=2, rowspan=3, padx=10)

        self.delete1_button = ttk.Button(self.frame1, text="Delete", command=self.delete_file1)
        self.delete1_button.grid(row=0, column=3, rowspan=3, padx=10)
        
        # Swap Button
        self.swap_button = ttk.Button(root, text="Swap Files", command=self.swap_pdfs)
        self.swap_button.pack(pady=10)


        # Frame for PDF 2
        self.frame2 = ttk.LabelFrame(root, text="PDF 2", padding="10")
        self.frame2.pack(pady=20, padx=10, fill="x")

        self.file2_label = ttk.Label(self.frame2, text="Selected File:")
        self.file2_label.grid(row=0, column=0, sticky="w")

        self.file2_pages_label = ttk.Label(self.frame2, text="Pages in PDF:")
        self.file2_pages_label.grid(row=1, column=0, sticky="w")

        self.file2_label_value = tk.StringVar()
        self.file2_pages_value = tk.StringVar()

        ttk.Label(self.frame2, textvariable=self.file2_label_value).grid(row=0, column=1, sticky="w")
        ttk.Label(self.frame2, textvariable=self.file2_pages_value).grid(row=1, column=1, sticky="w")

        self.file2_page_label = ttk.Label(self.frame2, text="Page Range:")
        self.file2_page_label.grid(row=2, column=0, sticky="w")

        self.file2_page_entry = ttk.Entry(self.frame2)
        self.file2_page_entry.grid(row=2, column=1, sticky="w", padx=5)

        self.file2_button = ttk.Button(self.frame2, text="Choose File", command=self.choose_file2)
        self.file2_button.grid(row=0, column=2, rowspan=3, padx=10)

        self.delete2_button = ttk.Button(self.frame2, text="Delete", command=self.delete_file2)
        self.delete2_button.grid(row=0, column=3, rowspan=3, padx=10)

        # Merge Button
        self.merge_button = ttk.Button(root, text="Merge PDFs", command=self.merge_pdfs)
        self.merge_button.pack(pady=20)


    def choose_file1(self):
        self.file1_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if self.file1_path:
            self.file1_label_value.set(os.path.basename(self.file1_path))
            with open(self.file1_path, "rb") as file1:
                pdf_reader = PyPDF2.PdfReader(file1)
                self.file1_pages_value.set(str(len(pdf_reader.pages)))

    def choose_file2(self):
        self.file2_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if self.file2_path:
            self.file2_label_value.set(os.path.basename(self.file2_path))
            with open(self.file2_path, "rb") as file2:
                pdf_reader = PyPDF2.PdfReader(file2)
                self.file2_pages_value.set(str(len(pdf_reader.pages)))

    def delete_file1(self):
        self.file1_path = ""
        self.file1_label_value.set("")
        self.file1_pages_value.set("")
        self.file1_page_entry.delete(0, tk.END)

    def delete_file2(self):
        self.file2_path = ""
        self.file2_label_value.set("")
        self.file2_pages_value.set("")
        self.file2_page_entry.delete(0, tk.END)

    def merge_pdfs(self):
        if not self.file1_path or not self.file2_path:
            messagebox.showwarning("Warning", "Please select both PDF files.")
            return

        self.file1_pages = self.file1_page_entry.get()
        self.file2_pages = self.file2_page_entry.get()

        if not self.file1_pages:
            self.file1_pages = f"1-{self.file1_pages_value.get()}" if self.file1_pages_value.get() else ""

        if not self.file2_pages:
            self.file2_pages = f"1-{self.file2_pages_value.get()}" if self.file2_pages_value.get() else ""

        pdf_writer = PyPDF2.PdfWriter()

        with open(self.file1_path, "rb") as file1:
            pdf_reader = PyPDF2.PdfReader(file1)
            for page_num in self.parse_pages(self.file1_pages, len(pdf_reader.pages)):
                pdf_writer.add_page(pdf_reader.pages[page_num])

        with open(self.file2_path, "rb") as file2:
            pdf_reader = PyPDF2.PdfReader(file2)
            for page_num in self.parse_pages(self.file2_pages, len(pdf_reader.pages)):
                pdf_writer.add_page(pdf_reader.pages[page_num])

        # Get the directory path of the first PDF file
        save_directory = os.path.dirname(self.file1_path)

        merged_filename = f"merged_{uuid.uuid4().hex}.pdf"
        merged_filepath = os.path.join(save_directory, merged_filename)

        with open(merged_filepath, "wb") as merged_file:
            pdf_writer.write(merged_file)

        messagebox.showinfo("Info", f"PDFs merged and saved as: {os.path.basename(merged_filepath)}")


    def parse_pages(self, page_range_str, total_pages):
        if not page_range_str:
            return range(total_pages)

        selected_pages = set()
        for part in page_range_str.split(','):
            if '-' in part:
                start, end = part.split('-')
                start, end = int(start), int(end)
                selected_pages.update(range(start - 1, min(end, total_pages)))
            else:
                selected_pages.add(int(part) - 1)
        return selected_pages


    def swap_pdfs(self):
        self.file1_path, self.file2_path = self.file2_path, self.file1_path

        if self.file1_path:
            with open(self.file1_path, "rb") as file1:
                pdf_reader = PyPDF2.PdfReader(file1)
                self.file1_label_value.set(os.path.basename(self.file1_path))
                self.file1_pages_value.set(str(len(pdf_reader.pages)))
        else:
            self.file1_label_value.set("")
            self.file1_pages_value.set("")

        if self.file2_path:
            with open(self.file2_path, "rb") as file2:
                pdf_reader = PyPDF2.PdfReader(file2)
                self.file2_label_value.set(os.path.basename(self.file2_path))
                self.file2_pages_value.set(str(len(pdf_reader.pages)))
        else:
            self.file2_label_value.set("")
            self.file2_pages_value.set("")

        self.file1_page_entry.delete(0, tk.END)
        self.file2_page_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop()
