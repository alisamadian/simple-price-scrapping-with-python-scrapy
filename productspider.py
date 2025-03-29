# You should have Python installed on your systems. 
# Scrapy is a library for web scraping. You can install it with this command "pip install scrapy".
# To do this, search "download Python windows" or your operating system.
# Then, get the the most stable version (not the latest version), and also longer time supported by them (LTS).

# Import necessary libraries
import scrapy  

class ProductSpider(scrapy.Spider):
    """A Scrapy spider designed to scrape product information from a e-commerce website.
    Right now it works on WooCommerce-based websites with wordpress.
    But can easily implemented with any website you want easily.
    
    This spider crawls through product pages, extracts product names and prices,
    And saves the data to a CSV file while avoiding duplicate products.
    """
    
    name = "productspider"
    
    # Starting URL(s) - where the spider begins crawling
    # This is a WooCommerce shop page on a WordPress site
    start_urls = ["https://example.com/shop/"]
    
    # Page counter for pagination
    page = 1
    
    # Set to track already scraped items and avoid duplicates
    seen_items = set()

    # Custom settings for this spider
    custom_settings = {
        # User agent to mimic a real browser.
        # Alternative options: You can use different browser user agents like Firefox, Safari, or mobile devices.
        # All of them are available on the internet.
        # It is suggested to use dynamic user agents to make code more robust.
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        
        # Output settings
        # It defines how and where to save the scraped data.
        "FEEDS": {
            # Output file name which is a dictionary
            "products.csv": {
                # Format of the output file
                # Alternative options: 'json', 'jsonlines', 'xml', 'pickle', etc.
                "format": "csv",
                
                # Encoding for the output file
                # The UTF-8-sig includes a BOM (Byte Order Mark) which helps Excel open the file correctly
                # Alternative options: 'utf-8' (without BOM), 'latin1', 'ascii', etc.
                "encoding": "utf-8-sig",
                
                # Whether to overwrite the file if it already exists
                # Alternative option: False (to append to existing file)
                "overwrite": True,
                
                # Fields to include in the output
                # You can add more fields here if you extract additional data.
                "fields": ["name", "price"]
            }
        }
        # Other possible settings you could add:
        # "CONCURRENT_REQUESTS": 16,  # Number of concurrent requests
        # "DOWNLOAD_DELAY": 1,       # Delay between requests in seconds
        # "COOKIES_ENABLED": False,  # Whether to enable cookies
        # "ROBOTSTXT_OBEY": True,    # Whether to obey robots.txt rules
        # "RETRY_ENABLED": True,
        # "RETRY_TIMES": 2,
        # "RETRY_HTTP_CODES": [500, 502, 503, 504, 408],
        # "HTTPERROR_ALLOWED_CODES": [404, 403],
    }

   
    def parse(self, response):
        """Parse the response and extract product information.
        
        This method is called for each URL in start_urls and for each URL yielded by callback methods.
        """
        # Debugging section - Uncomment to save the HTML response for inspection.
        # This is useful when you need to analyze the page structure or debug issues.
        # The saved HTML can be opened in a browser to see what the spider is seeing.
        # with open("response.html", "wb") as f:
        #     f.write(response.body)

        # Get all products using CSS selector.
        # You can use xpath for getting products but i leave that to you.
        products = response.css("div.wd-product")
        self.logger.info(f'Found {len(products)} products on page {self.page}')

        # Process each product
        for product in products:
            # Extract product name and price using CSS selectors specific to WooCommerce
            # The ::text pseudo-element extracts the text content of the matched elements
            # The style of selecting is easy to understand based on the structure on developer options
            name = product.css("h3.wd-entities-title a::text").get()
            price = product.css("span.woocommerce-Price-amount bdi::text").get()
            
            # Only process items where both name and price were found.
            # So we skip the not available products.
            # But you should handle the on sale products which have different elements for the price.
            if name and price:
                # Clean up extracted data by removing extra whitespace
                name = name.strip()
                price = price.strip()
                
                # Combine these two variables and create an identifier.
                # Alternative approaches could include using product IDs if available.
                # Remember, using name_price as a unique identifier might skip valid products with identical names and prices.
                item_identifier = f"{name}_{price}"
                
                # Check if we've seen this item before to avoid duplicates
                if item_identifier not in self.seen_items:
                    # Add to seen items set
                    self.seen_items.add(item_identifier)

                    # Yield the item to be processed by Scrapy's pipeline
                    yield {
                        "name": name,
                        "price": price
                        # You could add more fields here such as:
                        # "url": product.css("a::attr(href)").get(),
                        # "image": product.css("img::attr(src)").get(),
                        # "description": product.css(".description::text").get()
                    }
                else:
                    # Log duplicate items at debug level
                    self.logger.debug(f'Skipping duplicate item: {name}')


        # Pagination handling - Here we check for the "Load More" button.
        # This part is pretty flexible and websites can use pages of products instead of infinite scrolling.
        load_more = response.css('a.wd-load-more.wd-products-load-more::attr(href)').get()

        if load_more:
            # Increment page counter
            self.page += 1

            # Construct next page URL
            # This follows WooCommerce's pagination pattern: /shop/page/2/, /shop/page/3/, etc.
            next_page = f"https://example.com/shop/page/{self.page}/"
            self.logger.info(f'Moving to page {self.page}: {next_page}')

            # Make a new request to the next page
            yield scrapy.Request(
                url=next_page,
                callback=self.parse,
                # Use the same parse method for the next page.
                # Headers to mimic AJAX request as WooCommerce often uses AJAX for pagination
                headers={
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'text/html, */*; q=0.01'
                }
                # The code assumes WooCommerce’s /page/{num}/ structure.
                # If the target site uses query parameters (e.g., ?page=2), the next_page logic will fail.
                # In that case, modify the code as you wish.
                # meta={'dont_redirect': True},  # Control redirects
                # cookies={},                    # Add specific cookies
                # dont_filter=False,             # Control URL filtering
            )
        # Note: An alternative pagination approach for sites without "Load More":
        # next_page = response.css('a.next.page-numbers::attr(href)').get()
        # if next_page:
        #     yield scrapy.Request(url=next_page, callback=self.parse)





