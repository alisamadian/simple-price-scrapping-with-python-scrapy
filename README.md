# Simple Product Spider with python and Scrapy for extracting name and price

A lightweight web scraping tool built with Scrapy and Python.
It can be used to extract product names and prices from e-commerce websites.
Currently configured for WooCommerce-based websites but easily adaptable to other platforms.

## Features

- Extracts product names and prices from e-commerce websites
- Handles infinite scroll or pagination automatically
- Avoids duplicate products
- Exports data to CSV (supports other formats too)
- Configurable user agent and request settings

## Prerequisites

- Python 3.6 or higher installed
- pip (Python package installer)

## Usage

1. In your terminal, Install scrapy:
   ```bash
   pip install scrapy
   ```
2. Run the spider with the following command:
   ```bash
   scrapy runspider productspider.py
   ```

3. You should customize some values in the code to make it work as show below.

## Customization

### Changing the target website
To scrape a different website, modify the start_urls list in the ProductSpider class:
```python
start_urls = ["https://example.com/shop/"]
```
Remember, there are other places you should change "example.com" in the code, so search for it.

### Adjusting CSS selectors
The current selectors are configured for WooCommerce sites.
```python
products = response.css("div.wd-product")
```

You may need to adjust them based on the structure of your target website:
```python
name = product.css("h3.wd-entities-title a::text").get()
price = product.css("span.woocommerce-Price-amount bdi::text").get()
```

### Selecting the desired columns
 You should select the columns in the code based on the structure of your target website:
```python
name = name.strip()
price = price.strip()
```

### Modifying pagination
The pagination logic can be adjusted based on the website's structure:
```python
next_page = f"https://example.com/shop/page/{self.page}/"
```

## Output Format
The data will be saved named products.csv in the same directory, with the following columns:
- name: The product name
- price: The product price

## License
MIT License