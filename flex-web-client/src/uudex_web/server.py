from __future__ import annotations

import logging
from typing import List

import click

logging.basicConfig(level=logging.DEBUG)
# from dotenv import load_dotenv
#from fastapi import FastAPI
# import os
# import sys
from nicegui import ui

from uudex_web.pages import Pages, get_uudex_label
#from uudex_web.pages import Pages, show_global_header
from uudex_web.session import ClientApi, initialize

# from pathlib  import Path
# from dataclasses import dataclass
# from uudex_web import initialize_app
# from uudex_web.state import State
# import os




logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)
_log = logging.getLogger(__name__)

site_partitions = {
    'MITRE':  ["Ted@mitre", "Ted@pnnl", "Ted@oati"],
    'OATI': ["Shashank@oati", "Shashank@pnnl", "Shashank@mitre"],
    'PNNL': [
        "Jeff@pnnl",
        "Ted@pnnl",
        "Shashank@pnnl",
        "Jeff@oati",
        "Ted@mitre",
        "Shashank@mitre",
        "Jeff@oati",
        "Ted@oati",
        "Shashank@oati",
        "alice@PNNL",
        "bob@PNNL",
        "carol@PNNL",
        "subj_policy_demo@PNNL",
    ]
}

all_sites = [
            "Jeff@pnnl",
            "Ted@pnnl",
            "Shashank@pnnl",
            "Jeff@oati",
            "Ted@mitre",
            "Shashank@mitre",
            "Jeff@oati",
            "Ted@oati",
            "Shashank@oati",
            "alice@PNNL",
            "bob@PNNL",
            "carol@PNNL",
            "subj_policy_demo@PNNL",
        ]

# @click.command()
# @click.argument("site")
# def run_server(site: str):
#     if site not in all_sites:
#         raise ValueError(f"Site {site} is unavailable.")

#     api = ClientApi(all_sites=all_sites)
#     initialize(api)

#     Pages.HOME()
#     ui.run(show=True, port=8080, uvicorn_logging_level=logging.DEBUG)


# certs_dir = os.environ.get("CLIENT_CERTS")

# if not certs_dir:
#     raise ValueError("Invalid CLIENT_CERTS environmental variable specified")

# certs_path = Path(certs_dir)

# if not certs_path.is_dir():
#     raise ValueError(f"CLIENT_CERTS directory doesn't exist {certs_dir}")

# state = State(certs_path)

# ui.select([x.name for x in state.get_client_certs()],
#           label="Client Certificate",
#           on_change=lambda value: state.set_client_cert(value))
# ui.label("Woot There it is!")

# ui.run(port=6000)

if __name__ in {"__main__", "__mp_main__"}:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("site", type=str,
                        help="The local site to be used during this session.")

    opts = parser.parse_args()



    if opts.site not in (site_partitions.keys()):
        raise ValueError(f"Site {opts.site} not available.")

    from pathlib import Path
    print(f"The path is: {Path('.').absolute()}")

    api = ClientApi(site_users=site_partitions[opts.site])
    api.local_site = opts.site
    initialize(client=api)

    Pages.HOME.title = get_uudex_label(opts.site)
    Pages.HOME()
    reload_dirs = str(Path(".").absolute() / "src/uudex_web")
    ui.run(show=False, port=8080, uvicorn_logging_level=logging.DEBUG, uvicorn_reload_dirs=reload_dirs)
    #run_server()
