#! python3 # noqa: E265

"""
    WSGI script to allow launch isso through Apache mod_wsgi.
"""

import site  # noqa: E402

site.addsitedir("./.venv")


from pathlib import Path  # noqa: E402

from isso import config, make_app  # noqa: E402

# globals
isso_conf_file = Path(__file__).parent / "isso-prod.cfg"

application = make_app(
    config.load(
        default=config.default_file(),
        user=str(isso_conf_file.resolve())
        # default=os.path.join(dist.location, dist.project_name, "defaults.ini"),
        # user=str(isso_conf_file.resolve()),
    ),
    multiprocessing=True,
    threading=True,
)
