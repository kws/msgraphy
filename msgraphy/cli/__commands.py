import logging

import click
import click_log
from rich import print_json, print
from rich.table import Table

from .__settings import app_settings
from .. import GraphApi
from ..auth.graph_auth import BasicAuth
from ..client.graph_client import RequestsGraphClient
from ..data.sharepoint import SiteResource

logger = logging.getLogger(__name__)
click_log.basic_config(logger)


@click.group()
@click.option("--client_id", help="Client ID", type=str)
@click.option("--client_secret", help="Client Secret", type=str)
@click.option("--authority", help="Authority/Tenant Id", type=str)
@click_log.simple_verbosity_option(logger)
@click.pass_context
def msgraphy(ctx, client_id, client_secret, authority):
    settings = app_settings()

    if client_id:
        settings.client_id = client_id
    if client_secret:
        settings.client_secret = client_secret
    if authority:
        settings.authority = authority

    if not settings.client_id:
        settings.client_id = click.prompt('Please enter the graph application client_id', type=str)

    if not settings.authority:
        settings.authority = click.prompt('Please enter the authority URL or tenant_id', type=str)

    ctx.ensure_object(dict)
    ctx.obj['settings'] = settings


def __get_api(ctx, scopes):
    settings = ctx.obj['settings']
    auth = BasicAuth(settings, scopes=scopes)
    client = RequestsGraphClient(auth)
    return GraphApi(client)


@msgraphy.command()
@click.pass_context
def me(ctx):
    api = __get_api(ctx, ["User.Read"])
    response = api.client.make_request("/me")
    print_json(response.text)


@msgraphy.group()
def sites():
    pass


@sites.command(name="search")
@click.argument("name")
@click.option("--table", help="Display as table", is_flag=True)
@click.pass_context
def sites_search(ctx, name, table):
    api = __get_api(ctx, ["Sites.Read.All"])
    response = api.sharepoint.list_sites(name)

    if table:
        table = Table()
        table.add_column("Name")
        table.add_column("Display Name")
        table.add_column("Description")

        for site in response.value:
            table.add_row(
                site.name,
                site.display_name,
                site.description,
            )

        print(table)
    else:
        print_json(response.text)


@sites.command(name="drives")
@click.argument("name")
@click.option("--table", help="Display as table", is_flag=True)
@click.pass_context
def sites_drives(ctx, name, table):
    api = __get_api(ctx, ["Sites.Read.All"])
    response = api.sharepoint.list_drives(SiteResource(name=name))

    if table:
        table = Table()
        table.add_column("ID")
        table.add_column("Name")
        table.add_column("Created")
        table.add_column("Last Modified")

        for site in response.value:
            table.add_row(
                site.id,
                site.name,
                f"{site.created_date_time}",
                f"{site.last_modified_date_time}",
            )

        print(table)
    else:
        print_json(response.text)
