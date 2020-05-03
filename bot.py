# Bot que mira que personas sigues en instagram y no te dan el follow back. Esas personas se guardan en "unfollowers.txt"

from selenium import webdriver
from time import sleep
from secrets import pw

class MyBot:
    def __init__(self, username, pw):
        self.driver = webdriver.Chrome()
        self.username = username
        self.driver.get("https://instagram.com")
        sleep(2)
        # self.driver.find_element_by_xpath("//a[contains(text(), 'Log in')]")\
        #     .click()
        # sleep(2)

        # Busca el xpath que tenga un input con name = username
        self.driver.find_element_by_xpath("//input[@name=\"username\"]")\
            .send_keys(username)
        self.driver.find_element_by_xpath("//input[@name=\"password\"]")\
            .send_keys(pw)
        self.driver.find_element_by_xpath('//button[@type="submit"]')\
            .click()
        sleep(4)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Ahora no')]")\
            .click()
        sleep(2)

    def get_unfollowers(self):
        # Vamos al link de nuestro usuario
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(self.username))\
            .click()
        sleep(2)

        cantSeguidores = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span').text
        cantSeguidores = cantSeguidores.replace('.','')
        print( "Cantidad de seguidores: " + cantSeguidores)
        cantSeguidos = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span').text
        cantSeguidos.replace(',s','')
        print( "Cantidad de seguidos: " +cantSeguidos)


        self.driver.find_element_by_xpath("//a[contains(@href,'/following')]")\
            .click()

        following = self._get_names(cantSeguidos)

        while (following == False):
            self.driver.find_element_by_xpath("//a[contains(@href,'/following')]")\
                .click()
            following = self._get_names(cantSeguidos)

        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]")\
            .click()
        followers = self._get_names(cantSeguidores)

        while (followers == False):
            self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]")\
                .click()
            followers = self._get_names(cantSeguidores)

        # Aqui esta la chicha. Busca todos los usuarios que estan en la lista folowing que no estan en
        # followers y los guarda en una lista
        not_following_back = [user for user in following if user not in followers]
        print(not_following_back)
        t = open("unfollowers.txt" , "w")
        for persona in not_following_back:
            t.write(persona+"\n")
        self.driver.close()

    def _get_names(self, num):
        sleep(2)

        # Esta parte la comente ya que no me aparecen a mi
        # sugs = self.driver.find_element_by_xpath('//h4[contains(text(), Suggestions)]')
        # self.driver.execute_script('arguments[0].scrollIntoView()', sugs)
        # sleep(2)


        print(num)
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[2]")

        # Vamos hasta el final del cuadro con el while. En cada ciclo del while comparamos
        # el alto del cuadro con el alto del cuadro antes de hacer scroll, si es el mismo
        # es que ya hemos terminado
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(2)
            # Vamos hasta el final del box, y luego retornamos el alto del cuadro
            ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight);
                return arguments[0].scrollHeight;
                """, scroll_box)

        # links seran todos aquellos enlaces dentro del cuadro de texto
        links = scroll_box.find_elements_by_tag_name('a')
        # for name in links:
        #     if name.text != '':
        #         name = names
        names = [name.text for name in links if name.text != '']

        print(len(names))
        # close button
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]/button")\
            .click()

        # Hice esta linea porque a veces no recorria el box entero, entonces puse que si hay mas de
        # 10 personas que no recorrio, devuelva false asi lo vuelve a recorrer
        return names if len(names) >= (int(num) - 10) else False


my_bot = MyBot('zurdelli', pw)
my_bot.get_unfollowers()
