from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QGridLayout,QInputDialog,QTableView,QLCDNumber
from PyQt5.QtSql import QSqlDatabase,QSqlQuery,QSqlTableModel
from PyQt5.QtCore import Qt,QTime,QTimer
import sys


class CRUD(QWidget):
    def __init__(self):
        super().__init__()
        self.iniUI()
    def iniUI(self):
        
        createDBConnection()
        
        time = QTime.currentTime()
        text = time.toString('hh:mm:ss')
        self.lCD_time = QLCDNumber(self)
        self.lCD_time.setDigitCount(8)     # change the number of digits displayed from 5 to 8
        self.lCD_time.setSegmentStyle(QLCDNumber.Flat)
        self.lCD_time.setStyleSheet("QLCDNumber {color: blue;}") 
        self.lCD_time.setMinimumHeight(40) # change the font size to bigger        
        self.lCD_time.display(text)        
               
        # refresh timer to reset time in lCD_time
        self.refreshTimer = QTimer(self)
        self.refreshTimer.start(1000) # Starts or restarts the timer with a timeout of duration msec milliseconds.
        self.refreshTimer.timeout.connect(self.show_Time) # This signal is emitted when the timer times out.       
       
        bt_add = QPushButton("Add")
        bt_del = QPushButton("Delete")
        bt_sho = QPushButton("Show")        
        
        layout = QGridLayout()
        layout.addWidget(self.lCD_time)
        layout.addWidget(bt_add)
        layout.addWidget(bt_del)
        layout.addWidget(bt_sho)        
        
        bt_add.clicked.connect(self.add_records)
        bt_del.clicked.connect(self.del_records)
        bt_sho.clicked.connect(self.show_records)            

        self.tableView = QTableView(self)
        self.tableView.setObjectName("tableView")
        
        layout.addWidget(self.tableView)
        
        self.setLayout(layout)
        self.setWindowTitle("CRUD sample")
        self.setGeometry(200,300,350,450) # x,y, width, height
        self.show()
        
        
    def add_records(self):
        text, ok = QInputDialog.getText(self, "Dialog title", "Enter your  ID", )
        if ok :
            print("Entered ",text)
            name = str(text)
            emp_id = str(text)
            
#             createDBConnection()
            query=QSqlQuery()
            query.prepare("INSERT INTO employee1 (emp_id, name) "
                          "VALUES (:emp_id, :name)")

            query.bindValue(":emp_id", emp_id)
            query.bindValue(":name", name)
            
            if query.exec_():
                print("add_records Successful")
                self.show_records() 
            else:
                print("add_records Error: ", query.lastError().text())
                
                
    def show_records(self):  
#         createDBConnection()
        query=QSqlQuery()
        query.exec_("SELECT * from employee1")
        if query.exec_():
            print("show_records Successful")
        else:
            print("show_records Error: ", query.lastError().text())
        while query.next():
            print ("query show_records " , query.value(0),query.value(1) )
        model = QSqlTableModel() 
        self.show_records_View("Title",model)
        
    def del_records(self):  
#         createDBConnection()
        query=QSqlQuery()
        query.exec_("DELETE from employee1")
        if query.exec_():
            print("del_records Successful")
            self.show_records() 
        else:
            print("del_records Error: ", query.lastError().text())

    def show_records_View(self,title, model):
        
        model.setTable('employee1')
        model.setEditStrategy(QSqlTableModel.OnFieldChange)
        model.select()
        model.setHeaderData(0, Qt.Horizontal,"emp_id")
        model.setHeaderData(1, Qt.Horizontal,"name")
    
        self.tableView.setModel(model)
        self.tableView.setWindowTitle(title)
        return self.tableView
    
    def show_Time(self):
        time = QTime.currentTime()
#         print(time)
        text = time.toString('hh:mm:ss')
        self.lCD_time.display(text)
        

def createDBConnection():
    db = QSqlDatabase.addDatabase("QSQLITE") 
    db.setDatabaseName('test.db')
    if db.open():
        print('created db file!')
        query = QSqlQuery()
        query.exec_("create table IF NOT EXISTS employee1 (emp_id int primary key, "
                "name varchar(20) )")
        print('created table employee')
        
        query.exec_("SELECT row_id,emp_id,name from employee1")
        print('initial data in employee')
    else:
        print('Unable to create db file!')
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = CRUD()
    sys.exit(app.exec_())
    