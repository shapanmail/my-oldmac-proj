from llama_index.readers.web import ScrapflyReader

# Initiate ScrapflyReader with your ScrapFly API key
scrapfly_reader = ScrapflyReader(
    api_key="scp-test-2a41252a5c504fd2953b1cbedac4f922",  # Get your API key from https://www.scrapfly.io/
    ignore_scrape_failures=True,  # Ignore unprocessable web pages and log their exceptions
)

scrapfly_scrape_config = {
    "asp": True,  # Bypass scraping blocking and antibot solutions, like Cloudflare
    "render_js": True,  # Enable JavaScript rendering with a cloud headless browser
    "proxy_pool": "public_residential_pool",  # Select a proxy pool (datacenter or residnetial)
    "country": "us",  # Select a proxy location
    "auto_scroll": True,  # Auto scroll the page
    "js": "",  # Execute custom JavaScript code by the headless browser
}

# Load documents from URLs as markdown
# documents = scrapfly_reader.load_data(
#     urls=["http://www.reece.com.au/product/showers-c458/mizu-drift-brass-overhead-shower-200mm-chrome-3-9505038"],
#     scrape_config=scrapfly_scrape_config,  # Pass the scrape config
#     scrape_format="text",  # The scrape result format, either `markdown`(default) or `text`
# )

documents = scrapfly_reader.load_data(
    urls=["https://web-scraping.dev/products"]
)

print(documents)