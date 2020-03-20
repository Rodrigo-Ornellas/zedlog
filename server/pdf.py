# from pyPdf import PdfFileReader
# from StringIO import StringIO

# importing required modules 
import PyPDF2 
import tabula

# convert PDF into CSV file
tabula.convert_into("DPVesselSchedule3.pdf", "output3.csv", output_format="csv", pages='all')

if False:
    # creating a pdf file object 
    pdfFileObj = open('DPVesselSchedule2.pdf', 'rb') 

    # creating a pdf reader object 
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 

    # printing number of pages in pdf file 
    print('number of pages: {}'.format(pdfReader.numPages))
    pages = pdfReader.numPages

    # creating a page object 
    for i in range(pages):
        try:
            print(' ')
            print('page {}'.format(i))
            # pageArr.append(pdfReader.getPage(pag))
            # extracting text from page 
            print('=================================')

            pageObj = pdfReader.getPage(i)
            # print(pageObj.extractText())

            # Extracting text from page
            # And splitting it into chunks of lines
            text = pageObj.extractText().split("  ")        
            print('number of lines > {}'.format(len(text)))

            for i in range(len(text)):
                    # Printing the line
                    # Lines are seprated using "\n"
                    print(text[i],end="\n\n\n")


            print('*********************************')
            print(' ')
        except:
            print('ERROOOORRRR')

    # closing the pdf file object 
    pdfFileObj.close() 
