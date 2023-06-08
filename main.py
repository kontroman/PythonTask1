from collections import deque
from typing import List
import requests
from bs4 import BeautifulSoup
from typing import List
def FindLinks(First: str, Second: str, rate: int) -> List[str] | None:
    BaseWiki = "https://en.wikipedia.org"
    Queue = deque()
    Visited = set()

    Queue.append(([First], 0))
    Visited.add(First)

    while Queue:
        path, depth = Queue.popleft()

        if depth > 5:
            return None

        last_url = path[-1]
        html = Request(last_url, rate)
        URLSFromWiki = WikiLinks(html, BaseWiki)

        for link in URLSFromWiki:
            if link == Second:
                path.append(link)
                return path

            if link not in Visited:
                Visited.add(link)
                new_path = path.copy()
                new_path.append(link)
                Queue.append((new_path, depth + 1))

    return None


def Request(url: str, rate_limit: int) -> str:
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def WikiLinks(html: requests.Response.text, base_url: str) -> List[str]:
    Soup = BeautifulSoup(html, "html.parser")
    main_content = Soup.find("div", {"id": "bodyContent"})
    all_links = main_content.find_all("a", href=True)

    wiki_links = []

    for link in all_links:
        href = link["href"]
        if href.startswith("/wiki/") and ":" not in href:
            full_url = base_url + href
            wiki_links.append(full_url)

    return wiki_links


if __name__ == "__main__":
    FirstURL = "https://en.wikipedia.org/wiki/Isaac_Watt_Boulton"
    SecondURL = "https://en.wikipedia.org/wiki/Grand_Prix_motor_racing"
    Rate = 2;

    shortest_path = FindLinks(SecondURL, FirstURL, Rate)
    if shortest_path:
        print(" -> ".join(shortest_path))
    else:
        print("Цепочка не найдена")
