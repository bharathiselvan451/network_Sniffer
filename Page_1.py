from PySide6.QtWidgets import QApplication, QPushButton, QFrame, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QMessageBox, QComboBox, QTableWidget, QTableWidgetItem, QHeaderView, QTableWidgetItem
from PySide6.QtCore import Qt, QSize
import Scan
import Sniffer
import query
import threading

class firstpage(QWidget):
    button_layout = QVBoxLayout()
    line = ""
    devices = {}
    def __init__(self):
        super().__init__()
        self.resize(700,250)
        self.setWindowTitle("Network Scanner")
        #self.setGeometry(600, 600, 600, 600)
        button1 = QPushButton("Scan the network")
        button1.setStyleSheet("background-color : white; border-width: 15px; border-color: beige; min-width: 6em; color : black")
        button1.clicked.connect(self.Find_devices)
        #button1.setGeometry(100, 100, 600, 400)
        #sbutton1.setFixedSize(QSize(100, 50))
        #Sub_layout1 = QHBoxLayout()
        self.button_layout.addWidget(button1)
        #self.button_layout.addStretch(5)
        self.button_layout.setAlignment(button1,Qt.AlignCenter)
        #Sub_layout1.setAlignment(button1,Qt.AlignVCenter)
        #self.button_layout.addLayout(button_layout)
        
        button2 = QPushButton("Device History")
        button2.clicked.connect(self.Previous_devices)
        button2.setStyleSheet("background-color : white; border-width: 15px; border-color: beige; min-width: 6em; color : black")
        button2.adjustSize()
        #sbutton1.setFixedSize(QSize(100, 50))
        #Sub_layout1 = QHBoxLayout()
        self.button_layout.addWidget(button2)
        #self.button_layout.addStretch(5)
        self.button_layout.setAlignment(button2,Qt.AlignCenter)
        

        self.setLayout(self.button_layout)

    def Find_devices(self):
        dict = Scan.scanner()
        self.devices = dict
        print(self.devices)
        sub_layout2 = QHBoxLayout()
        label = QLabel("Enter the number of packets to capture :")
        label.setStyleSheet("color : black")
        self.line = QLineEdit()
        self.line.setStyleSheet("background-color : black; border-width: 15px; border-color: beige; min-width: 6em; color : white")
        self.button_layout.addWidget(label)
        self.button_layout.addWidget(self.line)
        self.button_layout.setAlignment(label,Qt.AlignCenter)
        self.button_layout.setAlignment(self.line,Qt.AlignCenter)
        #self.setGeometry(600, 600, 600, 600)
        #self.button_layout.addStretch(1)
        for key, value in dict.items():
           device = query.search_device(key)
           Button = ""
           if(device==None):
               Button = QPushButton(str(value[1])+" "+str(key))
               Button.setStyleSheet("background-color : white; border-width: 15px; border-color: beige; min-width: 6em; color : black")
           else:
               Button = QPushButton(device.Device_name)
               Button.setStyleSheet("background-color : white; border-width: 15px; border-color: beige; color : black")
               
           
           Button.pressed.connect(lambda val=str(key): self.modo(val))
           sub_layout2.addWidget(Button)
           Button.setGeometry(20, 15, 10, 40) 
           #self.button_layout.setAlignment(Button,Qt.AlignBottom)
           sub_layout2.setAlignment(Button,Qt.AlignVCenter)
        
        self.button_layout.addLayout(sub_layout2)
        #dict.clear()

    def modo(self,mac):
           ip = self.devices[mac][1]

     
           a = int(self.line.text())
           
           if(query.search(mac)):
              self.user_input_1(mac,ip,a)
           else:
              device = query.search_device(mac)
              Sniffer.algo(device.Device_name,device.vendour,mac,ip,a)
       
            #print(e)

       
    
      
       

    def Previous_devices(self):
        devices = query.all()
        print(len(devices))
        Layout = QVBoxLayout()
        table = QTableWidget()
        table.setGeometry(600, 600, 600, 600)
        table.setRowCount(len(devices))
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels(["Device name", "Mac address", "IP address", "Vendour", "Files", "    "])

        table.setStyleSheet("background-color : white; border-width: 15px; border-color: beige; color : black")

        header = table.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)

        i = 0
        for device in devices:
            Devicename = QTableWidgetItem(device.Device_name)
            MACaddress = QTableWidgetItem(device.MAC_address)
            IPaddress = QTableWidgetItem(device.IP_address)
            Vendour = QTableWidgetItem(device.vendour)
            Files = QTableWidgetItem(device.File_name)
            Button = QPushButton("Delete")
            Button.setStyleSheet("background-color : white; border-width: 15px; border-color: beige; min-width: 6em; color : black")
            Button.pressed.connect(lambda val=str(device.MAC_address): query.delete(val))
            #delete = QTableWidgetItem(Button)
            table.setItem(i,0,Devicename)
            table.setItem(i,1,MACaddress)
            table.setItem(i,2,IPaddress)
            table.setItem(i,3,Vendour)
            table.setItem(i,4,Files)
            table.setCellWidget(i,5,Button)
            i = i+1



            #Label = QLabel(device.Device_name+" "+device.MAC_address+" "+device.IP_address+" "+device.File_name+" "+device.vendour)
            #Label = QLabel("Device name: "+device.Device_name+" Mac Address: "+device.MAC_address+" IP address: "+device.IP_address+" Vendour: "+device.vendour+" Files: "+device.File_name)
        Layout.addWidget(table)
        self.wid = QWidget()
        self.wid.resize(700, 250)
        self.wid.setWindowTitle('Devices')
        self.wid.setLayout(Layout)
        self.wid.show()

    def user_input_1(self,mac,ip,a):
        label = QLabel("Provide details about the device")
        label_1 = QLabel("name")
        Device_name = QLineEdit()
        label_2 = QLabel("vendour")
        vendour = QComboBox()
        vendour.addItems(['Amazon', 'Apple', 'Cisco', 'Google', "IBM"])
        button = QPushButton("Continue")
        
        button.clicked.connect(lambda: self.First_Start(vendour.currentText(),Device_name,self.wid_1,mac,ip,a))

        label.setStyleSheet("color : black")
        label_1.setStyleSheet("color : black")
        Device_name.setStyleSheet("background-color : black; border-width: 15px; border-color: beige; min-width: 6em; color : white")
        label_2.setStyleSheet("color : black")
        vendour.setStyleSheet("background-color : white; border-width: 15px; border-color: beige; min-width: 6em; color : black")
        button.setStyleSheet("background-color : white; border-width: 15px; border-color: beige; min-width: 6em; color : black")

        Layout = QVBoxLayout()
        Layout.addWidget(label)
        Layout.addWidget(label_1)
        Layout.addWidget(Device_name)
        Layout.addWidget(label_2)
        Layout.addWidget(vendour)
        Layout.addWidget(button)

        

        Layout.setAlignment(label,Qt.AlignCenter)
        Layout.setAlignment(label_1,Qt.AlignCenter)
        Layout.setAlignment(Device_name,Qt.AlignCenter)
        Layout.setAlignment(label_2,Qt.AlignCenter)
        Layout.setAlignment(vendour,Qt.AlignCenter)
        Layout.setAlignment(button,Qt.AlignCenter)

        self.wid_1 = QWidget()
        self.wid_1.setStyleSheet('background-color: white;')
        self.wid_1.resize(250, 250)
        self.wid_1.setWindowTitle('Provide details')
        self.wid_1.setLayout(Layout)
        self.wid_1.show()

   
    
    def First_Start(self,vendour,name,wid,mac,ip,a):
        
            print((vendour))
            print(str(name.text()))
            print(mac)
            print(ip)
            print(a)

            #t1 = threading.Thread(target=Sniffer.algo, args=(name.text(),vendour.text(),mac,ip,a,))
            t1 = threading.Thread(target= self.closer(wid), args=wid,)
            t1.start()
            t1.join()
            Sniffer.algo(name.text(),vendour,mac,ip,a)
            
            #t1.join()


    def closer(self,wid):
        wid.close()
        print("here here here")

    

        
        
