# from pyPdf import PdfFileReader
# from StringIO import StringIO
import pyPdf


from StringIO import StringIO


def getPDFContent():
    path = 'DPVesselSchedule.pdf'
    content = ""
    num_pages = 2
    p = file(path, "rb")
    pdf = pyPdf.PdfFileReader(p)
    for i in range(0, num_pages):
        content += pdf.getPage(i).extractText() + "\n"
    content = " ".join(content.replace(u"\xa0", " ").strip().split())
    return content


# f = open('test.txt', 'w')
# pdfl = StringIO(getPDFContent(
#     "DPVesselSchedule.pdf").encode("ascii", "ignore"))
# for line in pdfl:
#     f.write(line)

# f.close()


# def get_pdf_content_lines(pdf_file_path):
#     with open(pdf_file_path) as f:
#         pdf_reader = PdfFileReader(f)
#         for page in pdf_reader.pages:
#             for line in page.extractText().splitlines():
#                 yield line


# print('started!!!')
# for pline in get_pdf_content_lines('DPVesselSchedule.pdf'):
#     print(pline)


# Read each line of the PDF
pdfContent = StringIO(getPDFContent("test.pdf").encode("ascii", "ignore"))
for line in pdfContent:
    print(line)
