from action import *
import sys

class Main(Edit):
    def __init__(self):
        File.__init__(self)
        self.set_file_actions()
        self.set_edit_actions()
    
    def set_file_actions(self):
        self.action_new.triggered.connect(self.run_new)
        self.action_open.triggered.connect(self.run_open)
        self.action_save.triggered.connect(self.run_save)
        self.action_save_as.triggered.connect(self.run_save_as)
        self.action_exit.triggered.connect(self.close)
    
    def set_edit_actions(self):
        self.action_undo.triggered.connect(self.run_undo)
        self.action_redo.triggered.connect(self.run_redo)
        self.action_cut.triggered.connect(self.run_cut)
        self.action_copy.triggered.connect(self.run_copy)
        self.action_paste.triggered.connect(self.run_paste)
        self.action_del.triggered.connect(self.run_del)
        self.action_find.triggered.connect(self.run_find)
        # self.action_next_find.triggered.connect(self.run_next_find)
        # self.action_change.triggered.connect(self.run_change)
        # self.action_move.triggered.connect(self.run_move)
        # self.action_all.triggered.connect(self.run_all)
        # self.action_time.triggered.connect(self.run_time)

if __name__ == '__main__':
    app=QApplication(sys.argv)
    main=Main()
    main.show()
    sys.exit(app.exec_())

