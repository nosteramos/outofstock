import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import xml.dom.minidom

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from channels import send_mail


class Tests(unittest.TestCase):

    def setUp(self):
        options = Options()
        options.add_argument("--disable-notifications")
        self.driver = webdriver.Chrome("chromedriver.exe", options=options)

    def test_outogstock(self, urls=None):

        wait = WebDriverWait(self.driver, 10)

        #
        # filepath = 'urls'
        # urls = []
        # with open(filepath) as fp:
        #     line = fp.readline()
        #     cnt = 1
        #     while line:
        #         urls.append(line)
        #         line = fp.readline()
        #         cnt += 1

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
                WebDriverWait(self.driver, 10).until(
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

                soldout_links = []
                for elm in elms:
                    if elm.is_displayed():
                        outofstock = True
                        links = elm.find_element_by_xpath("..").find_elements_by_tag_name("a")
                        if links:
                            soldout_links.append(links[0].get_attribute("href"))
                        break

                for l in soldout_links:
                    if str(l).startswith("http"):
                        msg = msg + l + "\n"

        send_mail(rcpt_list="amosmastbaum@gmail.com,reuterz@gmail.com", subject="Sold out - All Products",
                  body_text=msg)

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
