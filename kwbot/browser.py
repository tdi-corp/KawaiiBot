from selenium import webdriver


def set_selenium_local_session(
    bot,
    metamask_json,
    metamask_env_file,
    env_driver_path,
    kw_bot_dir
):
    """Starts local session for a selenium server.
    Default case scenario."""

    browser = None
    page_delay = 100
    err_msg = ""

    opt_window_size = "window-size=1920,1080"
    opt_user_agent = "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
    opt_prefs = {
        'intl.accept_languages': 'en,en_US',
        'profile.default_content_setting_values':
            {
                'cookies': 2, 'images': 2,
                'plugins': 2, 'popups': 2, 'geolocation': 2,
                'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 2,
                'mouselock': 2, 'mixed_script': 2, 'media_stream': 2,
                'media_stream_mic': 2, 'media_stream_camera': 2, 'protocol_handlers': 2,
                'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2,
                'push_messaging': 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop': 2,
                'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement': 2,
                'durable_storage': 2
            }
        }


    # Metamask data
    metamask_folder = "metamask"
    metamask_file = metamask_env_file
    metamask_path = '{}/{}/{}'.format(kw_bot_dir,metamask_folder,metamask_file)

    # prefer user path before downloaded one
    driver_path = env_driver_path

    # Start WebDriver
    chrome_options = webdriver.ChromeOptions()


    chrome_options.add_argument('disable-infobars')
    # chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # chrome_options.add_experimental_option('useAutomationExtension', False)
    # chrome_options.add_argument('--disable-gpu')
    # # chrome_options.add_argument("window-size=1920,1080")
    #
    # chrome_options.headless = True




    # Add metamask
    chrome_options.add_extension(metamask_path)

    # chrome_options.headless = True

    # For ChromeDriver version 79.0.3945.16 or over
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')

    # Change Browser Options
    chrome_options.add_argument(opt_window_size)
    chrome_options.add_argument(opt_user_agent)

    # set language and other
    chrome_options.add_experimental_option('prefs', opt_prefs)

    # start Chrome
    browser = webdriver.Chrome(
        executable_path=driver_path,
        options=chrome_options
    )

    # page delay
    browser.implicitly_wait(page_delay)


    return browser, err_msg
