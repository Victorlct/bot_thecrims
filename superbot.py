import undetected_chromedriver as uc
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
import time
import pyautogui
import re

class superbot:
    def __init__(self):
        self.tipoRoubo = 1 #1= normal  2=gangue
        self.vicioNum = 0
        self.numRoubos=0
        self.ultDiaTreino=0
        self.site_link = "https://www.thecrims.com"
        self.user = "" #seu user
        self.password = "" #sua senha
        self.treino = 1
        self.qtdTreinoDia = 0
        options = webdriver.ChromeOptions() 
        self.driver = uc.Chrome(options=options)
        options.add_argument('--ignore-certificate-errors')
        self.driver.maximize_window()

    def abrir_site(self):
        self.driver.get(self.site_link)
        self.login()
        self.roubar()

    def roubar(self):
        #ve se realmente logou e corrige bug de login se houver
        try:
            logado = self.driver.find_element(By.ID, "menu-user")
            if not logado:
                time.sleep(12)
                self.login()
        except:
            time.sleep(12)
            self.login()

        self.driver.get(self.site_link)
        time.sleep(2)    
        diaAtual = int(self.getDia())

        try:
            self.driver.find_element("xpath", '//div[@id="menu-sprite-robbery"]')
        except:
            self.seraqueapanhei()

        if(int(self.numRoubos)>10):
            #deixa sempre 20mi na carteira e resto no banco, caso falir (n sei como aconteceria) ele saca pra completar 10mi
            self.dinheiro = int(self.verDin())
            if(self.dinheiro < 20000000):
                diferenca = 20000000 - self.dinheiro
                self.sacarDin(diferenca)
                time.sleep(1)
            if(self.dinheiro > 20000000):
                diferenca = self.dinheiro - 20000000
                self.depDin(diferenca)
                time.sleep(1)
            self.numRoubos = 0

        if self.vicioNum > 9:
            self.hospital() 

        stamina = self.driver.find_element("xpath", '//*[@id="nightclub-singleassault-attack-19"]/div').value_of_css_property("width")
        staminaNum = round(100*float(stamina[:-2])/128)
        if 50>staminaNum:
            self.abrir_clube()

        if(diaAtual > self.ultDiaTreino):
            self.qtdTreinoDia = 0
            #self.coletarPutas()
            #self.coletarFabricas()
            #self.venderDrogas()

        if(self.qtdTreinoDia < 2):
            self.treinar()
            self.qtdTreinoDia = self.qtdTreinoDia + 1

        self.tickets = int(self.qtdTickets())
        if self.tickets < 6:
            self.esperaTicket()

        match self.tipoRoubo:
            case 1: #roubo normal  
                time.sleep(1)
                botaoRoubar = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//div[@id="menu-sprite-robbery"]')))
                botaoRoubar.click()
                drop = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, "singlerobbery-select-robbery")))
                select = Select(drop)
                time.sleep(3)
                select.select_by_value("39")   #id do roubo
                elemento = self.driver.find_element(By.ID, "full-stamina-robbery-toggle")
                if elemento.is_selected():
                    try:
                        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.ID, "singlerobbery-rob"))).click()
                        self.numRoubos = self.numRoubos + 1
                        self.roubar()
                    except:
                        self.roubar()
                else:
                    WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.ID, "full-stamina-robbery-toggle"))).click()
                    WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.ID, "singlerobbery-rob"))).click()
                    self.numRoubos = self.numRoubos + 1
                    self.roubar()
            case 2: #roubo gangue
                try:
                    WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.ID, "gangrobbery-accept"))).click()
                except:
                    try:
                        WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.ID, "gangrobbery-execute")))
                        time.sleep(1)
                        pyautogui.moveTo(930,458)
                        pyautogui.click(930,458)
                        self.qtdRouboGangue = self.qtdRouboGangue + 1
                        self.roubar() 
                    except:
                        self.entrarGang()
        
                time.sleep(2)
                pyautogui.moveTo(930,458)
                pyautogui.click(930,458)
                self.roubar()
            case _: #default
                pass
         
    def treinar(self):

        stamina = self.driver.find_element("xpath", '//*[@id="nightclub-singleassault-attack-19"]/div').value_of_css_property("width")
        staminaNum = round(100*float(stamina[:-2])/128)
        if 50>staminaNum:
            self.abrir_clube()

        self.dinheiro = int(self.verDin()) #certifica que tem dindin
        if(self.dinheiro < 10000000):
            diferenca = 10000000 - self.dinheiro
            self.sacarDin(diferenca)
            time.sleep(1)

        self.driver.get('https://www.thecrims.com/newspaper#/training')
        rest=self.treino % 2

        if(rest==0):
            #par = gym
            pyautogui.moveTo(1150,575)
            time.sleep(0.8)
            pyautogui.click(1150,575)
            self.ultDiaTreino = int(self.getDia())
        else:
            #impar = education
            pyautogui.moveTo(1150,710)
            time.sleep(0.8)
            pyautogui.click(1150,710)
            self.ultDiaTreino = int(self.getDia())
        
        self.driver.get(self.site_link) 

        try:
            self.driver.find_element(By.XPATH, '//div[@id="menu-sprite-robbery"]') #se achar o div nao esta treinando
            self.roubar()
        except: #esta treinando
            try:
                cli = self.driver.find_element(By.XPATH, '//*[@id="menu-sabotage"]')
                cli.click()
                for i in range(1860, 0, -1):
                    mensagem = f"Treinando por mais {i} segundos..."
                    self.driver.execute_script(f"document.querySelector('.content_style.main-content').innerHTML = '<h1>{mensagem}</h1>'")
                    time.sleep(1)
                    try:
                        self.driver.find_element(By.XPATH, '//div[@id="menu-sprite-robbery"]') #se achar o div nao esta treinando
                        self.roubar()      
                    except:
                        continue
                self.driver.execute_script("document.querySelector('.content_style.main-content').innerHTML = '<h1>Finalizado!</h1>'")
                self.driver.get(self.site_link)  
                time.sleep(1)
                self.roubar()
            except:
                self.roubar()
        self.roubar()

    def depDin(self, valor):
        cli = self.driver.find_element(By.XPATH, '//*[@id="menu-bank"]')
        cli.click()
        time.sleep(1)
        select_element = self.driver.find_element(By.CSS_SELECTOR, 'select')
        select_object = Select(select_element)
        time.sleep(1)
        select_object.select_by_value('deposit')
        time.sleep(0.3)
        campo_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='number']")
        campo_input.clear()
        campo_input.send_keys(f'{valor}')
        pyautogui.moveTo(770,350)
        time.sleep(0.8)
        pyautogui.click(770,350)
        time.sleep(1)
    
    def sacarDin(self, valor):
        self.driver.get(self.site_link)
        cli = self.driver.find_element(By.XPATH, '//*[@id="menu-bank"]')
        cli.click()
        time.sleep(2.5)
        select_element = self.driver.find_element(By.CSS_SELECTOR, 'select')
        select_object = Select(select_element)
        time.sleep(1.5)
        select_object.select_by_value('withdraw')
        time.sleep(0.3)
        campo_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='number']")
        campo_input.clear()
        campo_input.send_keys(f'{valor}')
        pyautogui.moveTo(770,350)
        time.sleep(0.8)
        pyautogui.click(770,350)
        time.sleep(1)
    
    def verDin(self):
        content_right = self.driver.find_element(By.ID, 'content_right')
        din = content_right.find_element(By.XPATH, './/div[contains(text(), "Cash")]').text.split()[-1]
        total =  int(''.join(filter(str.isdigit, din)))
        totalFormatado = str(total).lstrip('0')
        return totalFormatado

    def qtdTickets(self):
        content_right = self.driver.find_element(By.ID, 'content_right')
        tickets = content_right.find_element(By.XPATH, './/div[contains(text(), "Tickets")]').text.split()[-1]
        return tickets

    def hospital(self):
        try:
            self.dinheiro = int(self.verDin())
            if(self.dinheiro < 30000000):
                diferenca = 30000000 - self.dinheiro
                self.sacarDin(diferenca)
                time.sleep(1)
            if(self.dinheiro > 30000000):
                diferenca = self.dinheiro - 30000000
                self.depDin(diferenca)
                time.sleep(1)
        except:
            pass

        try:
            botaoHosp = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="menu-hospital"]')))
            if botaoHosp: 
                botaoHosp.click() 
                time.sleep(2)
                inputQtd = self.driver.find_element("xpath", '//*[@id="content_middle"]/div/div[3]/table[1]/tbody/tr[5]/td[4]/input')
                inputQtd.send_keys(f'{5}')
                pyautogui.moveTo(1150,475)
                pyautogui.click(1150,475)
                self.vicioNum=0  
        except:
            self.roubar()
        time.sleep(2)

    def abrir_clube(self):
        self.driver.get(self.site_link)
        time.sleep(2)

        try:
            stamina = self.driver.find_element("xpath", '//*[@id="nightclub-singleassault-attack-19"]/div').value_of_css_property("width")
            staminaNum = round(100*float(stamina[:-2])/128)
            if 50<staminaNum:
                self.roubar()
        except:
            pass
     
        try:
            botaoClube = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="menu-nightlife"]'))) #esta no menu de clubs
            if botaoClube: 
                botaoClube.click() 
                time.sleep(1.5)
                pyautogui.moveTo(900,470)
                pyautogui.click(900,470) #entrou em um club
                try:
                    btnComprar = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[contains(text(), "Buy")]')))
                    btnComprar.click()
                    btnSair = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[contains(text(), "Exit")]')))
                    btnSair.click()
                    self.vicioNum = self.vicioNum + 1
                except:
                    self.seraqueapanhei()
        except:
            self.roubar()

    def login(self):
        self.driver.get(self.site_link) #att para tentar corrigir bug login
        log = self.driver.find_element("xpath", '//*[@id="loginform"]/input[1]')
        pas = self.driver.find_element("xpath",'//*[@id="loginform"]/input[2]')
        if log:
            try:
                log.clear()
                log.send_keys(f'{self.user}')
            except:
                print("problema com user")
        if pas:
            try:
                pas.clear()
                pas.send_keys(f'{self.password}')
            except:
                print("problema com senha")
        if log.get_attribute("value") == f'{self.user}' and pas.get_attribute("value") == f'{self.password}':
            try:
                click_but = self.driver.find_element("xpath",'//*[@id="loginform"]/button') 
                click_but.click()
            except:
                print('problema no botao de login')
        time.sleep(3)

    def seraqueapanhei(self):
        try:
            self.driver.find_element(By.XPATH, '//*[@id="menu-sabotage"]')
        except:
            botaoHosp = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="menu-hospital"]')))
            botaoHosp.click()
            if self.driver.current_url == 'https://www.thecrims.com/newspaper#/rip':
                for i in range(600, 0, -1): #se o tempo de recuperacao for maior que 10m, ele volta aq e espera mais 10m, ate recuperar
                    mensagem = f"Passando vergonha por mais {i} segundos..."
                    self.driver.execute_script(f"document.querySelector('.content_style.main-content').innerHTML = '<h1>{mensagem}</h1>'")
                    time.sleep(1)
                    try:
                        self.driver.find_element(By.XPATH, '//div[@id="menu-sprite-robbery"]')
                        i=600
                        self.roubar()
                    except:
                        continue
            else:
                self.driver.get(self.site_link)
                time.sleep(2)
                self.roubar()

    def coletarPutas(self):
        self.driver.get(self.site_link)
        try:
            botaoPutas = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="menu-hookers"]')))
            botaoPutas.click()
            time.sleep(3)
            btnComprar = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'btn btn-inverse btn btn-inverse pull-right')))
            btnComprar.click()
            self.roubar()
        except:
            self.driver.execute_script("document.querySelector('.content_style.main-content').innerHTML = '<h1>NAO CLIQUEI NO BOTAO</h1>'")
            time.sleep(5)
            pyautogui.click(1340,80) #desloga    
        
    def entrarGang(self):
        self.driver.get(self.site_link)
        pagGang = self.driver.find_element(By.CSS_SELECTOR, "a[href='/gang'] img[title='Gang center']")
        pagGang.click()
        pyautogui.moveTo(1165,634)
        pyautogui.click(1165,634)
        time.sleep(1)
        self.driver.get(self.site_link)
        self.roubar()  

    def getDia(self):
        diaHTML = self.driver.find_element(By.CSS_SELECTOR, "div.pull-right")
        diaTexto = diaHTML.text
        dia = int(diaTexto.split()[1])
        return dia
        
    def esperaTicket(self):
        try:
            botaoAssault = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, ' //*[@id="menu-assault"]')))
            if botaoAssault: 
                botaoAssault.click() 
                for i in range(2400, 0, -1): #espera 40min por tickets
                    mensagem = f"Esperando tickets por mais {i} segundos... (Total de espera = 40min ou 30 tickets)"
                    self.driver.execute_script(f"document.querySelector('.content_style.main-content').innerHTML = '<h1>{mensagem}</h1>'")
                    time.sleep(1)
                    self.tickets = int(self.qtdTickets())
                    if(self.tickets > 29):
                        i = 600
                        self.driver.get(self.site_link)
                        self.roubar()
        except:
            time.sleep(1)
            pyautogui.click(1340,80) #desloga
            time.sleep(5)

    def coletarDrogas(self):
        self.driver.get(self.site_link)
        try:
            botaoBuild = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="menu-buildings"]')))
            botaoBuild.click()
            table = self.driver.find_element(By.CSS_SELECTOR, "table.table-condensed.table-top-spacing") #ideia era deletar todos os botoes antes do Coletar, para sobrar somente ele para clicar, mas essa tabela nao é identificada
            self.driver.execute_script("arguments[0].remove()", table)
            time.sleep(4)
            element = self.driver.find_element,(By.CLASS_NAME, 'well')
            self.driver.execute_script("arguments[0].remove()", element)
            time.sleep(4)
            collect_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn-inverse.btn.btn-inverse.btn-small')))
            collect_button.click()
            time.sleep(4)
            mensagem = f"COLETEI AS DROGAS"
            self.driver.execute_script(f"document.querySelector('.content_style.main-content').innerHTML = '<h1>{mensagem}</h1>'")
            time.sleep(4)
            self.driver.get(self.site_link)
        except:
            mensagem = f"Não consegui coletar"
            self.driver.execute_script(f"document.querySelector('.content_style.main-content').innerHTML = '<h1>{mensagem}</h1>'")
            time.sleep(5)
            self.driver.get(self.site_link)

    def presencaAula(self):
        self.driver.get(self.site_link)
        try:
            btnUni = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="menu-university"]')))
            btnUni.click()
            pyautogui.click(810,540) #entra no Paul
            btnPresenca = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@value="Register presence"]')))
            btnPresenca.click() #nao encontrou o botao
            self.driver.get(self.site_link)
            btnUni = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="menu-university"]')))
            btnUni.click()
            pyautogui.click(850,850) #entra no Tony
            btnPresenca = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input.btn.btn-inverse[value="Register presence"]')))
            btnPresenca.click() #nao encontrou o botao
            #clica na presença
            self.driver.get(self.site_link)
        except:
            mensagem = f"Não consegui registrar presenca"
            self.driver.execute_script(f"document.querySelector('.content_style.main-content').innerHTML = '<h1>{mensagem}</h1>'")
            time.sleep(5)
            self.driver.get(self.site_link)

