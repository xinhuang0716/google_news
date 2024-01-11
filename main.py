## import packages
import json, requests, pandas as pd
from bs4 import BeautifulSoup


## query function
def main(config_path: str = "./data/config/config.json"):
    """
    return google search results as excel file
    """
    # load configs
    data = json.load(open("./data/config/config.json"))
    url, query_chunk = data["url"], data["query_chunk"]
    url = url.replace("**query_chunk**", query_chunk)

    # query
    item = BeautifulSoup(requests.get(url).text, "xml").find_all("item")
    df = pd.DataFrame.from_dict(
        [
            {
                "title": item[i].find("title").text.split(" - ")[0],
                "date": item[i].find("pubDate").text,
                "source": item[i].find("source").text,
                "link": item[i].find("link").text,
            }
            for i in range(len(item))
        ]
    )
    print("completed")
    return df.to_excel(f"./data/result/result_{query_chunk}.xlsx", index=False)


if __name__ == "__main__":
    main()
