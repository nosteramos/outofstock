import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import xml.dom.minidom

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


from channels import send_mail
####


#//div[@class='product g']



class Tests(unittest.TestCase):


    def waitForPage(self, url):
        self.driver.get(url)
        WebDriverWait(self.driver, 1000).until(
            lambda driver: driver.execute_script('return document.readyState') == 'complete')
        self.driver.refresh()
        WebDriverWait(self.driver, 1000).until(
            lambda driver: driver.execute_script('return document.readyState') == 'complete')
        self.driver.refresh()
        WebDriverWait(self.driver, 1000).until(
            lambda driver: driver.execute_script('return document.readyState') == 'complete')



    def getLinks(self, url):
        self.waitForPage(url)
        items = self.driver.find_elements_by_class_name("product g")
        if items:
            result = []
            for item in items:
               result.append(item.find_element_by_xpath("//a/@href"))
            return result

        cat = self.driver.find_elements_by_class_name("category g")
        result = []
        for c in cat:
            _r = self.getLinks(c.find_element_by_xpath("//a/@href"))
            result.extend(_r)




    def ping(self,host):
        """
        Returns True if host responds to a ping request
        """
        import subprocess, platform

        # Ping parameters as function of OS
        ping_str = "-n 1" if platform.system().lower() == "windows" else "-c 1"
        args = "ping " + " " + ping_str + " " + host
        need_sh = False if platform.system().lower() == "windows" else True
        # Ping
        return subprocess.call(args, shell=need_sh) == 0

    def setUp(self):
        options = Options()
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-plugins")
        options.add_argument("--disable-extensions")
        options.set_capability('unexpectedAlertBehaviour', "dismiss")
        options.add_experimental_option("useAutomationExtension", False)
        self.driver = webdriver.Chrome("chromedriver.exe", options=options)

    # def test_outogstock_2(self):
    #
    #     self.getLinks("https://www.petmountain.com/category/aquarium")
    #
    #     pass

    def test_outogstock(self, urls=None):

        last = open('last', 'r')
        prev_list = last.readlines().copy()
        last.close()

        if not self.ping('www.saltwateraquarium.com'):
            send_mail(rcpt_list="amosmastbaum@gmail.com", subject="Failed to run!!! Sold out - All Products",
                      body_text="Maybe Amos turned off th Modem again?")
            send_mail(rcpt_list="reuterz@gmail.com", subject="Failed to run!!! Sold out - All Products",
                      body_text="Maybe Amos turned off th Modem again?")
            exit(-1)

        soldout_links = {""}
        wait = WebDriverWait(self.driver, 10)
        categories = ["aquariums",
                      "filtration-reactors-media",
                      "controllers-monitoring",
                      "filtration-reactors-media",
                      "food",
                      "aquarium-lighting",
                      "pumps",
                      "saltwater-specialty"]

        msg = "Products out of stock:\n\n"
        for category in categories:
            i = 0
            while True:
                i = i + 1
                url = "https://www.saltwateraquarium.com/" + str(category) + ".html?sort=bestselling&page=" + str(i)
                self.driver.get(url)
                WebDriverWait(self.driver, 1000).until(
                    lambda driver: driver.execute_script('return document.readyState') == 'complete')
                elms = self.driver.find_elements_by_xpath("//*[contains(text(),'404 Error - Page not found')]")
                if elms:
                    url = "https://www.saltwateraquarium.com/" + str(category) + "?sort=bestselling&page=" + str(i)
                    self.driver.get(url)
                    WebDriverWait(self.driver, 10).until(
                        lambda driver: driver.execute_script('return document.readyState') == 'complete')
                    elms = self.driver.find_elements_by_xpath("//*[contains(text(),'404 Error - Page not found')]")
                    if elms:
                        break
                elms.extend(self.driver.find_elements_by_xpath("//*[contains(text(),'Out of stock')]"))
                elms.extend(self.driver.find_elements_by_xpath("//*[contains(text(),'Sold out')]"))
                outofstock = False

                for elm in elms:
                    links = elm.find_element_by_xpath("..").find_elements_by_tag_name("a")
                    print(links[0].get_attribute("href"))
                    if elm.is_displayed() or True:
                        if links:
                            soldout_links.add(links[0].get_attribute("href"))



        last = open('last', 'w')
        last.truncate()
        ii=0
        for l in soldout_links:
            if str(l).startswith("http"):
                last.write(l + "\n")
                ii=ii+1
                if l + "\n" not in prev_list:
                    msg = msg + "(new)"
                msg = msg + str(ii) + ")" + l

                msg = msg + "\n"
                # self.driver.quit()
                # self.setUp()
                # self.driver.get(l)
                # time.sleep(3)
                # self.driver.find_elements_by_id("InStockNotifyEmailAddress")[0].send_keys("reuterz@gmail.com")
                # self.driver.find_elements_by_id("InStockNotifyClick")[0].click()
                # time.sleep(2)

        last.flush()
        last.close()


        send_mail(rcpt_list="amosmastbaum@gmail.com", subject="Sold out - All Products",
                  body_text=msg)

        send_mail(rcpt_list="reuterz@gmail.com", subject="Sold out - All Products",
                  body_text=msg)

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
