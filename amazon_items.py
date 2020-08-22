from typing import Tuple, List, Union, Optional
from selenium.webdriver.common.action_chains import ActionChains
from automation_functions import (get_driver, check_xpath_element, quit_chromium, scroll_down,
                                  webdriver, operating_system, user_name, sleep)
from xpath_strings import (amazon_search_label, amazon_four_star_button, amazon_product_star_ratings_label,
                           amazon_product_num_reviews_text, amazon_product_five_star_text,
                           amazon_product_four_star_text, amazon_product_price_text, amazon_product_name_text,
                           amazon_product_results, amazon_product_avg_rating, amazon_next_button)


def get_links(search: str) -> List[str]:
    print("Getting product links...")
    url_product_links: List[str] = []
    RETURN_KEY: str = "\ue006"
    driver.get("https://www.amazon.com/")
    check_xpath_element(driver, amazon_search_label).send_keys(search)
    check_xpath_element(driver, amazon_search_label).send_keys(RETURN_KEY)
    check_xpath_element(driver, amazon_four_star_button).click()
    scroll_down(driver)

    next_page: int = 1
    product_result: int = 1
    while True:
        anchor_tag_product: Optional[webdriver.remote] = check_xpath_element(driver, amazon_product_results.format(
            product_result))

        if anchor_tag_product is None:
            if next_page == max_num_of_pages:
                break
            else:
                product_result = 1
                next_page += 1
                check_xpath_element(driver, amazon_next_button).click()
                sleep(1)
                continue

        url_product: str = anchor_tag_product.get_attribute("href")
        print(url_product)

        if url_product not in url_product_links:
            url_product_links.append(url_product)
            if product_result % 4 == 0:
                scroll_down(driver, 235)
                print(len(url_product_links))

        product_result += 1

    print(len(url_product_links))
    return url_product_links


def open_product_links(url_links: List[str]) -> None:
    driver.get("https://www.google.com/")
    url_link: str
    for url_link in url_links:
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(url_link)
        get_product_info(url_link)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    quit_chromium(driver)


def get_product_info(link: str) -> None:
    print("Getting product info...")

    if hover_over_star_ratings():
        return

    avg_rating: str = get_avg_rating(link)
    product_price: str = get_product_price(link)

    total_number_of_reviews: int = check_number(driver, amazon_product_num_reviews_text)
    five_star_num_reviews: int = round(total_number_of_reviews * get_number_percent(amazon_product_five_star_text))
    four_star_num_reviews: int = round(total_number_of_reviews * get_number_percent(amazon_product_four_star_text))
    laplace_distribution: float = round((five_star_num_reviews + four_star_num_reviews + 1) /
                                        (total_number_of_reviews + 2), 2)

    if price_range[0] <= float(product_price.split("$")[1]) <= price_range[1] and laplace_distribution >= min_laplace \
            and total_number_of_reviews >= min_reviews:
        print("Writing product info...")
        with open(get_desktop_path(), "a") as file:
            file.write(f"Name: {check_xpath_element(driver, amazon_product_name_text).text}\n")
            file.write(f"Price: {product_price}\n")
            file.write(f"Average Score: {avg_rating}\n")
            file.write(f"Reviews: {total_number_of_reviews}\n")
            file.write(f"Laplace Distribution: {laplace_distribution}\n")
            file.write(f"Link: {link}\n")
            file.write("\n")


def get_number_percent(star_rating: str) -> Union[int, float]:
    percent: Optional[webdriver.remote] = check_xpath_element(driver, star_rating)
    if percent is None:
        return 0
    else:
        return round(float(percent.text.split("%")[0]) / 100, 2)


def check_number(web_driver, number: str) -> int:
    num: Optional[webdriver.remote] = check_xpath_element(web_driver, number)
    if num is None:
        exit(1)

    num: str = num.text.split(" ")[0]
    if "," in num:
        return int(num.replace(",", ""))


def get_desktop_path() -> str:
    if operating_system() == "Windows":
        return f"C:\\Users\\{user_name()}\\Desktop\\amazon_report.txt"
    else:
        return f"/Users/{user_name()}/Desktop/amazon_report.txt"


def hover_over_star_ratings() -> Optional[bool]:
    try:
        ActionChains(driver).move_to_element(check_xpath_element(driver, amazon_product_star_ratings_label)).perform()
    except AttributeError:
        return True


def get_avg_rating(link: str) -> str:
    avg_rating: Optional[webdriver.remote] = check_xpath_element(driver, amazon_product_avg_rating)

    if avg_rating is None:
        print("Avg Rating " + link)
        return "0 out of 5"
    else:
        return avg_rating.text


def get_product_price(link: str) -> str:
    product_cost: Optional[webdriver.remote] = check_xpath_element(driver, amazon_product_price_text)

    if product_cost is None:
        print("Product Price " + link)
        return "$0"
    else:
        product_price: str = product_cost.text

        if not product_price:
            return "$0"

        if "," in product_price:
            product_price = product_price.replace(",", "")

    return product_price


driver: webdriver = get_driver()
driver.maximize_window()
max_num_of_pages: int = 1
product_links: List[str] = get_links("diffuser oils")

min_reviews: int = 50
min_laplace: float = 0.85
price_range: Tuple[int, int] = (0, 75)

open_product_links(product_links)
