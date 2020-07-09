# This Python file uses the following encoding: utf-8
import sys
import os
import shutil
from datetime import date
from PySide2.QtWidgets import QApplication, QWidget, QComboBox, QGroupBox, QPushButton, QMainWindow, QTextEdit, QLineEdit, QLayout, QGridLayout, QLabel, QSpinBox
from PySide2.QtCore import QObject, SIGNAL
#from PySide2.QtWidgets import QApplication, QWidget, QComboBox, QGroupBox, QPushButton, QMainWindow, QTextEdit, QLineEdit, QLayout, QGridLayout, QLabel, QSpinBox
#from PySide2.QtCore import QObject, SIGNAL
# sfrom PySide2.QtGui import *

orderNumber  = 1
priceVec     = [0,0,0,0,0,0,0,0]
TOTAL        = 0
menuList     = ['','Calabresa','Frango','Frango com catupiry','Margerita','Mista','Mussarela','Pepperoni', 'Portuguesa']
tradicionals = ['Calabresa', 'Frango', 'Margerita', 'Mista', 'Mussarela']
specials     = ['Frango com catupiry', 'Portuguesa']
premiums     = ['Pepperoni']
pizzaPrice   = [20,25,30]
maxOrder     = 7

if not os.path.exists('/media/adriano/git/orcamento/Orçamentos/'):
    os.mkdir('/media/adriano/git/orcamento/Orçamentos/')
if not os.path.exists('/media/adriano/git/orcamento/Orçamentos/log.txt'):
    # Create log.txt
    with open('/media/adriano/git/orcamento/Orçamentos/log.txt', 'w') as writer:
        writer.write('Relatório de faturamento\n')
        writer.write('------------------------')
        writer.close()
else:
    # Refresh order number
    with open('/media/adriano/git/orcamento/Orçamentos/log.txt', 'r') as reader:
        orderNumber
        text = reader.read().split('#')[1::]
        orderNumber = len(text)+1
        reader.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Widget object
        self.mainWidget = QWidget()
        # Layout object
        self.mainLayout = QGridLayout(self.mainWidget)

        self.infoGroup  = QGroupBox("Dados")
        self.comboGroup = QGroupBox("Pedido")
        self.endGroup   = QGroupBox("Resumo")

        self.mainLayout.addWidget(self.infoGroup, 0, 0)
        self.mainLayout.addWidget(self.comboGroup, 1, 0)
        self.mainLayout.addWidget(self.endGroup, 2, 0)

        self.setCentralWidget(self.mainWidget)

