#! python3  # noqa: E265

# standard library
import json
import logging
import sys
from configparser import ConfigParser
from math import floor
from math import log as math_log
from os.path import expanduser, expandvars
from pathlib import Path

# 3rd party
import imagesize
from lunr import lunr

# -- VARIABLES ---------------------------------------------------------------
configuration_file: Path = Path(__file__).parent / "images-indexer.ini"
start_folder: Path = Path.home() / "Images"
extensions_to_index: tuple = (".gif", ".jpg", ".jpeg", ".png", ".svg", ".webp")
images_list: list[dict] = []
images_dict: dict = {}

# -- FUNCTIONS ---------------------------------------------------------------


def convert_octets(octets: int) -> str:
    """Convert a mount of octets in readable size.
    :param int octets: mount of octets to convert
    :Example:
    .. code-block:: python
        >>> convert_octets(1024)
        "1ko"
    """
    # check zero
    if octets == 0:
        return "0 octet"

    # conversion
    size_name = ("octets", "Ko", "Mo", "Go", "To", "Po")
    i = int(floor(math_log(octets, 1024)))
    p = pow(1024, i)
    s = round(octets / p, 2)

    return "{} {}".format(s, size_name[i])


# -- MAIN --------------------------------------------------------------------

# charge la configuration ou utilise les varibles par défaut
if configuration_file.exists():
    # read ini file
    config = ConfigParser()
    with configuration_file.open("r") as config_file:
        config.read_file(config_file)
    # parse and store variables
    start_folder = Path(expandvars(expanduser(config.get("global", "TARGET_FOLDER"))))
    extensions_to_index = tuple(config.get("global", "EXTENSIONS_TO_INDEX").split(","))
    logging.basicConfig(
        level=int(config.get("global", "LOG_LEVEL")),
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    console = logging.StreamHandler()
    console.setLevel(int(config.get("global", "LOG_LEVEL")))
    logging.getLogger("").addHandler(console)
    logging.info("Configuration file loaded.")
else:
    logging.warning(
        f"Configuration file not found: {configuration_file.resolve()}. Using default values."
    )

# checks
if not start_folder.is_dir():
    sys.exit(f"{start_folder.resolve()} is not a directory")

# déduit le nom du fichier de sortie
output_filepath: Path = start_folder / "search-index.json"

logging.info(
    f"Parameters: \n\tParent folder: {start_folder} \n\tExtensions to index: {extensions_to_index} \n\tOutput filepath: {output_filepath}"
)

# parse file structure
for file in start_folder.glob("**/*"):
    if file.suffix in extensions_to_index:
        # print(file.name, file.parents[0])

        # get image dimensions
        try:
            width, height = imagesize.get(file)
        except ValueError as exc:
            logging.error(f"Invalid image: {file.resolve()}. Trace: {exc}")
            width, height = -1, -1
        except Exception as exc:
            logging.error(
                f"Something went wrong reading the image: {file.resolve()}. Trace: {exc}"
            )
            width, height = -1, -1
        # print(width)

        # store image metadata as a dict into documents list
        images_list.append(
            {
                "name": file.stem,
                "img_type": file.suffix,
                "path": str(file.relative_to(start_folder)),
                "width": width,
                "height": height,
            }
        )

        images_dict[str(file.relative_to(start_folder))] = width, height

# create index
idx = lunr(
    ref="path",
    fields=[dict(field_name="name", boost=10), "img_type", "path"],
    documents=images_list,
)

output_dict = {"images": images_dict, "index": idx.serialize()}


# exporte en JSON
output_filepath: Path = start_folder / "search-index.json"
with output_filepath.open(mode="w") as fd:
    if int(config.get("global", "LOG_LEVEL")) == logging.DEBUG:
        prettify = 4
    else:
        prettify = 0

    json.dump(output_dict, fd, indent=prettify, sort_keys=True, separators=(",", ":"))

logging.info(
    f"Index created: {output_filepath}.\n\tSize: {convert_octets(output_filepath.stat().st_size)}"
)
