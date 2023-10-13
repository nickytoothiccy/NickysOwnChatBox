from chatNicky import chatBox
from multiprocessing import Process, freeze_support, Queue
from docx import Document
from PyQt5.QtWidgets import *
from nltk.tokenize import sent_tokenize
import nltk
from io import StringIO
from advancedFeatures import Ui_docsAndDiag
import sys
import fitz
import openai
import os
import subprocess
from PyQt5.QtCore import QThread, pyqtSignal
from time import sleep


class chatTask(QThread):
    finished = pyqtSignal(str)

    def __init__(self, chat_function, prompt):
        super(chatTask, self).__init__()
        self.chat_function = chat_function
        self.prompt = prompt

    def run(self):
        response = self.chat_function(self.prompt)
        self.finished.emit(response)


class advancedFeatures:

    def __init__(self):
        self.gptResponse = None
        self.chat_task = None
        self.gui_task = None
        self.advWin = QTabWidget()
        self.ui = Ui_docsAndDiag()
        self.ui.setupUi(self.advWin)
        self.userInput = None
        # Set up url for mermaid js editor
        self.urlMermaid = "https://mermaid.live/edit#pako:eNo9ijEOgCAQBL9itvYF1PoC22su3qEkAgaPwhD_LoWxm5lMw5pF4UCEEVFL5" \
                          "CBdG6VhINiuUQmuo6jnehiB0tNXrpaXO61wno9LR9RT2HQKvBWOcFbqH2cJlst3Pi9_Pyc9"
        # Define constants for Intelligent PDF reader
        nltk.download('punkt', quiet=True)
        self.chunkSize = 2500  # default value, can change due to accuracy
        self.chunks = None
        self.prePrompt = None
        self.totalPages = None
        self.FinalPath = None
        self.pdfObject1 = None
        # Define Object signals
        self.ui.diagGenerate.clicked.connect(self.diagramGenerator)

    def show(self):
        # setup current widget
        self.advWin.show()

    def fileUpload(self):
        file, check = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()",
                                                  "", "PDF Files (*.pdf);;Word Files (*.docx)")
        # choose a file. no checks in place in case wrong file is picked
        if check:
            self.FinalPath = file
            self.read_PDF(self.FinalPath)

    def read_pdf_to_chunks(self, context):
        chunks = []  # set class variable to empty array
        current_chunk = StringIO()
        current_size = 0
        sentences = sent_tokenize(context)
        for sentence in sentences:
            sentence_size = len(sentence)
            if sentence_size > self.chunkSize:
                while sentence_size > self.chunkSize:
                    chunk = sentence[:self.chunkSize]
                    chunks.append(chunk)
                    sentence = sentence[self.chunkSize:]
                    sentence_size -= self.chunkSize
                    current_chunk = StringIO()
                    current_size = 0

            if current_size + sentence_size < self.chunkSize:
                current_chunk.write(sentence)
                current_size += sentence_size
            else:
                chunks.append(current_chunk.getvalue())
                current_chunk = StringIO()
                current_chunk.write(sentence)
                current_size = sentence_size
        if current_chunk:
            chunks.append(current_chunk.getvalue())
        return chunks

    def read_pdf(self, file_path):
        context = ""
        with fitz.open(file_path) as pdf_file:
            # Get the number of pages in the PDF file
            num_pages = pdf_file.page_count
            # Loop through each page in the PDF file
            for page_num in range(num_pages - 1):
                # Get the current page
                page = pdf_file[page_num]
                # Get the text from the current page
                page_text = page.get_text()
                # Append the text to context
                context += page_text
        # Set PDF to Class variable
        # Get the file name from the file path
        file_name = os.path.basename(self.FinalPath)
        # self.ui.label.setText(file_name)  # Set the label text to the PDF title
        return context

    def summarize_PDF(self):
        # split the PDF chunks
        chunks = self.read_pdf_to_chunks()
        summaries = []
        for chunk in chunks:
            print('begin')
            prompt = 'Please summarize the following document:' + "\n"
            summary = self.ChatGPT4Completion(prompt + chunk)
            if summary.startswith('GPT-4 error:'):
                continue
            summaries.append(summary)
        # Combine all summaries into one string
        print(summaries)
        all_summaries = ' '.join(summaries)

        # Save to a text file in the root folder
        with open('All_Summaries.txt', 'w') as f:
            f.write(all_summaries)
        # Combine all summaries into one string
        print('all summarized')
        exit()

    def diagramGenerator(self):
        prePrompt = 'The only answers you are allowed to give is to translate whatever the user inputs into MermaidJS syntax. ' \
                    'never tell me that you cannot do it. put any item you dont know in a function block by itself.' + '\n'
        self.userInput = self.ui.diagPrompt.toPlainText()
        self.ui.diagPrompt.clear()
        # add the Pre prompt and user input together
        userInput = prePrompt + self.userInput
        # Create and start the thread
        self.chat_task = chatTask(ChatGPT4Completion, userInput)
        self.chat_task.finished.connect(self.onChatFinished)
        # now start the chosen task
        self.chat_task.start()

    def onChatFinished(self, gptResponse):
        # set variable to house modified mermaid response
        modifiedLines = []
        # trim the response to remove 'mermaid', replace ` with ', and remove any white space
        self.gptResponse = gptResponse.replace("mermaid", "")
        self.gptResponse = self.gptResponse.replace("`", "")
        self.gptResponse = self.gptResponse.replace("LR", "TD")
        # split the response into lines
        lines = self.gptResponse.splitlines()
        nonEmptyLines = [line for line in lines if line.strip() != ""]
        # format the response to be able to send to mermaid
        for line in nonEmptyLines:
            if line == "'''":
                modLineTemp = line
            else:
                modLineTemp = line + '; '
            modifiedLines.append(modLineTemp)
        formattedResponse = '\n'.join(modifiedLines)
        formattedResponse = formattedResponse.replace("\n", "")
        # it is not done yet, chat GPT won't put the correct syntax
        loadVisual(formattedResponse)


def ChatGPT4Completion(prompt):
    message = [
        {"role": "user", "content": prompt}
    ]
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=message,
            temperature=.1,
            max_tokens=5000,
            frequency_penalty=0.0
        )
        return response.choices[0].message.content
    except Exception as oops:
        return "GPT-4 error: %s" % oops


def loadVisual(script):
    print('start')
    # start the subprocess
    proc = subprocess.Popen([sys.executable, "niceguiExcecution.py", script], cwd=sys.path[0])
    # Let it run for some time (e.g., 5 seconds)\
    sleep(10)
    print('done')
    # terminate subprocess
    proc.terminate()

if __name__ == "__main__":

    # start QT application
    app = QApplication(sys.argv)
    # get API key
    openai.api_key = os.environ.get('API_KEY')
    #initialize the class
    main_win = advancedFeatures()
    # call the show function
    main_win.show()
    sys.exit(app.exec_())