#        # Creating button objects
        self.labelClient  = QLabel("Cliente:")   ; self.editClient   = QLineEdit()
        self.labelPhone   = QLabel("Telefone:")  ; self.editPhone    = QLineEdit()
        self.labelAddr    = QLabel("Endereço:")  ; self.editAddr     = QLineEdit()
        self.labelBurgh   = QLabel("Bairro:")    ; self.editBurgh    = QLineEdit()
        self.labelRef     = QLabel("Referência:"); self.editRef      = QLineEdit()
        self.labelAllergy = QLabel("Alergia")    ; self.editAllergy  = QLineEdit()
        self.labelObs     = QLabel("Obs.:")      ; self.editObs      = QLineEdit()

        self.editClient.textChanged.connect(self.checkMinimumData)
        self.editPhone.textChanged.connect(self.checkMinimumData)
        self.editAddr.textChanged.connect(self.checkMinimumData)
        self.editBurgh.textChanged.connect(self.checkMinimumData)

        self.combo  = [None]*maxOrder
        self.combo2 = [None]*maxOrder
        self.labelPriceU = [None]*maxOrder
        self.labelPriceT = [None]*maxOrder
        self.editQtd = [None]*maxOrder
        for i in range (0,maxOrder):
            self.labelPriceU[i] = QLabel("R$ 0.00")
            self.labelPriceT[i] = QLabel("R$ 0.00")
            self.combo[i] = QComboBox()
            self.combo2[i] = QComboBox()
            self.editQtd[i] = QSpinBox()
            self.combo[i].insertItems(0, menuList)
            self.combo2[i].insertItems(0, menuList)
            self.combo2[i].setEnabled(False)
            self.editQtd[i].setMaximumWidth(50)

        self.labelQtd = QLabel("Qtd."); self.labelItem = QLabel("Item"); self.labelItem2 = QLabel("Metade"); self.labelPriceUStr = QLabel("Preço uni."); self.labelPriceTStr = QLabel("Preço total")

        self.combo[0].currentIndexChanged.connect(lambda: self.price(0))
        self.combo[1].currentIndexChanged.connect(lambda: self.price(1))
        self.combo[2].currentIndexChanged.connect(lambda: self.price(2))
        self.combo[3].currentIndexChanged.connect(lambda: self.price(3))
        self.combo[4].currentIndexChanged.connect(lambda: self.price(4))
        self.combo[5].currentIndexChanged.connect(lambda: self.price(5))
        self.combo[6].currentIndexChanged.connect(lambda: self.price(6))

        self.combo2[0].currentIndexChanged.connect(lambda: self.price(0))
        self.combo2[1].currentIndexChanged.connect(lambda: self.price(1))
        self.combo2[2].currentIndexChanged.connect(lambda: self.price(2))
        self.combo2[3].currentIndexChanged.connect(lambda: self.price(3))
        self.combo2[4].currentIndexChanged.connect(lambda: self.price(4))
        self.combo2[5].currentIndexChanged.connect(lambda: self.price(5))
        self.combo2[6].currentIndexChanged.connect(lambda: self.price(6))

        self.editQtd[0].valueChanged.connect(lambda: self.price(0))
        self.editQtd[1].valueChanged.connect(lambda: self.price(1))
        self.editQtd[2].valueChanged.connect(lambda: self.price(2))
        self.editQtd[3].valueChanged.connect(lambda: self.price(3))
        self.editQtd[4].valueChanged.connect(lambda: self.price(4))
        self.editQtd[5].valueChanged.connect(lambda: self.price(5))
        self.editQtd[6].valueChanged.connect(lambda: self.price(6))

        orderStr = "Pedido n#"+str(orderNumber)
        totalStr = "Valor Total = R$ 0.00"
        self.date = date.today().strftime("%d/%B %Y")
        self.labelDate = QLabel("Data: "+self.date); self.labelOrder = QLabel(orderStr); self.labelTotal = QLabel(totalStr)
        self.buttonConfirm = QPushButton("Confirmar pedido")
        self.buttonConfirm.clicked.connect(self.confirmClick)
        self.buttonConfirm.setEnabled(False)

        self.infoLayout = QGridLayout(self.infoGroup)
        self.infoLayout.addWidget(self.labelClient , 0, 0)
        self.infoLayout.addWidget(self.editClient  , 0, 1)
        self.infoLayout.addWidget(self.labelPhone  , 1, 0)
        self.infoLayout.addWidget(self.editPhone   , 1, 1)
        self.infoLayout.addWidget(self.labelAddr   , 2, 0)
        self.infoLayout.addWidget(self.editAddr    , 2, 1)
        self.infoLayout.addWidget(self.labelBurgh  , 3, 0)
        self.infoLayout.addWidget(self.editBurgh   , 3, 1)
        self.infoLayout.addWidget(self.labelRef    , 4, 0)
        self.infoLayout.addWidget(self.editRef     , 4, 1)
        self.infoLayout.addWidget(self.labelAllergy, 5, 0)
        self.infoLayout.addWidget(self.editAllergy , 5, 1)
        self.infoLayout.addWidget(self.labelObs    , 6, 0)
        self.infoLayout.addWidget(self.editObs     , 6, 1)

        self.comboLayout = QGridLayout(self.comboGroup)
        self.comboLayout.setColumnStretch(1, 1)
        self.comboLayout.addWidget(self.labelItem     , 0, 0)
        self.comboLayout.addWidget(self.labelItem2    , 0, 1)
        self.comboLayout.addWidget(self.labelQtd      , 0, 2)
        self.comboLayout.addWidget(self.labelPriceUStr, 0, 3)
        self.comboLayout.addWidget(self.labelPriceTStr, 0, 4)

        for i in range(0,maxOrder):
            self.comboLayout.addWidget(self.combo[i]      , i+1, 0)
            self.comboLayout.addWidget(self.combo2[i]     , i+1, 1)
            self.comboLayout.addWidget(self.editQtd[i]    , i+1, 2)
            self.comboLayout.addWidget(self.labelPriceU[i], i+1, 3)
            self.comboLayout.addWidget(self.labelPriceT[i], i+1, 4)

        self.endLayout = QGridLayout(self.endGroup)
        self.endLayout.addWidget(self.labelDate    , 0, 0)
        self.endLayout.addWidget(self.labelOrder   , 0, 1)
        self.endLayout.addWidget(self.labelTotal   , 0, 2)
        self.endLayout.addWidget(self.buttonConfirm, 1, 2)