bot = superbot()
bot.abrir_site()
pyautogui.click(1340,80) #desloga
time.sleep(5)

#todo
    #tratar erro: depois que treinar 2x ao dia 
        #erro ao treinar pela segunda vez
    
    #universidade
        #verificar presenca do botao Registrar Presença e clicar - botao nao encontrado
    #coletar putas verifica presenca de botao coletar na tela e clica
    #coletar fabricas verifica presenca de botao coletar na tela e clica
    #fazer bot kill - na def Abrir CLube

    #roubos
    # diamofirna heroina 107 roubo 80k lucro 9,2mi   
    # claviceps cod roubo 42 
    # morphine  93 roubo80k lucro 8mi    cod roubo 45
    # poppy opium 79 roubo 160k lucro 13,3mi   cod roubo 47    
    # ketmina special k 119 roubo 80k  lucro 10,2mi  n vale
    # pheny anfetamina 84 roubo 140k   lucro 12,6mi   n vale
    #cocaina  69
    #magic mus 33
    #ecstasy 38
    #amphetamine 84
    #ghb 42
    
    #300k claviceps = 100200lsd a 55,00 = 5511000 din
    #160k poppy opium = 53440opium a 76,00 = 4061440 din

    #cod 30 motorgang
    #cod 27 russian
    #cod 39 million yat = 26,5mi por 100%
    #cod 24 drugking
    #cod 33 vaticano

    #acoes humanas

    #comprar curso na universidade
    #jogar dados
    #upgrade fabricas
    #vender drogas
    #tasks
    #usar item especial
    #vender barco
    #selecionar tipo de roubo pela variavel ou criar contador e alterar automaticamente a variavel tiporoubo