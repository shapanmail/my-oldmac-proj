import asyncio
import httpx
from bs4 import BeautifulSoup
from urllib.parse import quote, urljoin, urlparse

from sqlalchemy import false

# Global configuration variables to track crawled pages and max limit
crawled_pages = set()
max_crawled_pages = 200  # Note: it's always good idea to have a limit to prevent accidental endless loops

async def get_page(url, retries=5) -> httpx.Response:
    """Fetch a page with retries for common HTTP and system errors."""
    for attempt in range(retries):
        try:
            async with httpx.AsyncClient(timeout=10, follow_redirects=True, verify=False) as client:
                response = await client.get(url)
                if response.status_code == 200:
                    return response
                else:
                    print(f"Non-200 status code {response.status_code} for {url}")
        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            print(f"Attempt {attempt + 1} failed for {url}: {e}")
        await asyncio.sleep(1)  # Backoff between retries
    return None

async def process_page(response: httpx.Response) -> None:
    """
    Process the HTML content of a page here like store it in a database
    or parse it for content?
    """
    print(f"  processed: {response.url}")
    # ignore non-html results
    if "text/html" not in response.headers.get("content-type", ""):
        return
    # safe_filename = quote(response.url, safe="")
    safe_filename = str(response.url).replace("http://", "").replace("https://", "").replace("/", "_")
    #safe_filename = response.url
    with open(f"{safe_filename}.html", "w") as f:
        f.write(response.text)


async def crawl_page(url: str, limiter: asyncio.Semaphore) -> None:
    """Crawl a page and extract all relative or same-domain URLs."""
    global crawled_pages
    if url in crawled_pages:  # url visited already?
        return
    # check if crawl limit is reached
    if len(crawled_pages) >= max_crawled_pages:
        return

    # scrape the url
    crawled_pages.add(url)
    print(f"crawling: {url}")
    html_content = await get_page(url)
    if not html_content:
        return
    await process_page(html_content)

    # extract all relative or same-domain URLs
    soup = BeautifulSoup(html_content, "html.parser")
    base_domain = urlparse(url).netloc
    urls = []
    for link in soup.find_all("a", href=True):
        href = link["href"]
        absolute_url = urljoin(url, href)
        absolute_url = absolute_url.split("#")[0]  # remove fragment
        if absolute_url in crawled_pages:
            continue
        if urlparse(absolute_url).netloc != base_domain:
            continue
        urls.append(absolute_url)
    print(f"  found {len(urls)} new links")
    # ensure we don't crawl more than the max limit
    _remaining_crawl_budget = max_crawled_pages - len(crawled_pages)
    if len(urls) > _remaining_crawl_budget:
        urls = urls[:_remaining_crawl_budget]

    # schedule more crawling concurrently
    async with limiter:
        await asyncio.gather(*[crawl_page(url, limiter) for url in urls])

async def main(start_url, concurrency=10):
    """Main function to control crawling."""
    limiter = asyncio.Semaphore(concurrency)
    try:
        await crawl_page(start_url, limiter=limiter)
    except asyncio.CancelledError:
        print("Crawling was interrupted")
    finally:
        write_crawled_pages_to_file()

def write_crawled_pages_to_file():
    """Write the contents of crawled_pages to a text file."""
    with open("crawled_pages.txt", "w") as f:
        for page in crawled_pages:
            f.write(f"{page}\n")

if __name__ == "__main__":
    start_url = "http://www.reece.com.au/search/showers-c458"
    asyncio.run(main(start_url))