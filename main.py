import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class TranslationHelper(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        from wordtranslator1 import Ui_MainWindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.dictionary = {
            "English to Spanish": {"hello": "hola", "world": "mundo", "cat": "gato", "dog": "perro", "house": "casa",
        "car": "coche", "food": "comida", "water": "agua", "friend": "amigo", "love": "amor"},
            "English to French": {"hello": "bonjour", "world": "monde", "cat": "chat", "dog": "chien", "house": "maison",
        "car": "voiture", "food": "nourriture", "water": "eau", "friend": "ami", "love": "amour"},
            "English to German": {"hello": "hallo", "world": "welt", "cat": "katze", "dog": "hund", "house": "haus",
        "car": "auto", "food": "essen", "water": "wasser", "friend": "freund", "love": "liebe"},
            "English to Italian": {"hello": "ciao", "world": "mondo", "cat": "gatto", "dog": "cane", "house": "casa",
        "car": "macchina", "food": "cibo", "water": "acqua", "friend": "amico", "love": "amore"},
            "English to Japanese": {"hello": "こんにちは", "world": "世界", "cat": "猫", "dog": "犬", "house": "家",
        "car": "車", "food": "食べ物", "water": "水", "friend": "友達", "love": "愛"},
            "English to Georgian": {"hello": "გამარჯობა", "world": "მსოფლიო", "cat": "კატა", "dog": "ძაღლი", "house": "სახლი",
        "car": "მანქანა", "food": "საკვები", "water": "წყალი", "friend": "მეგობარი", "love": "სიყვარული"},
            "Georgian to English": {"გამარჯობა": "hello", "მსოფლიო": "world", "კატა": "cat", "ძაღლი": "dog", "სახლი": "house",
        "მანქანა": "car", "საკვები": "food", "წყალი": "water", "მეგობარი": "friend", "სიყვარული": "love"},
            "French to English": {"bonjour": "hello", "monde": "world", "chat": "cat", "chien": "dog", "maison": "house",
        "voiture": "car", "nourriture": "food", "eau": "water", "ami": "friend", "amour": "love"},
            "German to English": {"hallo": "hello", "welt": "world", "katze": "cat", "hund": "dog", "haus": "house",
        "auto": "car", "essen": "food", "wasser": "water", "freund": "friend", "liebe": "love"}
        }

        self.favoritesModel = QStandardItemModel(0, 3)
        self.favoritesModel.setHorizontalHeaderLabels(['ენები', 'სიტყვა', 'თარგმანი'])
        self.ui.favoritesTableView.setModel(self.favoritesModel)
        self.ui.favoritesTableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.ui.favoritesTableView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.ui.favoritesTableView.horizontalHeader().setStretchLastSection(True)

        self.ui.translateButton.clicked.connect(self.translate_word)
        self.ui.removeFavoriteButton.clicked.connect(self.remove_favorite)

    def translate_word(self):
        word = self.ui.lineEdit.text().strip().lower()
        language_pair = self.ui.languageComboBox.currentText()

        if not word:
            self.ui.statusLabel.setText("გთხოვთ, ჩაწერეთ სიტყვა")
            self.ui.translationLabel.setText("")
            return

        translation = self.dictionary.get(language_pair, {}).get(word, None)
        if translation:
            self.ui.translationLabel.setText(translation)
            self.ui.statusLabel.setText("")

            if self.ui.rememberCheckBox.isChecked():
                if not self.is_in_favorites(language_pair, word):
                    self.add_to_favorites(language_pair, word, translation)
                else:
                    self.ui.statusLabel.setText("ეს სიტყვა უკვე დამატებულია ფავორიტებში.")
            else:
                self.ui.statusLabel.setText("")

        else:
            self.ui.translationLabel.setText("თარგმნა ვერ მოიძებნა.")
            self.ui.statusLabel.setText("")

    def is_in_favorites(self, language_pair, word):
        for row in range(self.favoritesModel.rowCount()):
            lp_item = self.favoritesModel.item(row, 0)
            word_item = self.favoritesModel.item(row, 1)
            if lp_item.text() == language_pair and word_item.text() == word:
                return True
        return False

    def add_to_favorites(self, language_pair, word, translation):
        row = self.favoritesModel.rowCount()
        self.favoritesModel.insertRow(row)
        self.favoritesModel.setItem(row, 0, QStandardItem(language_pair))
        self.favoritesModel.setItem(row, 1, QStandardItem(word))
        self.favoritesModel.setItem(row, 2, QStandardItem(translation))
        self.ui.statusLabel.setText("სიტყვა დამატებულია ფავორიტებში.")

    def remove_favorite(self):
        selection = self.ui.favoritesTableView.selectionModel().selectedRows()
        if selection:
            index = selection[0]
            self.favoritesModel.removeRow(index.row())
            self.ui.statusLabel.setText("სიტყვა წაიშალა ფავორიტებიდან.")
        else:
            self.ui.statusLabel.setText("გთხოვთ, მონიშნეთ სიტყვა წასაშლელად.")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TranslationHelper()
    window.show()
    sys.exit(app.exec_())
