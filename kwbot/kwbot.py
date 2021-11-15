import json
import logging
import os
import sys
import re
import time

from dotenv import load_dotenv
from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .browser import set_selenium_local_session
from .page_actions import PageActions



class KwBot:
    """Class to be instantiated to use the script"""

    def __init__(
        self,
        page_delay: int = 25,
        multi_logs: bool = True,
        show_logs: bool = True,
    ):

        self.aborting = "False"


        # main dir
        self.kw_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

        # main bot dir
        self.kw_bot_dir = os.path.dirname(os.path.realpath(__file__))

        # config dir
        self.kw_conf_dir = os.path.join(self.kw_dir, "config")


        # log dir
        self.kw_log_dir = os.path.join(self.kw_dir, "log")
        self.kw_log_file = os.path.join(self.kw_log_dir, "run.log")


        # configs dir
        self.kw_conf_bot = os.path.join(self.kw_conf_dir, "bot.json")
        self.kw_conf_metamask = os.path.join(self.kw_conf_dir, "metamask.json")
        self.kw_conf_scenario = os.path.join(self.kw_conf_dir, "scenario.json")

        # logs dir
        if not os.path.exists(os.path.join(self.kw_log_dir)):
            os.mkdir(os.path.join(self.kw_log_dir))


        # data from config
        self.bot = open_json(self.kw_conf_bot)
        self.metamask = open_json(self.kw_conf_metamask)
        self.scenario = open_json(self.kw_conf_scenario)


        # dotenv
        dotenv_path = Path(os.path.join(self.kw_dir, ".env"))
        load_dotenv(dotenv_path = dotenv_path)


        #.env var
        self.app_name = os.getenv("APP_NAME")

        self.metamask_env_file = os.getenv("METAMASK_FILE")
        self.metamask_env_extension_id = os.getenv("METAMASK_EXTENSION_ID")
        self.metamask_env_secret_recovery_phrase = os.getenv("METAMASK_SECRET_RECOVERY_PHRASE")
        self.metamask_env_password = os.getenv("METAMASK_PASSWORD")
        self.env_driver_path = os.getenv("DRIVER_PATH")


        # assign logger
        logging.basicConfig(
            format='%(asctime)s-%(name)s-%(levelname)s=> [%(funcName)s] %(message)s ', level=logging.INFO, filename=self.kw_log_file,
            filemode='w')
        self.logger = logging.getLogger(__name__)
        # self.logger.info(f'执行{self.browser.title}命令完毕')



        # start Selenium
        self.browser, message = set_selenium_local_session(
            self.bot,
            self.metamask,
            self.metamask_env_file,
            self.env_driver_path,
            self.kw_bot_dir
            )


        self.page_actions = PageActions()


    def run(self):

        #########################################################
        # Start Browser
        #########################################################

        self.start()




        #########################################################
        # Metamask Install
        #########################################################

        self.INS__metamask_install()




        #########################################################
        # 2 Switch Metamask to Binance Smart Chain
        #########################################################

        self.ABS__metamask_bsc()




        #########################################################
        # Kawaii islands Bypass Protection
        #########################################################

        self.bypass_protection()




        #########################################################
        # Kawaii islands Marketplace Open
        #########################################################

        self.website_open()




        #########################################################
        # Metamask connect
        #########################################################

        self.MCN__metamask_connect()




        #########################################################
        #
        #########################################################

        self.PDS__push_dropdown_and_switch_to_latest()



        #########################################################
        #
        #########################################################
        self.PPQ__get_data_from_marketplace_in_cycle()




    def start(self):
        """
        Open Browser
        """

        # Switch to Current Window
        self.browser.switch_to.window(self.browser.current_window_handle)

        # Close all Tabs exept current
        self.page_actions.close_all_tabs_exept_current(self.browser)



    def INS__metamask_install(self):
        """
        Install Metamask and navigate
        """

        # Open Metamask
        self.page_actions.get_and_wait_page_by_tag(
                self.browser,
                'chrome-extension://{}/home.html#initialize/welcome'.format(self.metamask_env_extension_id),
                30
            )

        # Navigate Metamask
        self.page_actions.wait_page_and_click_by_xpath(self.browser, self.scenario['INS']['clickGetStart']['xpath'])
        self.page_actions.wait_page_and_click_by_xpath(self.browser, self.scenario['INS']['clickImportWallet']['xpath'])
        self.page_actions.wait_page_and_click_by_xpath(self.browser, self.scenario['INS']['clickNoThanks']['xpath'])

        # Await Metamask Page Form
        inputs_singup = self.page_actions.wait_page_and_find_elements_by_xpath(self.browser, self.scenario['INS']['awaitMetaPage']['xpath'])

        # Input Metamask Form
        inputs_singup[0].send_keys(self.metamask_env_secret_recovery_phrase)
        inputs_singup[1].send_keys(self.metamask_env_password)
        inputs_singup[2].send_keys(self.metamask_env_password)

        # Push Metamask I have read and agree to the Terms of Use
        self.browser.execute_script(self.scenario['INS']['clickTermsofUse']['script'])

        # Push Metamask Form Import Button
        self.page_actions.wait_page_and_click_by_xpath(self.browser, self.scenario['INS']['clickImport']['xpath'])

        # Push Metamask All Done Button
        self.page_actions.wait_page_and_click_by_xpath(self.browser, self.scenario['INS']['clickAllDone']['xpath'])



    def ABS__metamask_bsc(self):
        """
        Switch Metamask to Binance Smart Chain
        """

        # Open Metamask Settings -> Networks
        self.page_actions.get_and_wait_page_by_tag(
                self.browser,
                'chrome-extension://{}/home.html#settings/networks'.format(self.metamask_env_extension_id),
                30
            )

        # Push Metamask Add Network Button
        self.page_actions.wait_page_and_click_by_xpath(self.browser, self.scenario['ABS']['clickAddNetwork']['xpath'])

        # Await Metamask Network Form
        inputs_network = self.page_actions.wait_page_and_find_elements_by_xpath(self.browser, self.scenario['ABS']['awaitMetamaskForm']['xpath'])

        # Input Metamask Network Form
        inputs_network[0].send_keys(self.metamask['metamask_bsc']['network_name'])
        inputs_network[1].send_keys(self.metamask['metamask_bsc']['new_rpc_url'])
        inputs_network[2].send_keys(self.metamask['metamask_bsc']['chain_id'])
        inputs_network[3].send_keys(self.metamask['metamask_bsc']['symbol'])
        inputs_network[4].send_keys(self.metamask['metamask_bsc']['block_explorer_url'])

        # Push Metamask Network Save Button
        self.page_actions.wait_page_and_click_by_xpath(self.browser, self.scenario['ABS']['clickSave']['xpath'])

        # Wait page by BNB
        self.page_actions.wait_page_by_xpath(self.browser, self.scenario['ABS']['awaitPageBNB']['xpath'])



    def bypass_protection(self):
        """
        Kawaii islands Bypass Protection
        """
        # Open kawaii Globl website
        self.page_actions.get_and_wait_page_by_tag(self.browser, self.bot['urls']['kawaii_global'], 50)

        # wait
        time.sleep(5)

        # Click to link
        self.browser.find_element_by_partial_link_text('Marketplace').click()

        # Close first tab
        self.page_actions.switch_to_second_tab_if_there_two_and_close_first(self.browser)




    def website_open(self):
        """
        Kawaii islands Marketplace Open
        """
        # wait
        time.sleep(3)

        # open kawaii_marketplace_creatures
        self.page_actions.get_and_wait_page_by_tag(
                self.browser,
                self.bot['urls']['kawaii_marketplace_creatures'],
                50
            )




    def MCN__metamask_connect(self):
        """
        Metamask connect to Kawaii islands Marketplace
        """

        time.sleep(2)

        # Push Connect Wallet
        self.page_actions.wait_page_and_click_by_xpath(self.browser, self.scenario['MCN']['clickConnectWallet']['xpath'])

        time.sleep(2)

        # Push Connect Metamask
        self.page_actions.wait_page_and_click_by_xpath(self.browser, self.scenario['MCN']['clickConnectMetamask']['xpath'])


        time.sleep(2)

        # Switch to MetaMask Notification
        self.page_actions.switch_to_second_tab_if_there_two(self.browser)


        time.sleep(2)


        # Click to Next MetaMask Notification
        self.page_actions.wait_page_and_click_by_xpath(self.browser, self.scenario['MCN']['clickNext']['xpath'])


        # Click to Connect MetaMask Notification
        self.page_actions.wait_page_and_click_by_xpath(self.browser, self.scenario['MCN']['clickConnect']['xpath'])


        # time.sleep(2)

        self.page_actions.switch_to_first_tab(self.browser)


        print(self.browser.window_handles)



    def PDS__push_dropdown_and_switch_to_latest(self):
        """
        Push the dropdown and switch to 'Latest'
        """

        time.sleep(3)


        # Push the dropdown Products Position
        self.page_actions.open_dropdown_and_click(
                self.browser,
                self.scenario['FORMS']['dropdowns']['ProductsPosition']['button']['xpath'],
                [
                    self.scenario['FORMS']['dropdowns']['ProductsPosition']['button']['list']['LowestEndingPrice'],
                    self.scenario['FORMS']['dropdowns']['ProductsPosition']['button']['list']['Latest']
                ],
                self.scenario['FORMS']['dropdowns']['ProductsPosition']['menu']['item']['xpath'],
                [
                    self.scenario['FORMS']['dropdowns']['ProductsPosition']['button']['list']['Latest']
                ],
            )




    def PPQ__get_data_from_marketplace_in_cycle(self):
        """
        get data from marketplace in cycle
        """
        price_not_more_than_usd = 200


        flag = 1

        for i in range(10):

            soup = self.switch_dropdown(i)

            result = self.DRP__get_data_from_marketplace_dir_page(price_not_more_than_usd, soup)

            if result['result']['status_buy'] == 'ok':

                x = result['result']['buy'][0]['i']


                # click to Product Card
                self.browser.execute_script(
                        self.scenario['PPQ']['clickProdcard']['script'].format(x)
                    )



                # Wait page by text()='Price'
                self.page_actions.wait_page_by_xpath(
                        self.browser,
                        self.scenario['PPQ']['waitPage']['xpath']
                    )


                # Get HTML page
                soup2 = self.page_actions.get_html_page(self.browser)


                # Take Qt
                name = soup2.find(self.scenario['PPQ']['fndName']['tag'], class_= self.scenario['PPQ']['fndName']['class']).string

                qt = soup2.find(self.scenario['PPQ']['fndQt']['tag'], class_= self.scenario['PPQ']['fndQt']['class']).string

                price_usd = soup2.find(self.scenario['PPQ']['fndPrice']['tag'], class_= self.scenario['PPQ']['fndPrice']['class']).string


                price_maybe, price_usd_convert = check_price(price_not_more_than_usd, price_usd, qt)

                if price_maybe:

                    print(f"Good Price {price_usd_convert}")
                    print(f"dotenv: {self.app_name}")

                    # CLick Button Buy
                    self.page_actions.wait_page_and_click_by_xpath(self.browser, self.scenario['PPQ']['clickBuy']['xpath'])


                    # CLick Button Buy in Popup
                    self.page_actions.wait_page_and_click_by_xpath(self.browser, self.scenario['PPQ']['clickPopupBuy']['xpath'])



                # Stop cicle
                flag = 0


            print("__________________________")

            if flag == 0:
                break




    def DRP__get_data_from_marketplace_dir_page(self, price_not_more_than_usd, soup):
        """
        get data from marketplace in cycle
        """
        # price_not_more_than_usd = 212
        #
        # soup = self.switch_dropdown(0)
        dataOrder = DataOrder()


        quotes = soup.find_all(self.scenario['DRP']['fndAll']['tag'], class_= self.scenario['DRP']['fndAll']['class'])

        data = {}
        status_buy = "no"
        buy = {}
        i = 0
        i_price = 0

        for quote in quotes:


            name = quote.find(self.scenario['DRP']['fndName']['tag'], class_= self.scenario['DRP']['fndName']['class']).string

            qt = quote.find(self.scenario['DRP']['fndQt']['tag'], class_= self.scenario['DRP']['fndQt']['class']).string

            price_usd = quote.find(self.scenario['DRP']['fndPrice']['tag'], class_= self.scenario['DRP']['fndPrice']['class']).string

            price_maybe, price_usd_convert = check_price(price_not_more_than_usd, price_usd, qt)

            data[i] = dataOrder.product(i, name, qt, price_usd_convert)

            print("--- lot: {}, qt: {}, cost: {}".format(name, qt, price_usd_convert))


            if price_maybe:

                buy[i_price] = dataOrder.product(i, name, qt, price_usd_convert)

                status_buy = "ok"
                i_price += 1


            i += 1

        return dataOrder.product_return(status_buy, buy, data)





    def switch_dropdown(self, ivar):
        """
        Switch Status dropdown
        'All' or 'For sale' and parce html

        :return html
        """


        if ivar % 2 == 0:
            # Push the dropdown Products Status
            self.page_actions.open_dropdown_and_click(
                    self.browser,
                    self.scenario['FORMS']['dropdowns']['ProductsStatus']['button']['xpath'],
                    [
                        self.scenario['FORMS']['dropdowns']['ProductsStatus']['button']['list']['All'],
                        self.scenario['FORMS']['dropdowns']['ProductsStatus']['button']['list']['ForSale'],
                        self.scenario['FORMS']['dropdowns']['ProductsStatus']['button']['list']['NotForSale'],
                    ],
                    self.scenario['FORMS']['dropdowns']['ProductsStatus']['menu']['item']['xpath'],
                    [
                        self.scenario['FORMS']['dropdowns']['ProductsStatus']['button']['list']['All']
                    ],
                )
        else:
            # Push the dropdown Products Status
            self.page_actions.open_dropdown_and_click(
                    self.browser,
                    self.scenario['FORMS']['dropdowns']['ProductsStatus']['button']['xpath'],
                    [
                        self.scenario['FORMS']['dropdowns']['ProductsStatus']['button']['list']['All'],
                        self.scenario['FORMS']['dropdowns']['ProductsStatus']['button']['list']['ForSale'],
                        self.scenario['FORMS']['dropdowns']['ProductsStatus']['button']['list']['NotForSale'],
                    ],
                    self.scenario['FORMS']['dropdowns']['ProductsStatus']['menu']['item']['xpath'],
                    [
                        self.scenario['FORMS']['dropdowns']['ProductsStatus']['button']['list']['ForSale']
                    ],
                )


        # Wait page by
        self.page_actions.wait_page_by_CLASS_NAME(
                self.browser,
                30,
                "ListNFT_grid__2DfYW"
            )

        soup = self.page_actions.get_html_page(self.browser)

        return soup




