import glob
import os
import PyPDF2
import md2pdf.core as md2pdf


def convert_md_to_pdf(dirname):
    original_dir = os.getcwd()

    os.chdir(dirname)
    for file in glob.glob('*.md'):
        pdf_list = glob.glob('*.pdf')
        new_filename = file.replace('.md', '.pdf')
        if new_filename not in pdf_list and new_filename.lower().replace(' ', '-') not in pdf_list:
            md2pdf.md2pdf(new_filename, md_file_path=file)

    os.chdir(original_dir)


def merge_pdfs(dirname, output):
    original_dir = os.getcwd()
    files = []
    pdf_writer = PyPDF2.PdfFileWriter()

    os.chdir(dirname)
    for file in glob.glob('*.pdf'):
        if file != output:
            files.append(file)

    files.sort(key=lambda x: str(x.lower()).replace(' ', '-'))
    for file in files:
        pdf_reader = PyPDF2.PdfFileReader(file)

        for page in range(pdf_reader.getNumPages()):
            # Add each page to the writer object
            pdf_writer.addPage(pdf_reader.getPage(page))

    # Write out the merged PDF
    with open(output, 'wb') as out:
        pdf_writer.write(out)

    os.chdir(original_dir)


if __name__ == '__main__':
    notes_dir = os.environ.get('MERGE_PDFS_DIRECTORY')
    convert_md_to_pdf(notes_dir)
    merge_pdfs(notes_dir, 'notes.pdf')
