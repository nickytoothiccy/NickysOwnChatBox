# Nick AI Chat Box V2.0 Desktop App
# added Image Generation Functionality
import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThread, pyqtSignal
from datetime import datetime
import os
import requests
import openai
import sys
from chatBoxMainScreen import Ui_MainWindow
from chatWizardScreen import Ui_WizardPage


class chatTask(QThread):
    finished = pyqtSignal(str)

    def __init__(self, chat_function, prompt):
        super(chatTask, self).__init__()
        self.chat_function = chat_function
        self.prompt = prompt

    def run(self):
        response = self.chat_function(self.prompt)
        self.finished.emit(response)


class chatBox(object):

    def __init__(self):
        self.main_win = QMainWindow()
        self.wiz_win = QDialog()
        self.ui = Ui_MainWindow()
        self.wizUI = Ui_WizardPage()
        self.ui.setupUi(self.main_win)
        # status bar object makes it easier to call later since it will be used repeatedly
        self.statusBar = self.ui.statusBar
        # link scroll bar to text edit
        self.ui.textEdit.setVerticalScrollBar(self.ui.responseScroll)
        # will incorporate this with PDF and TXT file upload
        self.chunkSize = 1000  # default value, can change due to accuracy
        self.chunks = None
        self.totalPages = None
        # Replace with the number of characters you want to keep
        self.trimSize = 2000
        # initialize Pre-Prompt
        self.prePrompt = ''
        self.temp = .1
        self.userInput = None
        self.token = 2000
        # set up picture generation resolution
        self.resolution = '1024x1024'
        # Connect the "Send" button to the send_message function
        self.ui.sendPushButton.clicked.connect(self.send_message)
        # If the user presses enter, it will send the message
        self.ui.lineEdit.returnPressed.connect(self.send_message)
        # Link Menu item to function
        self.ui.promptDesigner.triggered.connect(self.open_wizard)
        # link the image generate button to switch ui
        self.ui.imageGenerate.clicked.connect(self.openImage)
        # link to send image prompt button
        self.ui.send.clicked.connect(self.sendImage)
        # link to back to chat button
        self.ui.returnChat.clicked.connect(self.openChat)
        # save the chat or image
        self.ui.saveChat.triggered.connect(self.saveFile)
        # add pre-prompt if there is one
        with open('prePrompt.txt', 'r') as f:
            self.prePrompt = f.read()
        # add settings
        with open('temperature.txt', 'r') as f:
            self.temp = f.read()
        with open('token.txt', 'r') as f:
            self.token = f.read()
        # URL object
        self.url = None

    def show(self):
        # setup current widget
        self.ui.stackedWidget.setCurrentWidget(self.ui.chat)
        self.main_win.setFixedSize(1077, 602)
        self.main_win.show()

    def open_wizard(self):
        # Open Wizard pop up menu
        self.wizUI.setupUi(self.wiz_win)
        # Set the text to the saved pre_prompt
        self.wizUI.promptEdit.setText(self.prePrompt)
        # Set the max token and temperature
        self.wizUI.tempEdit.setText(str(self.temp))
        self.wizUI.tokenEdit.setText(str(self.token))
        self.wizUI.saveButton.clicked.connect(self.save_settings)
        self.wiz_win.show()

    def openImage(self):
        # Switch Views
        self.ui.stackedWidget.setCurrentWidget(self.ui.image)
        # Set the dimensions
        self.main_win.setFixedSize(1521, 1031)

    def openChat(self):
        # Switch Views
        self.ui.stackedWidget.setCurrentWidget(self.ui.chat)
        # Set the dimensions
        self.main_win.setFixedSize(1077, 602)

    def send_message(self):
        # Get user input from lineEdit
        self.userInput = self.ui.lineEdit.text()
        # Get current timestamp

        # Clear the QLineEdit
        self.ui.lineEdit.clear()
        # add pre prompt if available
        if self.prePrompt != '':
            # Get response from Chat GPT with user Pre-Prompt
            pre_prompt = self.prePrompt + "\n"
            # print a status to know if it is awaiting a message
            self.statusBar.showMessage('Loading Response.....')
            # Create and start the thread
            self.chat_task = chatTask(self.ChatGPT4Completion, pre_prompt + self.userInput)
            self.chat_task.finished.connect(self.on_chat_finished)
            # now start the chosen task
            self.chat_task.start()
        else:
            # Create and start the thread
            self.chat_task = chatTask(self.ChatGPT4Completion, self.userInput)
            self.chat_task.finished.connect(self.on_chat_finished)
            # now start the chosen task
            self.chat_task.start()

    def sendImage(self):
        # Get user input from textEdit
        self.userInput = self.ui.imageDesc.toPlainText()
        # Clear prompt space
        self.ui.imageDesc.clear()
        # print a status to know if it is awaiting a message
        self.statusBar.showMessage('Loading Response.....')
        # Create and start the thread
        self.chat_task = chatTask(self.dallE3Completion, self.userInput)
        self.chat_task.finished.connect(self.on_image_finished)
        # now start the chosen task
        self.chat_task.start()

    def save_settings(self):
        self.prePrompt = self.wizUI.promptEdit.toPlainText()
        self.temp = self.wizUI.tempEdit.text()
        self.token = self.wizUI.tokenEdit.text()
        # Save the response
        with open('prePrompt.txt', 'w') as w:
            w.write(self.prePrompt)
        # Save the settings
        with open('temperature.txt', 'w') as w:
            w.write(self.temp)
        with open('token.txt', 'w') as w:
            w.write(self.token)
        # Close Screen
        self.wiz_win.close()

    def saveFile(self):
        # check which mode the user is on
        # Chat tab
        if self.ui.stackedWidget.currentIndex() == 0:
            timestamp = datetime.now().strftime("%d-%m-%Y-%H_%M")
            convo = self.ui.textEdit.toPlainText()
            file, check = QFileDialog.getSaveFileName(None, "QFileDialog.getOpenFileName()",
                                                      "", "Text Files (*.txt)")
            print(file)
            with open(str(file), 'w') as w:
                print(convo)
                w.write(convo)
            self.statusBar.showMessage('save success')
        # # Image Tab
        # if self.ui.stackedWidget.currentIndex() == 1:
        #     file, check = QFileDialog.getSaveFileName(None, "QFileDialog.getOpenFileName()",
        #                                               "", "All Files (*);;PDF Files (*.pdf);;Text Files (*.txt)",
        #                                               options=QFileDialog.DontUseNativeDialog)
        #     if check:
        #         # Create the complete path to save the image
        #         print(file)
        #         save_path = file + '.png'
        #         # Save the image
        #         with open(save_path, 'wb') as f:
        #             f.write(self.url)
        #         file = file + '.png'
        #     else:
        #         self.statusBar.showMessage('save failed')

    def ChatGPT4Completion(self, prompt):
        message = [
            {"role": "user", "content": prompt}
        ]
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=message,
                temperature=float(self.temp),
                max_tokens=int(self.token),
                frequency_penalty=0.0
            )
            return response.choices[0].message.content
        except Exception as oops:
            return "GPT-4 error: %s" % oops

    def dallE3Completion(self, prompt):
        try:
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size=self.resolution
            )
            image_url = response['data'][0]['url']
            return image_url
        except Exception as oops:
            return 'fail:' % oops

    def on_chat_finished(self, gpt_response):
        # Set TimeStamp
        timestamp = datetime.now().strftime("%d-%m-%Y-%H:%M")
        # Update the QTextEdit to display the response
        # Trim the response, so it isn't printing a 10000 character question I be asking
        user_input = self.userInput[:self.trimSize]
        # Print response to screen
        self.ui.textEdit.append(f"{timestamp}\nUser: {user_input}\nGPT: {gpt_response}\n")
        # Show status message for 5 seconds
        self.statusBar.showMessage('Response Loaded', 5000)

    def on_image_finished(self, imageFileURL):
        # if the user broke some kind of rule place default image and tell user a message
        if imageFileURL[:4] == 'fail':
            save_path = 'Images/placeholder900x900.png'
            # Insert the image into the label
            pixmap = QPixmap(save_path)  # Create QPixmap object
            self.ui.dalleImage.setPixmap(pixmap)
            # set the warning message on the status bar
            self.statusBar.showMessage(imageFileURL)
        else:
            response = requests.get(imageFileURL)
            # Pre prompt to ensure good quality images
            # clear the text edit field
            self.ui.textEdit.clear()
            # ensure we get a good response
            if response.status_code == 200:
                self.url = imageFileURL
                print(self.url)
                # Extract the filename from the URL
                filename = 'Image File.png'
                # Create the complete path to save the image
                save_path = 'Images/' + filename
                # Save the image
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                # Insert the image into the label
                pixmap = QPixmap(save_path)  # Create QPixmap object
                self.ui.dalleImage.setPixmap(pixmap)
            else:
                print(f"Failed to download image. HTTP Error Code: {response.status_code}")
            # Show status message for 5 seconds
            self.statusBar.showMessage('Response Loaded', 5000)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    openai.api_key = os.environ.get('API_KEY')
    main_win = chatBox()
    main_win.show()
    sys.exit(app.exec_())
