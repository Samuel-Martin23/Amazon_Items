amazon_search_label: str = "//input[@id='twotabsearchtextbox']"
amazon_four_star_button: str = "//section[@aria-label='4 Stars & Up']//parent::node()"
amazon_product_results: str = "(//h2//a[@class='a-link-normal a-text-normal'])[{}]"
amazon_product_star_ratings_label: str = "(//a[@class='a-popover-trigger a-declarative'])[1]"
amazon_product_num_reviews_text: str = "(//span[@id='acrCustomerReviewText'])[1]"
amazon_product_five_star_text: str = "//td[@class='a-text-right a-nowrap']//a[contains(@title, '5 stars')]"
amazon_product_four_star_text: str = "//td[@class='a-text-right a-nowrap']//a[contains(@title, '4 stars')]"
amazon_product_name_text: str = "//span[@id='productTitle']"
amazon_product_price_text: str = "(//*[text()='Price:']//parent::node()//span)[1]"
amazon_product_avg_rating: str = "//span[@class='a-size-medium a-color-base a-text-beside-button a-text-bold']"
amazon_next_button: str = "//*[text()='→']"


"""
amazon_product_link: str = ".//a[@class='a-link-normal a-text-normal']"
if you ever loop over multiple elements 
"""
