#! python3  # noqa: E265

# standard library
import json
import logging
import sys
from configparser import ConfigParser
from os.path import expanduser, expandvars
from pathlib import Path

# 3rd party
from lunr import lunr

# -- VARIABLES ---------------------------------------------------------------
configuration_file: Path = Path(__file__).parent / "images-indexer.ini"
start_folder: Path = Path.home() / "Images"
extensions_to_index: tuple = (".gif", ".jpg", ".jpeg", ".png", ".svg", ".webp")
documents: list = []

# -- MAIN --------------------------------------------------------------------

# charge la configuration ou utilise les varibles par défaut
if configuration_file.exists():
    # read ini file
    config = ConfigParser()
    config.read(Path.home() / ".config" / "images-indexer.ini")
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
        documents.append(
            {
                "name": file.name,
                "img_type": file.suffix,
                "path": str(file.relative_to(start_folder)),
            }
        )

# create index
idx = lunr(
    ref="path",
    fields=[dict(field_name="name", boost=10), "img_type", "path"],
    documents=documents,
)

serialized_idx = idx.serialize()

# exporte en JSON
output_filepath: Path = start_folder / "search-index.json"
with output_filepath.open(mode="w") as fd:
    json.dump(serialized_idx, fd)

logging.info(
    f"Index created: {output_filepath}.\n\tSize: {output_filepath.stat().st_size}"
)
