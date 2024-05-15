from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)


class TopItems:
    def __init__(self):
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get("https://www.alibaba.com/")
        time.sleep(15)
        self.window_before = self.driver.window_handles[0]
        try:
            self.accept = self.driver.find_element(By.CSS_SELECTOR, ".gdpr-agree-btn")
            self.accept.click()
        finally:
            self.categories = []

    def top_categories(self):
        featured = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/div[1]")
        hover = ActionChains(self.driver).move_to_element(featured)
        hover.perform()
        top = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div/div/div/a[1]")
        top.click()
        window_after = self.driver.window_handles[1]
        self.driver.switch_to.window(window_after)
        time.sleep(5)
        categ = self.driver.find_elements(By.CSS_SELECTOR, ".hugo3-util-ellipsis.title")
        lista = [item.text for item in categ]
        self.categories = {n: cat for n, cat in enumerate(lista)}
        print("Alibaba's top 20 ranking categories:")
        print(self.categories)

    def click_categ(self, n):
        try:
            self.accept.click()
            time.sleep(5)
        except:
            pass
        finally:
            categ_links = self.driver.find_elements(By.CSS_SELECTOR, ".card .hugo-dotelement")
            categ_links[n].click()
            time.sleep(5)
            #self.driver.quit()

    def list_items(self):
        items_window = self.driver.window_handles[2]
        self.driver.switch_to.window(items_window)
        time.sleep(5)
        item_list = self.driver.find_elements(By.CSS_SELECTOR, 'a.hugo4-product-pc')
        links = [item.get_attribute('href') for item in item_list]
        img_list = self.driver.find_elements(By.CSS_SELECTOR, 'img.picture-image-5')
        imgs = [item.get_attribute('src') for item in img_list]
        title_list = self.driver.find_elements(By.CSS_SELECTOR, '.hugo4-product-element.subject span')
        titles = [item.get_attribute('title') for item in title_list]
        price_list = self.driver.find_elements(By.CSS_SELECTOR, '.hugo4-product-element.price .hugo3-fw-heavy')
        prices = [item.text for item in price_list]
        order_list = self.driver.find_elements(By.CSS_SELECTOR, '.hugo4-product-element.moq span.moq-number')
        orders = [item.text for item in order_list]
        data_dict = {'Title': titles,
                     'link': links,
                     'img_url': imgs,
                     'price': prices,
                     'min. order': orders[:20]}
        return data_dict


my_bot = TopItems()
my_bot.top_categories()
num = int(input(f"What category are you interested in? (0-{len(my_bot.categories)-1}): "))
while num < 0 or num > len(my_bot.categories)-1:
    num = int(input("Choose an existing category: "))
my_bot.click_categ(num)
data = my_bot.list_items()
print(data)
print(len(data['Title']), len(data['link']), len(data['price']), len(data['min. order']))
print(data['price'])
products = pandas.DataFrame(data)
products.to_csv('products.csv')