class DataOrder:
    """Class """

    def product(
            self,
            i: int = 0,
            name: str = None,
            qt: int = 1,
            price_usd_convert: float = 0
        ):

        return {'i': i, 'name': name, 'qt': qt, 'price_usd': price_usd_convert}


    def product_return(
            self,
            status_buy: str = None,
            buy = {},
            data = {}
        ):

        res = {}

        res['result'] = {
                'status_buy': status_buy,
                'buy': buy,
                'data': data,
                }

        return res



def check_price(price_not_more_than_usd, price_usd, qt=1):
    """

    :return True/False
    """

    price_usd_convert = convert_amount(price_usd)

    # IF Price is God
    if price_usd_convert <= price_not_more_than_usd:

        return True, price_usd_convert


    return False, price_usd_convert





def convert_amount(num_str):

    powers = {
            'K': 10 ** 3,
            'M': 10 ** 6
        }

    match = re.search(r"([0-9\.]+)\s?(K|M)", num_str)

    if match is not None:
        quantity = match.group(1)
        magnitude = match.group(2)
        return float(quantity) * powers[magnitude]
    else:
        r = re.sub("[^0123456789\.,]","",num_str)
        return float(r)




def open_json(file = "no.json"):

    r = None

    if os.path.exists(file):
        with open(file, encoding="utf-8") as json_file:
            try:
                r = json.load(json_file)
            except Exception as e:
                logger.error(
                    f"Please check {json_file.name}, it contains this error: {e}"
                )
                sys.exit(0)
    else:
        logger.error(
            f"No directory or file"
        )
        sys.exit(0)

    return r



kwbot = KwBot()

kwbot.run()
