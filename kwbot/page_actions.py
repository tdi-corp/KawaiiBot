from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup as bs


class PageActions:
    """Class """

    def __init__(self):
        self.delay = 20


    def close_all_tabs_exept_current(self, browser):

        handles = browser.window_handles
        current = browser.current_window_handle
        size = len(handles)

        for x in range(size):
            if handles[x] != current:
                browser.switch_to.window(handles[x])
                self.wait_page_by_tag(browser)
                print(f"--Close window - with Title: {browser.title}")
                browser.close()

            browser.switch_to.window(current)

        print(f"--Current window - with Title: {browser.title}, with Id: {browser.current_window_handle}")




    def wait_page_by_tag(self, browser, tag="html"):

        try:
            WebDriverWait(browser, self.delay).until(
                EC.presence_of_element_located((By.TAG_NAME, tag))
            )
        except:
            print("Loading took too much time!")
            browser.quit()



    def wait_page_by_CLASS_NAME(self, browser, tag="html"):

        try:
            WebDriverWait(browser, self.delay).until(
                EC.presence_of_element_located((By.CLASS_NAME, tag))
            )
        except:
            print("Loading took too much time!")
            browser.quit()



    def wait_page_by_xpath(self, browser, xpath):

        try:
            WebDriverWait(browser, self.delay).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
        except:
            print("Loading took too much time!")
            browser.quit()




    def get_and_wait_page_by_tag(self, browser, url, tag="html"):

        browser.get(url)

        try:
            el = WebDriverWait(browser, self.delay).until(
                EC.presence_of_element_located((By.TAG_NAME, tag))
            )
            if el:
                print(f"--Active Handle Tab - Title: {browser.title}")
            else:
                print("Sorry!")

        except:
            print("Loading took too much time!")
            browser.quit()
            # exit()



    def wait_page_and_click_by_xpath(self, browser, xpath):

        try:
            el = WebDriverWait(browser, self.delay).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            if el:
                browser.find_element(By.XPATH, xpath).click()
                print(f"--Click xpath")
            else:
                browser.quit()
                print(f"--Error xpath")

        except:
            browser.quit()
            print(f"--Error Loading took too much time! by xpath")
            # exit()



    def wait_page_and_find_elements_by_xpath(self, browser, xpath):

        elements = None
        try:
            el = WebDriverWait(browser, self.delay).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            if el:
                elements = browser.find_elements(By.XPATH, xpath)
                print(f"--Elements find by xpath")
            else:
                print(f"--Error xpath")

        except:
            print(f"--Error Loading took too much time! by xpath")
            # exit()

        return elements




    def switch_to_second_tab_if_there_two_and_close_first(self, browser):
        handles = browser.window_handles
        current = browser.current_window_handle
        size = len(handles)

        for x in range(size):
            if handles[x] == current:
                print(f"--Close window with - Title: {browser.title}")
                browser.close()

            elif handles[x] != current:
                browser.switch_to.window(handles[x])
                print(f"--Active Handle Tab - Title: {browser.title}")




    def switch_to_second_tab_if_there_two(self, browser):
        handles = browser.window_handles
        current = browser.current_window_handle
        size = len(handles)

        for x in range(size):
            if handles[x] != current:
                browser.switch_to.window(handles[x])
                print(f"--Active Handle Tab - Title: {browser.title}")






    def switch_to_first_tab(self, browser):
        handles = browser.window_handles
        browser.switch_to.window(handles[0])
        print(f"--Switch to First Tab - with Active Handle Tab title: {browser.title}")




    def open_dropdown_and_click(
            self,
            browser,
            xpath_dropd,
            togg_dropd,
            xpath_click,
            togg_click
        ):
        """
        Open dropdown and select one item

        :browser
        :xpath_dropd: string: "//tag[@class='' and ({})]\n"
        :togg_dropd: array: ['val1', 'val2']
        :xpath_click: string: "//tag[@class='' and ({})]\n"
        :togg_click: array: ['val1 or val2']

        """
        text_dropd = self.xpath_text(togg_dropd)

        xp_dropd = xpath_dropd.format(text_dropd)

        self.wait_page_and_click_by_xpath(
                browser,
                xp_dropd
            )



        text_click = self.xpath_text(togg_click)

        xp_click = xpath_click.format(text_click)

        self.wait_page_and_click_by_xpath(
                browser,
                xp_click
            )




    def get_html_page(self, browser):

        source_data = browser.page_source
        soup = bs(source_data, 'lxml')

        return soup




    def xpath_text(self, val = []):
        """

        :return: string: "text() = '' or text() = ''"
        """
        size = len(val)

        if size > 0:

            textf = []

            for x in range(size):
                if x == 0:
                    r = "text()='{}'\n".format(val[x])

                else:
                    r = " or text()='{}'\n".format(val[x])

                textf.append(r)

            text = ''.join(textf)

        else:
            text = None

        return text
