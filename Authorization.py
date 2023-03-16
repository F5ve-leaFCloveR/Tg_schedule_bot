from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import configparser
import sys


# authorization on class using selenium
def authorization_lk():

    config = configparser.ConfigParser()
    try: # попытка чтения cfg файла с токеном
        config.read('.gitignored/login.cfg')
    except FileNotFoundError:
        print('Error: token.cfg file not found')
        sys.exit(1)
    except configparser.Error as e:
        print(f'Error parsing token.cfg file: {e}')
        sys.exit(1)

    try: # получение логина и пароля из cfg файла
        username = config['Login']['username']
        password = config['Login']['password']
    except KeyError:
        print('Error: "token" not found in token.cfg file')
        sys.exit(1)

    login_url = "https://lk.sut.ru/cabinet/?login=no"
    
    driver = webdriver.Chrome()
    driver.get(login_url)

    # login
    driver.find_element('id', 'users').send_keys(username)
    driver.find_element('id', 'parole').send_keys(password)
    driver.find_element('id', 'logButton').click()

    # navigation on the site
    lodin_first_page = "https://lk.sut.ru/cabinet/?login=yes"
    driver.get(lodin_first_page)
    driver.find_element(By.ID, 'heading1').click()
    driver.find_element('id', 'menu_li_6118').click()

    # authorization on class through table
    for tr in range(2, 40):
        table_cell = driver.find_element(By.XPATH, f"//*[@id='rightpanel']/div[2]/table/tbody/tr[{tr}]/td[6]")
        if table_cell.text == "Начать занятие":
            table_cell.click()
        # проверка, существет ли следующая строка в таблице
        try:
            next_row = driver.find_element(By.XPATH, f"//*[@id='rightpanel']/div[2]/table/tbody/tr[{tr+1}]/td[6]")
            next_clone = driver.find_element(By.XPATH, f"//*[@id='rightpanel']/div/table/tbody/tr[{tr+1}]/td")
        except:
            break
    driver.quit()
    return True