############################################## APAGAR
        self.editClient.setText('Adriano Rodrigues')
        self.editAddr.setText('Av. Engenheiro Alberto Sá, 153, apt 301')
        self.editPhone.setText('(85) 9.9404-2131')
        self.editBurgh.setText('Vicente Pinzon')
        self.editRef.setText('Em frente ao posto shell. Cruzamento com Eng. Santana Jr.')
        self.combo[0].setCurrentIndex(1)
        self.combo2[0].setCurrentIndex(2)
        self.editQtd[0].setValue(2)
##############################################

    def checkMinimumData(self):
        if TOTAL > 0 and self.editClient.text() and self.editAddr.text() and self.editPhone.text() and self.editBurgh.text() and self.labelRef.text():
            self.buttonConfirm.setEnabled(True)
        else:
            self.buttonConfirm.setEnabled(False)

    def price(self, index):
        global priceVec, TOTAL
        qtd = self.editQtd[index].value()
        if not self.combo2[index].currentText():
            if self.combo[index].currentText() in tradicionals:
                itemPrice = pizzaPrice[0]
                self.combo2[index].setEnabled(True)
            elif self.combo[index].currentText() in specials:
                itemPrice = pizzaPrice[1]
                self.combo2[index].setEnabled(True)
            elif self.combo[index].currentText() in premiums:
                itemPrice = pizzaPrice[2]
                self.combo2[index].setEnabled(True)
            else:
                itemPrice = 0
                self.combo2[index].setEnabled(False)
        else:
            if self.combo[index].currentText() in tradicionals:
                itemPrice1 = pizzaPrice[0]
            elif self.combo[index].currentText() in specials:
                itemPrice1 = pizzaPrice[1]
            elif self.combo[index].currentText() in premiums:
                itemPrice1 = pizzaPrice[2]
            else:
                itemPrice1 = 0

            if self.combo2[index].currentText() in tradicionals:
                itemPrice2 = pizzaPrice[0]
            elif self.combo2[index].currentText() in specials:
                itemPrice2 = pizzaPrice[1]
            elif self.combo2[index].currentText() in premiums:
                itemPrice2 = pizzaPrice[2]
            else:
                itemPrice2 = 0

            itemPrice = (itemPrice1+itemPrice2)/2

        priceVec[index] = itemPrice*qtd
        self.labelPriceU[index].setText('R$ {0:.2f}'.format(itemPrice))
        self.labelPriceT[index].setText('R$ {0:.2f}'.format(priceVec[index]))

        TOTAL = sum(priceVec)
        self.labelTotal.setText('Valor Total = R$ {0:.2f}'.format(TOTAL))
        self.checkMinimumData()

    # CLICK: Confirm order
    def confirmClick(self):
        global orderNumber
        today   = self.date
        client  = self.editClient.text()
        phone   = self.editPhone.text()
        addr    = self.editAddr.text()
        burgh   = self.editBurgh.text()
        allergy = self.editAllergy.text()
        ref     = self.editRef.text()
        obs     = self.editObs.text()
        deliver = "10.00"
        self.deliver = deliver
        item    = [None]*maxOrder
        itemm   = [None]*maxOrder
        qtd     = [None]*maxOrder
        uni     = [None]*maxOrder
        tot     = [None]*maxOrder
        for i in range(0,maxOrder):
            item[i]   = self.combo[i].currentText()
            itemm[i]  = self.combo2[i].currentText()
            qtd[i]    = self.editQtd[i].text()
            uni[i]    = self.labelPriceU[i].text()[3::]
            tot[i]    = self.labelPriceT[i].text()[3::]
            if itemm[i]:
                itemm[i] = ' / '+itemm[i]
            if qtd[i] == '0':
                qtd[i] = ''
            if uni[i] == '0.00':
                uni[i] = ''
            if tot[i] == '0.00':
                tot[i] = ''
        orderStr = "Pedido n#"+str(orderNumber)
        self.labelOrder.setText(orderStr)

        with open('/media/adriano/git/orcamento/template.tex') as replacer:
            dataIn = replacer.read()
            dataIn = dataIn.replace('@data',today)
            dataIn = dataIn.replace('@cliente',client)
            dataIn = dataIn.replace('@telefone',phone)
            dataIn = dataIn.replace('@endereco',addr)
            dataIn = dataIn.replace('@bairro',burgh)
            dataIn = dataIn.replace('@referencia',ref)
            dataIn = dataIn.replace('@alergia',allergy)
            dataIn = dataIn.replace('@obs',obs)
            dataIn = dataIn.replace('@produto1',item[0]); dataIn = dataIn.replace('@produtom1',itemm[0])
            dataIn = dataIn.replace('@produto2',item[1]); dataIn = dataIn.replace('@produtom2',itemm[1])
            dataIn = dataIn.replace('@produto3',item[2]); dataIn = dataIn.replace('@produtom3',itemm[2])
            dataIn = dataIn.replace('@produto4',item[3]); dataIn = dataIn.replace('@produtom4',itemm[3])
            dataIn = dataIn.replace('@produto5',item[4]); dataIn = dataIn.replace('@produtom5',itemm[4])
            dataIn = dataIn.replace('@produto6',item[5]); dataIn = dataIn.replace('@produtom6',itemm[5])
            dataIn = dataIn.replace('@produto7',item[6]); dataIn = dataIn.replace('@produtom7',itemm[6])
            dataIn = dataIn.replace('@qtd1',qtd[0])
            dataIn = dataIn.replace('@qtd2',qtd[1])
            dataIn = dataIn.replace('@qtd3',qtd[2])
            dataIn = dataIn.replace('@qtd4',qtd[3])
            dataIn = dataIn.replace('@qtd5',qtd[4])
            dataIn = dataIn.replace('@qtd6',qtd[5])
            dataIn = dataIn.replace('@qtd7',qtd[6])
            dataIn = dataIn.replace('@valor1U',uni[0]); dataIn = dataIn.replace('@valor1T',tot[0])
            dataIn = dataIn.replace('@valor2U',uni[1]); dataIn = dataIn.replace('@valor2T',tot[1])
            dataIn = dataIn.replace('@valor3U',uni[2]); dataIn = dataIn.replace('@valor3T',tot[2])
            dataIn = dataIn.replace('@valor4U',uni[3]); dataIn = dataIn.replace('@valor4T',tot[3])
            dataIn = dataIn.replace('@valor5U',uni[4]); dataIn = dataIn.replace('@valor5T',tot[4])
            dataIn = dataIn.replace('@valor6U',uni[5]); dataIn = dataIn.replace('@valor6T',tot[5])
            dataIn = dataIn.replace('@valor7U',uni[6]); dataIn = dataIn.replace('@valor7T',tot[6])
            dataIn = dataIn.replace('@entrega',deliver)
            dataIn = dataIn.replace('@valorT','{0:.2f}'.format(TOTAL))
            dataIn = dataIn.replace('@pedido',orderStr)
            dataIn = dataIn.replace('R$','R\$')
            dataIn = dataIn.replace('Pedido n#','Pedido n\#')
            replacer.close()

        invoiceFileName = date.today().strftime("%Y-%m-%d--"+str(orderNumber)+'-'+client.split()[0])
        with open('/media/adriano/git/orcamento/Orçamentos/'+invoiceFileName+'.tex', 'w') as writer:
            for i in range(len(dataIn)):
                writer.write(dataIn[i])
            writer.close()

        os.system('pdflatex -output-directory=\'/media/adriano/git/orcamento/Orçamentos\' /media/adriano/git/orcamento/Orçamentos/'+invoiceFileName+'.tex')
        os.remove('/media/adriano/git/orcamento/Orçamentos/'+invoiceFileName+'.aux')
        os.remove('/media/adriano/git/orcamento/Orçamentos/'+invoiceFileName+'.log')
        os.remove('/media/adriano/git/orcamento/Orçamentos/'+invoiceFileName+'.tex')

        with open('/media/adriano/git/orcamento/Orçamentos/log.txt', 'a') as appender:
            appender.write("\n\n"+self.labelOrder.text())
            appender.write(date.today().strftime(" \n%d/%B %Y\n"))
            appender.write('Pizzaria R$ {0:.2f}'.format(TOTAL)+'\n')
            appender.write('Entrega R$ '+deliver+'\n')
            appender.close()

        with open('/media/adriano/git/orcamento/Orçamentos/log.txt', 'r') as reader:
            text = reader.read()
            pizza = text.split('Pizzaria R$ ')[1::]
            N = len(pizza)
            profit = [None]*N
            for i in range(0,N):
                profit[i] = float(pizza[i].split('\n')[0])
            profitTotal = sum(profit)
            reader.close()

        with open('/media/adriano/git/orcamento/Orçamentos/log.txt', 'a') as appender:
            appender.write("Acumulado R$ {0:.2f}".format(profitTotal)+'\n')
            appender.close()

        orderNumber += 1
        orderStr = "Pedido n#"+str(orderNumber)
        self.labelOrder.setText(orderStr)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    form = MainWindow()
    form.setWindowTitle('Orçamento: Já chegou!')
    form.setGeometry(100, 100, 500, 500)
    form.show()
    sys.exit(app.exec_())