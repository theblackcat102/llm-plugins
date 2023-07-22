import re
from duckduckgo_search import DDGS


class DuckDuckGo:
    url_pattern = r"^(?:https?:\/\/)?(?:www\.)?([^\/]+)"

    prompt = """
    Web search: a function which allows you to search the web and reference based on the result.
    function: Search(query)
    parameters :
       - query: a string of query text
    returns: a list of serp results
    """

    def __init__(self, proxies=None) -> None:
        self.prompt = self.prompt.replace("    ", "")
        self.proxies = proxies

    def __call__(self, query):
        results = []
        index = 1
        with DDGS(self.proxies, timeout=20) as ddgs:
            for r in ddgs.text(query):
                if len(results) > 8:
                    break
                match = re.match(self.url_pattern, r["href"])
                if match:
                    domain = match.group(1)
                    results.append(
                        f"<|{index}|> title: {r['title']}\ndomain: {domain}\nbody: {r['body']}"
                    )
                else:
                    results.append(
                        f"<|{index}|> title: {r['title']}\nbody: {r['body']}"
                    )
                index += 1
        return "\n".join(results)
