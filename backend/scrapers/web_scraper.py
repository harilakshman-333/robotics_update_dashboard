import asyncio
from typing import List, Dict, Any
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from backend.database import SessionLocal
from backend.models.feed_item import FeedItem
from sqlalchemy import select

async def is_url_in_db(url: str) -> bool:
    async with SessionLocal() as session:
        result = await session.execute(select(FeedItem).where(FeedItem.url == url))
        return result.scalar_one_or_none() is not None

async def scrape_ieee_spectrum() -> List[Dict[str, Any]]:
    url = "https://spectrum.ieee.org/tag/robotics"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        html = await page.content()
        soup = BeautifulSoup(html, "html.parser")
        articles = soup.select("article")
        items = []
        for article in articles:
            a = article.find("a", href=True)
            if not a:
                continue
            article_url = a["href"]
            if not article_url.startswith("http"):
                article_url = "https://spectrum.ieee.org" + article_url
            if await is_url_in_db(article_url):
                continue
            title = a.get_text(strip=True)
            # Visit article page for body
            article_page = await browser.new_page()
            await article_page.goto(article_url)
            article_html = await article_page.content()
            article_soup = BeautifulSoup(article_html, "html.parser")
            body = article_soup.get_text()
            body = body[:3000]
            items.append({
                "title": title,
                "url": article_url,
                "raw_text": body,
                "source": "web"
            })
            await article_page.close()
        await browser.close()
        return items

async def scrape_robot_report() -> List[Dict[str, Any]]:
    url = "https://therobotreport.com"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        html = await page.content()
        soup = BeautifulSoup(html, "html.parser")
        articles = soup.select(".jeg_postblock_content .jeg_post_title a")
        items = []
        for a in articles:
            article_url = a["href"]
            if await is_url_in_db(article_url):
                continue
            title = a.get_text(strip=True)
            article_page = await browser.new_page()
            await article_page.goto(article_url)
            article_html = await article_page.content()
            article_soup = BeautifulSoup(article_html, "html.parser")
            body = article_soup.get_text()
            body = body[:3000]
            items.append({
                "title": title,
                "url": article_url,
                "raw_text": body,
                "source": "web"
            })
            await article_page.close()
        await browser.close()
        return items

async def scrape_arxiv_robotics() -> List[Dict[str, Any]]:
    url = "https://arxiv.org/list/cs.RO/recent"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        html = await page.content()
        soup = BeautifulSoup(html, "html.parser")
        items = []
        for dt in soup.select("dl > dt"):
            id_link = dt.find("a", title="Abstract")
            if not id_link:
                continue
            article_url = "https://arxiv.org" + id_link["href"]
            if await is_url_in_db(article_url):
                continue
            dd = dt.find_next_sibling("dd")
            title = dd.find("div", class_="list-title mathjax").get_text(strip=True).replace("Title:", "").strip()
            abstract = dd.find("p", class_="mathjax").get_text(strip=True)
            body = abstract[:3000]
            items.append({
                "title": title,
                "url": article_url,
                "raw_text": body,
                "source": "web"
            })
        await browser.close()
        return items

async def fetch_web_news() -> List[Dict[str, Any]]:
    ieee, robot_report, arxiv = await asyncio.gather(
        scrape_ieee_spectrum(),
        scrape_robot_report(),
        scrape_arxiv_robotics()
    )
    return ieee + robot_report + arxiv
