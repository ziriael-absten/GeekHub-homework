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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


url = "https://robotsparebinindustries.com/"
orders_url = url + "orders.csv"


class Order:
    def __init__(self, order_number, head, body, legs, address):
        self.order_number = order_number
        self.head = head
        self.body = body
        self.legs = legs
        self.address = address

    def __repr__(self):
        return f"Order(order_number={self.order_number}, head={self.head}, body={self.body}, legs={self.legs}, address='{self.address}')"


class RobotOrder:
    def __init__(self, driver, output_directory):
        self.driver = driver
        self.output_directory = output_directory

    def run(self):
        self.create_output_directory()
        orders = self.load_orders()
        if orders is None:
            print("Error loading orders, exiting")
            return
        for order in orders:
            self.process_order(order)
            time.sleep(1)

    def create_output_directory(self):
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)
        else:
            files = os.listdir(self.output_directory)
            for file in files:
                os.remove(os.path.join(self.output_directory, file))

    def load_orders(self):
        response = requests.get(orders_url)
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
                    address=row[4],
                )
                orders.append(order)

            return orders
        else:
            print(f"Не вдалося завантажити файл. Код відповіді: {response.status_code}")
            return None

    def fill_order_data(self, order):
        head_dropdown = Select(driver.find_element(By.NAME, "head"))
        head_dropdown.select_by_value(order.head)
        body_radio = self.driver.find_element(
            By.XPATH, f"//input[@name='body' and @value='{order.body}']"
        )
        body_radio.click()

        legs_input = self.driver.find_element(
            By.XPATH, '//label[text()="3. Legs:"]/following-sibling::input'
        )
        legs_input.clear()
        legs_input.send_keys(order.legs)

        address_input = self.driver.find_element(By.NAME, "address")
        address_input.clear()
        address_input.send_keys(order.address)

    def close_popup(self):
        order_tab = self.driver.find_element(
            By.XPATH, "//a[contains(text(),'Order your robot')]"
        )
        order_tab.click()
        pop_up = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "modal-dialog"))
        )
        button = self.driver.find_element(By.XPATH, "//button[contains(text(),'OK')]")
        button.click()

    def perform_order(self):
        order_button = self.driver.find_element(By.ID, "order")
        while True:
            order_button.click()
            message = self.driver.find_elements(By.CLASS_NAME, "alert-danger")
            if message:
                continue
            break

        check_element = self.driver.find_element(By.CLASS_NAME, "badge-success")
        check_number = check_element.text.strip()
        check_number = check_number.split("-")[-1]
        return check_number

    def process_order(self, order):
        print(f"processing order {order.order_number}")
        self.driver.get("https://robotsparebinindustries.com/")
        try:
            self.close_popup()
        except Exception as e:
            print(f"Cannot close popup: {e}")
        self.fill_order_data(order)
        time.sleep(1)
        self.save_robot_image(order.order_number)
        check_number = self.perform_order()
        self.rename_image(order.order_number, check_number)

    def make_screenshot_name(self, order_number):
        return os.path.join(self.output_directory, f"{order_number}.png")

    def save_robot_image(self, order_number):
        try:
            self.driver.execute_script("window.scrollBy(0, 500)")
            time.sleep(2)
            preview_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "preview"))
            )
            preview_button.click()

            image_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "robot-preview-image"))
            )
            time.sleep(2)
            element_screenshot = image_element.screenshot_as_png

            with open(self.make_screenshot_name(order_number), "wb") as file:
                file.write(element_screenshot)

        except Exception as e:
            print("Exception class ", type(e))
            print(f"Помилка при збереженні зображення: {e}")

    def rename_image(self, order_number, check_name):
        os.rename(
            self.make_screenshot_name(order_number),
            self.make_screenshot_name(check_name),
        )


if __name__ == "__main__":
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    robot_order = RobotOrder(driver, "output")
    try:
        robot_order.run()
    finally:
        driver.quit()
