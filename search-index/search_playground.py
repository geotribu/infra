#! python3  # noqa: E265

# standard library
import json
import logging
import sys
from datetime import datetime, timedelta
from math import floor
from math import log as math_log
from pathlib import Path
from pprint import pprint
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

# 3rd party
from lunr.index import Index

# -- LOGGING ------------------------------------------------------------------
# levels: 10 = debug, 20 = info, 30 = warning, 40 = error
log_level: int = 10

logging.basicConfig(
    level=log_level,
    format="%(asctime)s||%(levelname)s||%(module)s||%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    force=1,
)

logging.debug(f"Log level: {logging.getLevelName(log_level)}")


# -- VARIABLES ---------------------------------------------------------------
base_url: str = "https://cdn.geotribu.fr/img/"
index_remote_file: str = f"{base_url}/search-index.json"
index_local_file: Path = Path().home() / ".geotribu/search/cdn_search_index.json"
index_rotating_hours: int = 1
user_agent: str = "Python urllib/3 Testing Geotribu search index"


# -- FUNCTIONS ---------------------------------------------------------------


def convert_octets(octets: int) -> str:
    """Convert a mount of octets in readable size.

    :param int octets: mount of octets to convert

    :Example:
    .. code-block:: python
        >>> convert_octets(1024)
        "1ko"
        >>> from pathlib import Path
        >>> convert_octets(Path(my_file.txt).stat().st_size)
    """
    # check zero
    if octets == 0:
        return "0 octet"

    # conversion
    size_name = ("octets", "Ko", "Mo", "Go", "To", "Po")
    i = int(floor(math_log(octets, 1024)))
    p = pow(1024, i)
    s = round(octets / p, 2)

    return f"{s} {size_name[i]}"


def download_search_index(
    url_index_to_download: str = index_remote_file,
    local_file_path: Path = index_local_file,
    expiration_rotating_hours: int = index_rotating_hours,
    user_agent: str = user_agent,
) -> Path:
    """Check if the local index file exists. If not, download the search index from remote URL.
    If it does exist, check if it has been modified

    :param str url_index_to_download: remote URL of the search index, defaults to index_remote_file
    :param Path local_file_path: local path to the index file, defaults to index_local_file
    :param int expiration_rotating_hours: number in hours to consider the local file outaded, defaults to index_rotating_hours
    :param str user_agent: user agent to use to perform the request, defaults to user_agent

    :return Path: path to the local index file (should be the same as local_file_path)
    """
    # content search index
    if local_file_path.exists():
        f_creation = datetime.fromtimestamp(local_file_path.stat().st_ctime)
        if (datetime.now() - f_creation) < timedelta(hours=expiration_rotating_hours):
            logging.info(
                f"Local search index ({local_file_path}) is up to date. "
                "No download needed.",
            )
            return local_file_path
        else:
            logging.info(
                f"Local search index ({local_file_path}) is outdated: "
                f"updated more than {expiration_rotating_hours} hour(s) ago. "
                "Let's remove and download it again from remote."
            )
            local_file_path.unlink(missing_ok=True)

    # download the remote file into local
    custom_request = Request(
        url=url_index_to_download,
        headers={"User-Agent": user_agent, "Accept": "application/json"},
    )

    try:
        with urlopen(custom_request) as response:
            with local_file_path.open(mode="wb") as tmp_file:
                tmp_file.write(response.read())
        logging.info(
            f"Téléchargement du fichier distant {url_index_to_download} dans {local_file_path} a réussi."
        )
    except HTTPError as error:
        return error
    except URLError as error:
        return error
    except TimeoutError as error:
        return error

    return local_file_path


# -- MAIN --------------------------------------------------------------------

index_local_file.parent.mkdir(parents=True, exist_ok=True)

# get local search index
get_or_update_local_search_index = download_search_index(
    url_index_to_download=index_remote_file,
    local_file_path=index_local_file,
    expiration_rotating_hours=24,
    user_agent=user_agent,
)
if not isinstance(get_or_update_local_search_index, Path):
    logging.error(
        f"Le téléchargement du fichier distant {index_remote_file} "
        f"ou la récupération du fichier local {index_local_file} a échoué."
    )
    if isinstance(get_or_update_local_search_index, Exception):
        logging.error(get_or_update_local_search_index)
    sys.exit()
logging.info(
    f"Local index file: {index_local_file}, {convert_octets(index_local_file.stat().st_size)}"
)

# load the local index file
if not index_local_file.exists():
    logging.error(f"{index_local_file.resolve()} does not exist")
    sys.exit(f"{index_local_file.resolve()} does not exist")
# loads it
with index_local_file.open("r") as fd:
    serialized_idx = json.loads(fd.read())


# charge l'index sérialisé
idx = Index.load(serialized_idx.get("index"))
images_dict = serialized_idx.get("images")

# recherche
search_results: list[dict] = idx.search("*satellite*")

extended_results = []

for search_result in search_results:
    mapped_img = images_dict.get(search_result.get("ref"))
    search_result.update(
        {
            "width": mapped_img[0],
            "height": mapped_img[1],
            "full_url": f"{base_url}{search_result.get('ref')}",
        }
    )

pprint(search_results)

# pprint(idx.search("satellite"))

pprint(len(idx.search("qgis")))
print("\n\n")
pprint(len(idx.search("name:qgis")))
pprint(idx.search("+path:logo +name:qgis"))
pprint(idx.search("openstreetmap logo"))
pprint(idx.search("+openstreetmap +logo"))
