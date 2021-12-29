import fitz
def readTextFromPDFDoc(doc):
    text=""
    for page in doc:
        text += str(page.get_text())
    return text

def readPDFFromStream(stream):
    return fitz.open(stream=stream, filetype="pdf")


class PreTraitedText:
    def removeReturnLine(self,text):
        return text.replace('\n',"").replace("\r"," ")

    def pretraited(self,text):
        return self.removeReturnLine(text)