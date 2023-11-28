import zipfile
import PyPDF2
from tqdm import tqdm

def pdf_files_in_zip(zip_file):
    files = []
    with zipfile.ZipFile(zip_file, 'r') as myzip:
        files = [file for file in myzip.namelist() if file.lower().endswith('.pdf')]
    return files

zip_folder_path = "C:/Users/vaishnavi.pandey/Downloads/data.zip"
output_file_train = "output_train.txt"
output_file_val = "output_val.txt"
vocab_file = "vocab.txt"

pdf_files = pdf_files_in_zip(zip_folder_path)
total_files = len(pdf_files)

# Calculate the split indices
split_index = int(total_files * 0.9)  # 90% for training
pdf_files_train = pdf_files[:split_index]
pdf_files_val = pdf_files[split_index:]

# Process the PDF files for training and validation separately
vocab = set()

# Process the training PDF files
with open(output_file_train, "w", encoding="utf-8") as outfile:
    for filename in tqdm(pdf_files_train, total=len(pdf_files_train)):
        with zipfile.ZipFile(zip_folder_path, 'r') as myzip:
            with myzip.open(filename) as pdf_file:
                pdf_reader = PyPDF2.PdfFileReader(pdf_file)
                text = ''
                for page_num in range(pdf_reader.numPages):
                    page = pdf_reader.getPage(page_num)
                    text += page.extractText()
                outfile.write(text)
                characters = set(text)
                vocab.update(characters)

# Process the validation PDF files
with open(output_file_val, "w", encoding="utf-8") as outfile:
    for filename in tqdm(pdf_files_val, total=len(pdf_files_val)):
        with zipfile.ZipFile(zip_folder_path, 'r') as myzip:
            with myzip.open(filename) as pdf_file:
                pdf_reader = PyPDF2.PdfFileReader(pdf_file)
                text = ''
                for page_num in range(pdf_reader.numPages):
                    page = pdf_reader.getPage(page_num)
                    text += page.extractText()
                outfile.write(text)
                characters = set(text)
                vocab.update(characters)

# Write the vocabulary to vocab.txt
with open(vocab_file, "w", encoding="utf-8") as vfile:
    for char in vocab:
        vfile.write(char + '\n')