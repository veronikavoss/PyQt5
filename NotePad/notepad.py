from action import *
import sys

class Main(Edit):
    def __init__(self):
        File.__init__(self)
        self.set_file_actions()
        # self.set_edit_actions()
    
    def set_file_actions(self):
        self.action_new.triggered.connect(self.run_new_file)
        self.action_open.triggered.connect(self.run_open_file)
        self.action_save.triggered.connect(self.run_save)
        # self.action_save_as.triggered.connect(self.run_save_as)
        self.action_exit.triggered.connect(self.close)
    
    def set_edit_actions(self):
        self.action_undo.triggered.connect(lambda:self.plainTextEdit.undo())
        self.action_redo.triggered.connect(lambda:self.plainTextEdit.redo())
        self.action_cut.triggered.connect(lambda:self.plainTextEdit.cut())
        self.action_copy.triggered.connect(lambda:self.plainTextEdit.copy())
        self.action_paste.triggered.connect(lambda:self.plainTextEdit.paste())
        self.action_del.triggered.connect(self.run_del)
        self.action_find.triggered.connect(self.run_find)
        # self.action_next_find.triggered.connect(self.run_next_find)
        # self.action_change.triggered.connect(self.run_change)
        # self.action_move.triggered.connect(self.run_move)
        self.action_all.triggered.connect(lambda:self.plainTextEdit.all())
        # self.action_time.triggered.connect(self.run_time)

if __name__ == '__main__':
    app=QApplication(sys.argv)
    main=Main()
    main.show()
    sys.exit(app.exec_())

