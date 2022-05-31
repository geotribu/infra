#! python3  # noqa: E265

"""
    Images compressor using Tinify API

    See: https://tinypng.com/developers/reference/python
"""

# standard library
import datetime
import logging
from logging.handlers import TimedRotatingFileHandler
from os import getenv
from pathlib import Path
from sys import exit

# 3rd party
import tinify

# -- VARIABLES ---------------------------------------------------------------
# LOG
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        TimedRotatingFileHandler(
            filename=f"{__file__}.log",
            when="D",
            interval=1,
            backupCount=20,
        )
    ],
)
logging.info(
    f"====== Compressor started {datetime.datetime.now():%Y-%m-%d %H:%M} ======"
)

# API KEY
if not getenv("TINIFY_API_KEY"):
    logging.critical("TINIFY_API_KEY environment variable not set")
    exit("TINIFY_API_KEY environment variable not set")

tinify.key = getenv("TINIFY_API_KEY")
logging.info(f"Tinify API key set: {tinify.key[:5]}...")

# FOLDERS
input_folder: Path = Path("~/Git/Geotribu/website/_to_upload")
if not input_folder.exists():
    logging.critical(f"Input folder {input_folder} not found")
    exit(f"Input folder {input_folder} not found")

output_folder: Path = Path("_tinified")
output_folder.mkdir(parents=True, exist_ok=True)

# SETTINGS
images_extension = (".png", ".jpg", ".jpeg", ".webp")


# -- FUNCTIONS ---------------------------------------------------------------
def check_api_limit() -> int:
    """Check the API limit and log it"""
    compressions_this_month = tinify.compression_count
    # check if limit is reached
    if compressions_this_month and compressions_this_month >= getenv(
        "TINIFY_API_LIMIT", 500
    ):
        logging.critical(
            f"API limit reached: {compressions_this_month} compressions this month. "
            f"Try again next month ({get_days_until_next_month()} days remaining)!"
        )
        exit(
            f"API limit reached. Try again next month ({get_days_until_next_month()} days remaining)!"
        )

    return compressions_this_month


def get_days_until_next_month(
    from_date: datetime.date = datetime.date.today(),
) -> int:
    """Return the number of days until the next month

    :param datetime.date from_date: date to compare to next month, defaults to datetime.date.today()
    :return int: number of days until next month
    """
    next_month: datetime.date = datetime.date(
        from_date.year, from_date.month, 1
    ) + datetime.timedelta(days=31)
    diff = next_month - from_date
    return diff.days


# -- MAIN --------------------------------------------------------------------

# check API consumption
compressions_this_month = tinify.compression_count
logging.info(f"Compressions this month: {compressions_this_month}")
check_api_limit()

# compress all images
for image in input_folder.glob("**/*"):
    if image.suffix.lower() in images_extension:
        check_api_limit()
        logging.info(f"Compressing {image}")
        try:
            source = tinify.from_file(str(image.resolve()))
            resized = source.resize(
                method="scale",
                width=1000,
            )
            resized.to_file(str(output_folder / image.name))
        except tinify.AccountError as error:
            logging.critical(f"Account error: {error}")
            exit("Account error. Check your API key!")
        except tinify.ClientError as error:
            logging.error(f"Client error: {error}. Ignoring {image}.")
        except tinify.ServerError as error:
            logging.critical(f"Server error: {error}")
            exit("Server error. Check the log!")
        except tinify.ConnectionError as error:
            logging.critical(f"Connection error: {error}")
            exit("Connection error. Check the log!")
        except tinify.Error as error:
            logging.error(f"Error: {error}")
