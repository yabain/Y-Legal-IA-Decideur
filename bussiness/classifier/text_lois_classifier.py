class TextLoiClassifier:
    """Algorithme de classification qui dit si un texte est un text de loi ou pas"""

    def __init__(self):
        self.model=None
        self.loadModel();

    def loadModel(self):
        pass

    def predict(self,text):
        #self.model.predict(text)
        return {"percent":1,"prediction":"yes"}