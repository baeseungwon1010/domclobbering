import sys
import time
import os
from pathlib import Path
from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

DEFAULT_FLAG = os.environ.get("MY_FLAG", "CTF{**redected**}")


def visit(url: str) -> None:
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=opts)

    try:
        driver.set_page_load_timeout(15)
        flag = load_flag()

        parsed = urlparse(url)
        base = f"{parsed.scheme}://{parsed.netloc or 'localhost:5000'}"

        driver.get(base)
        driver.add_cookie(
            {
                "name": "FLAG",
                "value": flag,
                "domain": parsed.hostname or "localhost",
                "path": "/",
                "httpOnly": False,
                "secure": False,
            }
        )

        driver.get(url)

        time.sleep(5)
    finally:
        driver.quit()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python bot.py <url>")
        sys.exit(1)
    visit(sys.argv[1])

