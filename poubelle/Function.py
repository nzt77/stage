class Global:

    @staticmethod
    def Afficher(Texte):
        print(Texte)

    @staticmethod
    def Ajouter(a, b):
        return a + b

    @staticmethod
    def Soustraire(a, b):
        return a - b

    @staticmethod
    def Multiplier(a, b):
        return a * b

    @staticmethod
    def Diviser(a, b):
        if b != 0:
            return a / b
        else:
            return "ne peut pas diviser par 0"
