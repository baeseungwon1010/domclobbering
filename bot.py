import sys
import time
import os
from pathlib import Path
from urllib.parse import urlparse, quote

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

DEFAULT_FLAG = os.environ.get("MY_FLAG", "CTF{**redected**}")


def load_flag() -> str:
    flag_path = Path("flag.txt")
    if flag_path.exists():
        return flag_path.read_text().strip() or DEFAULT_FLAG
    return DEFAULT_FLAG


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


def visit_payload(content: str) -> None:
    url = f"http://127.0.0.1:5000/xss?content={quote(content)}"
    visit(url)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        visit(sys.argv[1])
    elif len(sys.argv) == 3 and sys.argv[1] == "--payload":
        visit_payload(sys.argv[2])
    else:
        print("Usage: python bot.py <url>  or  python bot.py --payload <content>")
        sys.exit(1)

