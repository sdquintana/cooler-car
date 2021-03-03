from datetime import datetime
from sqlalchemy import exc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
import selenium.webdriver.support.ui as ui
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from src.Models.LuTradeMarkType import LuCarType


engine = create_engine(f'mysql://root:root@127.0.0.1:3306/cooler_car')
Session = sessionmaker(bind=engine)
session = Session()


options = Options()
options.binary_location = '/opt/headless-chromium'
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--single-process')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--homedir=/tmp")

prefs = {'download.default_directory': '/tmp',
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'safebrowsing.enabled': False,
        'behavior': 'allow',
        'downloadPath': '/tmp',
        'safebrowsing.disable_download_protection': True}

options.add_experimental_option("prefs", prefs)

login_url = 'https://www.diariomotor.com/marcas/'
body = "/html/body/div[2]/div[4]/div[2]/div/div"


def click_element(drivers, xpath, file_to_wait):
    print(f'clinking {file_to_wait}')
    click_link = drivers.find_element_by_xpath(xpath)
    click_link.click()


def get_trade_marks():
   with webdriver.Chrome(ChromeDriverManager().install()) as driver:

        wait = ui.WebDriverWait(driver, 100, 1)
        driver.get(login_url)

        element = wait.until(EC.visibility_of_element_located((By.XPATH, body)))

        list_of_marks = element.text.splitlines()

        id = 1
        rows_to_insert = []
        for row in list_of_marks:
            print(row)

            data = {'trade_mark_type_id': id,
                    'code': row.lower(),
                    'description_us': row,
                    'description_es': row,
                    'is_active': 1
                    }
            id = id + 1

            rows_to_insert.append(data)

        session.bulk_insert_mappings(LuCarType, rows_to_insert)
        session.commit()
        session.close()
        print('load trade mark')


if __name__ == '__main__':
    get_trade_marks()
