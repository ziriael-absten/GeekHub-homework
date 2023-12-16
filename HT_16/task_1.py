# Автоматизувати процес замовлення робота за допомогою Selenium
# 1. Отримайте та прочитайте дані з "https://robotsparebinindustries.com/orders.csv". Увага! 
# Файл має бути прочитаний з сервера кожного разу при запускі скрипта, не зберігайте файл 
# локально.
# 2. Зайдіть на сайт "https://robotsparebinindustries.com/"
# 3. Перейдіть у вкладку "Order your robot"
# 4. Для кожного замовлення з файлу реалізуйте наступне:
#     - закрийте pop-up, якщо він з'явився. Підказка: не кожна кнопка його закриває.
#     - оберіть/заповніть відповідні поля для замовлення
#     - натисніть кнопку Preview та збережіть зображення отриманого робота. Увага! Зберігати 
# треба тільки зображення робота, а не всієї сторінки сайту.
#     - натисніть кнопку Order та збережіть номер чеку. Увага! Інколи сервер тупить і видає 
# помилку, але повторне натискання кнопки частіше всього вирішує проблему. Дослідіть цей кейс.
#     - переіменуйте отримане зображення у формат <номер чеку>_robot (напр. 123456_robot.jpg). 
# Покладіть зображення в директорію output (яка має створюватися/очищатися під час запуску 
# скрипта).
#     - замовте наступного робота (шляхом натискання відповідної кнопки)

import csv
import os
import time
import requests
from io import StringIO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

output_directory = 'output'

def main():
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    else:
        files = os.listdir(output_directory)
        for file in files:
            os.remove(os.path.join(output_directory, file))
    time.sleep(2)
    orders = load_orders()
    if orders is None:
        print("Error loading orders, exiting")
        return
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()

    try:
        for order in orders:
            order_robot(driver, order)

    finally:
        driver.quit()


def make_screenshot_name(order_number):
    return os.path.join(output_directory, f"{order_number}.png")

def save_robot_image(driver, order_number):
    try:
        driver.execute_script("window.scrollBy(0, 500)")
        time.sleep(2)
        preview_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "preview"))
        )
        preview_button.click()

        image_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "robot-preview-image"))
        )
        time.sleep(2)

        element = driver.find_element(By.ID, "robot-preview-image")
        element_screenshot = element.screenshot_as_png

        with open(make_screenshot_name(order_number), "wb") as file:
            file.write(element_screenshot)

    except Exception as e:
        print("Exception class ", type(e))
        print(f"Помилка при збереженні зображення: {e}")


def load_orders():
    url = "https://robotsparebinindustries.com/orders.csv"
    response = requests.get(url)
    
    if response.status_code == 200:
        csv_data = response.text
        csv_reader = csv.reader(StringIO(csv_data))
        orders = []
        
        next(csv_reader)
        for row in csv_reader:
            order = Order(
                order_number=row[0],
                head=row[1],
                body=row[2],
                legs=row[3],
                address=row[4]
            )
            orders.append(order)
            
        return orders
    else:
        print(f"Не вдалося завантажити файл. Код відповіді: {response.status_code}")
        return None
def order_robot(driver, order):
    print(f"processing order {order.order_number}")
    driver.get("https://robotsparebinindustries.com/")
    order_tab = driver.find_element(By.XPATH, "//a[contains(text(),'Order your robot')]")
    order_tab.click()
    try:
        pop_up = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'modal-dialog'))
        )
        button = driver.find_element(By.XPATH, "//button[contains(text(),'OK')]")
        button.click()
    except Exception as e:
        print(f"Cannot close popup: {e}")
        pass
    head_dropdown = Select(driver.find_element(By.NAME, "head"))
    head_dropdown.select_by_value(order.head)
    body_radio = driver.find_element(By.XPATH, f"//input[@name='body' and @value='{order.body}']")
    body_radio.click()

    legs_input = driver.find_element(By.XPATH, '//label[text()="3. Legs:"]/following-sibling::input')
    legs_input.clear()
    legs_input.send_keys(order.legs)

    address_input = driver.find_element(By.NAME, "address")
    address_input.clear()
    address_input.send_keys(order.address)

    time.sleep(1)
    save_robot_image(driver, order.order_number)

    order_button = driver.find_element(By.ID, "order")
    while True:
        order_button.click()
        message = driver.find_elements(By.CLASS_NAME, "alert-danger")
        if message:
            continue
        break

    check_element = driver.find_element(By.CLASS_NAME, "badge-success")
    check_number = check_element.text.strip()
    check_number = check_number.split("-")[-1]

    rename_image(order.order_number, check_number)
    time.sleep(1)

def rename_image(order_number, check_name):
    os.rename(make_screenshot_name(order_number), make_screenshot_name(check_name))

class Order:
    def __init__(self, order_number, head, body, legs, address):
        self.order_number = order_number
        self.head = head
        self.body = body
        self.legs = legs
        self.address = address

    def __repr__(self):
        return f"Order(order_number={self.order_number}, head={self.head}, body={self.body}, legs={self.legs}, address='{self.address}')"

if __name__ == "__main__":
    main()