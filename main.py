from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

"""
Este protótpipo tem a finalidade de aumentar a quantidade de seguidores
de um determinado perfil do instagram de forma automatizada.

Antes de iniciar o script é necessário preencher as variáveis:
self.user_login - login do usuario que quer ganhar seguidores
self.user_password - senha do usuario que quer ganhar seguidores
self.profile_list - lista de perfis no instagram para seguir os seguidores

Etapas da rotina:
01. login() - Faz o login no instagram com a conta e senha do usuário. 
02. search_profile() - Utilizando a lista self.profile_list, abre a página do perfil e o remove da lista.
03. open_followers() - Abre a lista de seguidores.
04. sweep_followers() - Rola a barra de rolagem da tela de seguidores até o final.
05. follow() - Segue ordenadamente os seguidores, sempre saltando um deles sem seguir. 
06. close_followers_box() - Fecha a caixa de seguidores.
Finalmente a rotina recomeça com o próximo perfil da lista self.profile_list, sem repetir a Etapa 01 login().

Todas as etapas tem seu tratamento de erro com mensagens específicas.

Ao final de cada função e ao encerrar o script é exibida uma mensagem de sucesso.

"""

__author__= "Diogo Oliveira"
__date__ = "06/01/2020"
__version__ = "1.0.0"

PATH = "C:\Program Files (x86)\chromedriver.exe" # pega o path do executável do chrome driver

class InstaBot():
    def __init__(self):
        self.driver = webdriver.Chrome(PATH)
        self.driver.get("https://instagram.com") # abre a página
        self.profile_list = ['sw0len_lab1a', 'dabhitzz', 'pocketnoose'] # lista de usuarios do instagram para seguir os seguidores
        self.user_login = "__biaabite"
        self.user_password = "Minhasenha123" #senha do seu usuario do instagram
        self.number_to_follow = 500 #numero de seguidores a ser seguido de cada perfil listado (este número será dividido por 2)
        try:
            self.login(); sleep(2)
            for i in self.profile_list:
                self.search_profile(); sleep(2)
                self.open_followers(); sleep(2)
                self.sweep_followers(); sleep(2)
                self.follow(); sleep(2)
                self.close_followers_box(); sleep(2)
        except:
            print('Erro na função Iniciar')
        print('Fim do Script')
    
    def login(self):
        try:
            self.login = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input'))
            )
            self.login.send_keys(self.user_login) #preenche usuario
        except:
            print('Erro ao preencher o login')
        try:
            self.senha = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input'))
            )
            self.senha.send_keys(self.user_password) #Preenche senha
            sleep(1)
        except:
            print('Erro ao preencher a senha')
        try:
            self.entrar = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="loginForm"]/div/div[3]/button'))
            )
            self.entrar.click() #Clica no botão entrar
        except:
            print('Erro ao clicar no botão Entrar')
        print('LOGIN REALIZADO COM SUCESSO')

    def search_profile(self):
        try:
            search = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div/div/span[2]'))
            )
            search.click() #clica na barra de pesquisa para ativar o input de pesquisa
        except:
            print('Erro ao clicar na barra de pesquisa')
        try:
            opened_search = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input'))
            )
            opened_search.send_keys(self.profile_list[0]) #digita na barra de pesquisa o perfil a ser pesquisado
            sleep(2)
            opened_search.send_keys(Keys.DOWN)
            sleep(2)
            opened_search.send_keys(Keys.ENTER)
            sleep(2)
        except:
            print('Erro ao digitar perfil a ser pesquisado')
        self.profile_list.remove(self.profile_list[0]) #remove o perfil já pesquisado da lista self.profile_list
        print('PESQUISA DE PERFIL REALIZADA COM SUCESSO')

    def open_followers(self):
        try:
            followers = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a'))
            )
            followers.click()
        except:
            print('Erro ao abrir seguidores')
        print('ABERTURA DOS SEGUIDORES REALIZADA COM SUCESSO')

    def sweep_followers(self):
        
        try:
            followers_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@class="isgrP"]'))
            )
            count = 0
            last_ht, ht = 0, 1
            while last_ht != ht:
                last_ht = ht
                sleep(1)
                ht = self.driver.execute_script("""
                    arguments[0].scrollTo(0, arguments[0].scrollHeight);
                    return arguments[0].scrollHeight;
                    """, followers_box)
                count+=1
                if count == 200: #numero de rolls na barra
                    print('VARREDURA DE SEGUIDORES REALIZADA COM SUCESSO')
                    break
                else:
                    pass
        except:
            print('Erro ao rolar a lista de seguidores')
        

    def follow(self): 
        try:
            for i in range(1, self.number_to_follow): #numero de seguidores a seguir de cada perfil da lista self.profile_list
                if (i%2==0):
                    try:
                        followers = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located(
                                (By.XPATH, '/html/body/div[5]/div/div/div[2]/ul/div/li['+i.__str__()+']/div/div[2]/button'))
                        )
                        if followers.text == 'Seguir':
                            followers.click()
                            sleep(300)
                    except Exception:
                        pass
        except:
            print('Erro ao executar o numero')
        print('PERFIS SEGUIDOS COM SUCESSO')

    def close_followers_box(self): #fechar a tela de seguidores
        try:
            close_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[5]/div/div/div[1]/div/div[2]/button'))
            )
            close_button.click()
        except Exception:
            pass
        print('PASSANDO PARA OUTRO PERFIL')

InstaBot()