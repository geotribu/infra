#! python3  # noqa: E265

# standard library
import json
import logging
import sys
from pathlib import Path
from pprint import pprint
from urllib.request import Request, urlopen

# 3rd party
from lunr.index import Index

# -- VARIABLES ---------------------------------------------------------------
index_file: str = "https://cdn.geotribu.fr/img/search-index.json"
user_agent: str = "Python urllib/3 Testing Geotribu search index"

# -- MAIN --------------------------------------------------------------------

# local or remote
if index_file.startswith("http"):
    # build request
    request = Request(
        url=index_file, headers={"User-Agent": user_agent, "Accept": "application/json"}
    )

    with urlopen(index_file) as response:
        serialized_idx = json.loads(response.read())
else:
    local_index: Path = Path(index_file)
    # checks
    if not local_index.exists():
        logging.error(f"{local_index.resolve()} does not exist")
        sys.exit(f"{local_index.resolve()} does not exist")
    # loads it
    with local_index.open("idx.json") as fd:
        serialized_idx = json.loads(fd.read())


# charge l'index sérialisé
idx = Index.load(serialized_idx.get("index"))
images_dict = serialized_idx.get("images")

# recherche
search_results_low: list[dict] = idx.search("*satellite*")

extended_results = []

for search_result in search_results_low:
    mapped_img = images_dict.get(search_result.get("ref"))
    search_result.update({"width": mapped_img[0], "height": mapped_img[1]})

pprint(search_results_low)

# search_results_up = idx.search("PYT*")
# pprint(search_results_up)


# print(search_results_low == search_results_up)
