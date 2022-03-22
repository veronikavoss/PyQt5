from asyncio import events
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
import os

current_path=os.path.dirname(os.path.abspath(__file__))
image_path=os.path.join(current_path,'image')

UiClass=uic.loadUiType(os.path.join(current_path,'notepad.ui'))[0]
FindUi=os.path.join(current_path,'find.ui')

class FindWindow(QDialog):
    def __init__(self,parent):
        QDialog.__init__(self,parent)
        uic.loadUi(FindUi,self)
        self.show()
        
        self.parent_text=parent.plainTextEdit
        self.cursor=parent.plainTextEdit.textCursor()
        self.next_button.clicked.connect(self.set_next_button)
        self.cancel_button.clicked.connect(self.set_cancel_button)
    
    def keyReleaseEvent(self,event):
        print(self.line_edit.text())
        if self.line_edit.text():
            self.next_button.setEnabled(True)
        else:
            self.next_button.setEnabled(False)
    
    def set_cursor(self):
        print(self.cursor.selectionStart(),self.cursor.selectionEnd())
    
    def set_next_button(self):
        print('next')
    
    def set_cancel_button(self):
        self.close()

class File(QMainWindow,UiClass):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.file_name='제목 없음'
        self.setWindowIcon(QIcon(os.path.join(image_path,'notepad_icon.png')))
        self.setWindowTitle(f'{self.file_name} - 메모장')
        self.plainTextEdit.clear()
        self.current_text_edit=self.plainTextEdit.toPlainText()
        self.plainTextEdit.textChanged.connect(self.text_changed)
        self.text_changed=False
    
    def text_changed(self):
        if type(self.file_name)==str:
            if self.current_text_edit!=self.plainTextEdit.toPlainText():
                self.setWindowTitle(f'*{os.path.basename(self.file_name)} - 메모장')
                self.text_changed=True
            else:
                self.setWindowTitle(f'{os.path.basename(self.file_name)} - 메모장')
                self.text_changed=False
    
    def set_new_file(self):
        self.plainTextEdit.clear()
        self.file_name='제목 없음'
        self.setWindowTitle(f'{os.path.basename(self.file_name)} - 메모장')
        self.current_text_edit=self.plainTextEdit.toPlainText()
        self.text_changed=False
    
    def set_open_file(self):
        with open(self.file_name[0],'r',encoding='ansi') as r:
            self.plainTextEdit.setPlainText(r.read())
            self.current_text_edit=self.plainTextEdit.toPlainText()
            self.current_file_name=self.file_name[0]
            self.file_name=os.path.basename(self.file_name[0])
            self.setWindowTitle(f'{self.file_name} - 메모장')
            self.text_changed=False
    
    def set_save_file(self):
        with open(self.file_name[0],'w',encoding='ansi') as w:
            w.write(self.plainTextEdit.toPlainText())
            self.current_text_edit=self.plainTextEdit.toPlainText()
            self.text_changed()
    
    def set_save_messagebox(self):
        messagebox=QMessageBox()
        messagebox.setWindowTitle('메모장')
        if self.file_name=='제목 없음':
            messagebox.setText(f'변경 내용을 {self.file_name}에 저장하시겠습니까?')
        else:
            messagebox.setText(f'변경 내용을 {self.current_file_name}에 저장하시겠습니까?')
        messagebox.addButton('저장',QMessageBox.YesRole)
        messagebox.addButton('저장 안 함',QMessageBox.NoRole)
        messagebox.addButton('취소',QMessageBox.RejectRole)
        self.get_button_event=messagebox.exec_()
    
    def set_close(self,event):
        if self.text_changed:
            self.set_save_messagebox()
            if self.get_button_event==0:
                if self.file_name=='제목 없음':
                    self.file_name=QFileDialog.getSaveFileName(self,'다른 이름으로 저장',filter='텍스트 문서 (*.txt);;모든 파일 (*.*)')
                    if self.file_name[0]:
                        self.setWindowTitle(f'{os.path.basename(self.file_name[0])} - 메모장')
                        self.set_save_file()
                    else:
                        self.file_name='제목 없음'
                        event.ignore()
                else:
                    self.run_save()
            elif self.get_button_event==2:
                event.ignore()
    
    def run_new(self):
        if self.file_name=='제목 없음':
            if self.text_changed:
                self.set_save_messagebox()
                if self.get_button_event==0:
                    self.run_save_as()
                elif self.get_button_event==1:
                    self.plainTextEdit.clear()
        else:
            if self.text_changed:
                self.set_save_messagebox()
                if self.get_button_event==0:
                    self.run_save()
                    self.set_new_file()
                elif self.get_button_event==1:
                    self.set_new_file()
            else:
                self.set_new_file()
    
    def run_open(self):
        if self.text_changed:
            self.set_save_messagebox()
            if self.get_button_event==0:
                if self.file_name=='제목 없음':
                    self.file_name=QFileDialog.getSaveFileName(self,'다른 이름으로 저장',filter='텍스트 문서 (*.txt);;모든 파일 (*.*)')
                    if self.file_name[0]:
                        self.setWindowTitle(f'{os.path.basename(self.file_name[0])} - 메모장')
                        self.set_save_file()
                        self.file_name=QFileDialog.getOpenFileName(self,'열기',filter='텍스트 문서 (*.txt);;모든 파일 (*.*)')
                        if self.file_name[0]:
                            self.set_open_file()
                        else:
                            self.file_name='제목 없음'
                else:
                    self.run_save()
                    self.file_name=QFileDialog.getOpenFileName(self,'열기',filter='텍스트 문서 (*.txt);;모든 파일 (*.*)')
                    if self.file_name[0]:
                        self.set_open_file()
            elif self.get_button_event==1:
                if self.file_name=='제목 없음':
                    self.file_name=QFileDialog.getOpenFileName(self,'열기',filter='텍스트 문서 (*.txt);;모든 파일 (*.*)')
                    if self.file_name[0]:
                        self.set_open_file()
                    else:
                        self.file_name='제목 없음'
                else:
                    self.file_name=QFileDialog.getOpenFileName(self,'열기',filter='텍스트 문서 (*.txt);;모든 파일 (*.*)')
                    if self.file_name[0]:
                        self.set_open_file()
            elif self.get_button_event==2:
                return
            
        else:
            if self.file_name=='제목 없음':
                self.file_name=QFileDialog.getOpenFileName(self,'열기',filter='텍스트 문서 (*.txt);;모든 파일 (*.*)')
                if self.file_name[0]:
                    self.set_open_file()
                    self.text_changed=False
                    print(self.text_changed)
                else:
                    self.file_name='제목 없음'
            else:
                self.file_name=QFileDialog.getOpenFileName(self,'열기',filter='텍스트 문서 (*.txt);;모든 파일 (*.*)')
                if self.file_name[0]:
                    self.set_open_file()
                    self.text_changed=False
    
    def run_save(self):
        if self.file_name=='제목 없음':
            self.file_name=QFileDialog.getSaveFileName(self,'저장',filter='텍스트 문서 (*.txt);;모든 파일 (*.*)')
            if self.file_name[0]:
                self.setWindowTitle(f'{os.path.basename(self.file_name[0])} - 메모장')
                self.set_save_file()
            else:
                self.file_name='제목 없음'
        else:
            if self.file_name[0]:
                self.set_save_file()
    
    def run_save_as(self):
        if self.file_name=='제목 없음':
            self.file_name=QFileDialog.getSaveFileName(self,'다른 이름으로 저장',filter='텍스트 문서 (*.txt);;모든 파일 (*.*)')
            if self.file_name[0]:
                self.setWindowTitle(f'{os.path.basename(self.file_name[0])} - 메모장')
                self.set_save_file()
            else:
                self.file_name='제목 없음'
        else:
            self.file_name=QFileDialog.getSaveFileName(self,'다른 이름으로 저장',filter='텍스트 문서 (*.txt);;모든 파일 (*.*)')
            if self.file_name[0]:
                self.set_save_file()
    
    def closeEvent(self,event):
        self.set_close(event)

class Edit(File):
    def run_undo(self):
        self.plainTextEdit.undo()
    def run_redo(self):
        self.plainTextEdit.redo()
    def run_cut(self):
        self.plainTextEdit.cut()
    def run_copy(self):
        self.plainTextEdit.copy()
    def run_paste(self):
        self.plainTextEdit.paste()
    def run_del(self):
        QTextCursor.clearSelection(self.plainTextEdit)
    def run_find(self):
        FindWindow(self)
    # def run_next_find(self):
    #     self.plainTextEdit.()
    # def run_(self):
    #     self.plainTextEdit.()
    # def run_(self):
    #     self.plainTextEdit.()
    # def run_(self):
    #     self.plainTextEdit.()
    # def run_(self):
    #     self.plainTextEdit.()

