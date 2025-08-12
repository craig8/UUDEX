#!/usr/bin/env python3
"""
UUDEX Standalone CLI - Command Line Interface for UUDEX API

A colorful and feature-rich standalone CLI for interacting with the UUDEX API.
Supports certificate-based authentication, table output, and various API operations.
"""

import asyncio
import os
import sys
from pathlib import Path
from typing import List, Dict, Optional, Any
import json
import click
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.text import Text
from rich.syntax import Syntax
from rich.tree import Tree
from rich.columns import Columns
from rich.markdown import Markdown
from rich import print as rprint
from rich.live import Live

# Add current directory to path for local imports
sys.path.insert(0, str(Path(__file__).parent))

from cert_manager import CertificateManager
from config import Config

# Add parent directory to path for uudex_api_client
sys.path.insert(0, str(Path(__file__).parent.parent))
from uudex_api_client import Client

# Initialize rich console
console = Console()

# Global configuration
config = Config()


class UUDEXCLIError(Exception):
    """Custom exception for UUDEX CLI errors"""
    pass


class UUDEXClient:
    """Wrapper class for UUDEX API client with enhanced CLI functionality"""

    def __init__(self, entity_name: Optional[str] = None):
        self.entity_name = entity_name
        self.client = None
        self.cert_manager = CertificateManager(config.CERTS_DIR)
        self.config = config

    def initialize(self):
        """Initialize the client with certificate authentication"""
        if not self.entity_name:
            self._select_entity()

        if self.entity_name:
            self.client = self.cert_manager.build_client(
                self.entity_name, self.config.get_api_base_url())
        else:
            raise UUDEXCLIError("No entity selected or available")

    def _select_entity(self):
        """Interactively select an entity from available certificates"""
        self.cert_manager.load_entities_from_certs()

        if not self.cert_manager.available_entities:
            raise UUDEXCLIError("No entities found in certificate directory")

        # Display available entities
        table = Table(title="Available Entities")
        table.add_column("Index", style="cyan")
        table.add_column("Entity Name", style="green")
        table.add_column("Status", style="yellow")

        for i, entity in enumerate(self.cert_manager.available_entities):
            # Test authentication status
            status = "✓ Valid" if self.cert_manager.test_client_authentication(
                entity) else "✗ Invalid"
            table.add_row(str(i + 1), entity, status)

        console.print(table)

        while True:
            try:
                choice = Prompt.ask(
                    "Select an entity",
                    choices=[
                        str(i + 1) for i in range(
                            len(self.cert_manager.available_entities))
                    ],
                    default="1")
                self.entity_name = self.cert_manager.available_entities[
                    int(choice) - 1]
                break
            except (ValueError, IndexError):
                console.print("[red]Invalid choice. Please try again.[/red]")


def create_table(title: str,
                 data: List[Dict],
                 columns: Optional[List[str]] = None) -> Table:
    """Create a rich table from data"""
    table = Table(title=title, show_header=True, header_style="bold magenta")

    if not data:
        table.add_column("Message", style="yellow")
        table.add_row("No data available")
        return table

    # Auto-detect columns if not provided
    if not columns:
        columns = list(data[0].keys()) if data else []

    # Add columns with alternating colors
    colors = ["cyan", "green", "yellow", "blue", "red", "magenta"]
    for i, col in enumerate(columns):
        table.add_column(col.replace('_', ' ').title(),
                         style=colors[i % len(colors)])

    # Add rows
    for row in data:
        table.add_row(*[str(row.get(col, '')) for col in columns])

    return table


def format_json_output(data: Any, title: str = "JSON Output") -> None:
    """Format and display JSON data with syntax highlighting"""
    if isinstance(data, (dict, list)):
        json_str = json.dumps(data, indent=2, default=str)
        syntax = Syntax(json_str, "json", theme="monokai", line_numbers=True)
        console.print(Panel(syntax, title=title, border_style="blue"))
    else:
        console.print(Panel(str(data), title=title, border_style="blue"))


@click.group(invoke_without_command=True)
@click.option('--entity', '-e', help='Entity name to use for authentication')
@click.option('--output',
              '-o',
              type=click.Choice(['table', 'json', 'tree']),
              default='table',
              help='Output format')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.pass_context
def cli(ctx, entity, output, verbose):
    """UUDEX Standalone CLI - A colorful command-line interface for the UUDEX API"""
    ctx.ensure_object(dict)
    ctx.obj['entity'] = entity
    ctx.obj['output'] = output
    ctx.obj['verbose'] = verbose

    # Print welcome banner if no subcommand is provided
    if ctx.invoked_subcommand is None:
        banner = """
[bold cyan]╔══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗[/bold cyan]
[bold cyan]║[/bold cyan]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]                                                                    [bold green]██╗   ██╗██╗   ██╗██████╗ ███████╗██╗  ██╗     ██████╗██╗     ██╗[/bold green]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]                                                                    [bold green]██║   ██║██║   ██║██╔══██╗██╔════╝╚██╗██╔╝    ██╔════╝██║     ██║[/bold green]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]                                                                    [bold green]██║   ██║██║   ██║██║  ██║█████╗   ╚███╔╝     ██║     ██║     ██║[/bold green]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]                                                                    [bold green]██║   ██║██║   ██║██║  ██║██╔══╝   ██╔██╗     ██║     ██║     ██║[/bold green]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]                                                                    [bold green]╚██████╔╝╚██████╔╝██████╔╝███████╗██╔╝ ██╗    ╚██████╗███████╗██║[/bold green]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]                                                                     [bold green]╚═════╝  ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝     ╚═════╝╚══════╝╚═╝[/bold green]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]                                                                           [bold yellow]A colorful standalone command-line interface for the UUDEX API[/bold yellow]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      [bold cyan]║[/bold cyan]
[bold cyan]╚══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝[/bold cyan]
        """
        console.print(banner)
        console.print("[bold]Use --help to see available commands[/bold]")
        console.print()

        # Show quick start info
        console.print("[bold cyan]Quick Start:[/bold cyan]")
        console.print(
            "  [green]./uudex entities[/green]     - List available certificate entities"
        )
        console.print(
            "  [green]./uudex status[/green]       - Check API status and authentication"
        )
        console.print(
            "  [green]./uudex config-info[/green]  - Display configuration information"
        )
        console.print(
            "  [green]./uudex --help[/green]       - Show all available commands"
        )
        console.print()

        # Show certificate setup info if no certs found
        from cert_manager import CertificateManager
        cert_manager = CertificateManager(config.CERTS_DIR)
        cert_manager.load_entities_from_certs()
        if not cert_manager.available_entities:
            console.print(
                "[bold yellow]💡 Tip:[/bold yellow] Place your X.509 certificates in the 'certs' directory to get started"
            )
            console.print(
                f"[dim]Certificate directory: {config.CERTS_DIR}[/dim]")


def get_client(ctx) -> UUDEXClient:
    """Get authenticated UUDEX client"""
    client = UUDEXClient(ctx.obj['entity'])

    with console.status("[bold green]Initializing authentication..."):
        client.initialize()

    return client


# Endpoint commands
@cli.group()
@click.pass_context
def endpoints(ctx):
    """Manage endpoints"""
    pass


@endpoints.command(name="list")
@click.pass_context
def list_endpoints(ctx):
    """List all endpoints"""
    try:
        client = get_client(ctx)

        with console.status("[bold green]Fetching endpoints..."):
            httpx_client = client.client.get_httpx_client()
            response = httpx_client.get("/auth/endpoints")

            if response.status_code == 200:
                endpoints_data = response.json()

                if ctx.obj['output'] == 'json':
                    format_json_output(endpoints_data, "Endpoints")
                else:
                    # Convert to table format
                    table_data = []
                    for endpoint in endpoints_data:
                        table_data.append({
                            'UUID':
                            endpoint.get('uuid', ''),
                            'Name':
                            endpoint.get('name', ''),
                            'Status':
                            endpoint.get('status', ''),
                            'Created':
                            endpoint.get('created_at', ''),
                            'Updated':
                            endpoint.get('updated_at', '')
                        })

                    table = create_table("Endpoints", table_data)
                    console.print(table)
            else:
                console.print(
                    f"[red]Error: {response.status_code} - {response.text}[/red]"
                )

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")


@endpoints.command(name="get")
@click.argument('endpoint_uuid')
@click.pass_context
def get_endpoint(ctx, endpoint_uuid):
    """Get details of a specific endpoint"""
    try:
        client = get_client(ctx)

        with console.status(
                f"[bold green]Fetching endpoint {endpoint_uuid}..."):
            httpx_client = client.client.get_httpx_client()
            response = httpx_client.get(f"/auth/endpoints/{endpoint_uuid}")

            if response.status_code == 200:
                endpoint_data = response.json()

                if ctx.obj['output'] == 'json':
                    format_json_output(endpoint_data,
                                       f"Endpoint {endpoint_uuid}")
                else:
                    # Display as key-value pairs
                    table = Table(title=f"Endpoint Details: {endpoint_uuid}")
                    table.add_column("Property", style="cyan")
                    table.add_column("Value", style="green")

                    for key, value in endpoint_data.items():
                        table.add_row(
                            key.replace('_', ' ').title(), str(value))

                    console.print(table)
            else:
                console.print(
                    f"[red]Error: {response.status_code} - {response.text}[/red]"
                )

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")


@endpoints.command()
@click.pass_context
def peers(ctx):
    """List peer endpoints"""
    try:
        client = get_client(ctx)

        with console.status("[bold green]Fetching peer endpoints..."):
            httpx_client = client.client.get_httpx_client()
            response = httpx_client.get("/auth/endpoints/peers")

            if response.status_code == 200:
                peers_data = response.json()

                if ctx.obj['output'] == 'json':
                    format_json_output(peers_data, "Peer Endpoints")
                else:
                    table_data = []
                    for peer in peers_data:
                        table_data.append({
                            'UUID':
                            peer.get('uuid', ''),
                            'Name':
                            peer.get('name', ''),
                            'Organization':
                            peer.get('organization', ''),
                            'Status':
                            peer.get('status', ''),
                            'Last Seen':
                            peer.get('last_seen', '')
                        })

                    table = create_table("Peer Endpoints", table_data)
                    console.print(table)
            else:
                console.print(
                    f"[red]Error: {response.status_code} - {response.text}[/red]"
                )

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")


@endpoints.command()
@click.pass_context
def me(ctx):
    """Get information about the current endpoint"""
    try:
        client = get_client(ctx)

        with console.status("[bold green]Fetching current endpoint info..."):
            httpx_client = client.client.get_httpx_client()
            response = httpx_client.get("/endpoint/me")

            if response.status_code == 200:
                me_data = response.json()

                if ctx.obj['output'] == 'json':
                    format_json_output(me_data, "Current Endpoint")
                else:
                    # Create an info panel
                    info_text = f"""
[bold green]Name:[/bold green] {me_data.get('name', 'N/A')}
[bold blue]UUID:[/bold blue] {me_data.get('uuid', 'N/A')}
[bold yellow]Organization:[/bold yellow] {me_data.get('organization', 'N/A')}
[bold cyan]Status:[/bold cyan] {me_data.get('status', 'N/A')}
[bold magenta]Created:[/bold magenta] {me_data.get('created_at', 'N/A')}
[bold red]Updated:[/bold red] {me_data.get('updated_at', 'N/A')}
                    """
                    console.print(
                        Panel(info_text,
                              title="Current Endpoint Information",
                              border_style="green"))
            else:
                console.print(
                    f"[red]Error: {response.status_code} - {response.text}[/red]"
                )

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")


# Dataset commands
@cli.group()
@click.pass_context
def datasets(ctx):
    """Manage datasets"""
    pass


@datasets.command(name="list")
@click.argument('subject_uuid')
@click.option('--search', '-s', help='Search expression to filter datasets')
@click.option('--participant',
              '-p',
              help='Limit search to datasets owned by this participant')
@click.pass_context
def list_datasets(ctx, subject_uuid, search, participant):
    """List datasets for a subject"""
    try:
        client = get_client(ctx)

        params = {'subject_uuid': subject_uuid}
        if search:
            params['search_expression'] = search
        if participant:
            params['participant_uuid'] = participant

        with console.status("[bold green]Fetching datasets..."):
            httpx_client = client.client.get_httpx_client()
            response = httpx_client.get("/datasets", params=params)

            if response.status_code == 200:
                datasets_data = response.json()

                if ctx.obj['output'] == 'json':
                    format_json_output(datasets_data, "Datasets")
                else:
                    table_data = []
                    for dataset in datasets_data:
                        table_data.append({
                            'UUID':
                            dataset.get('uuid', ''),
                            'Name':
                            dataset.get('name', ''),
                            'Subject':
                            dataset.get('subject_name', ''),
                            'Owner':
                            dataset.get('owner_name', ''),
                            'Size':
                            dataset.get('size', ''),
                            'Created':
                            dataset.get('created_at', '')
                        })

                    table = create_table(f"Datasets (Subject: {subject_uuid})",
                                         table_data)
                    console.print(table)
            else:
                console.print(
                    f"[red]Error: {response.status_code} - {response.text}[/red]"
                )

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")


@datasets.command(name="get")
@click.argument('dataset_uuid')
@click.pass_context
def get_dataset(ctx, dataset_uuid):
    """Get details of a specific dataset"""
    try:
        client = get_client(ctx)

        with console.status(f"[bold green]Fetching dataset {dataset_uuid}..."):
            httpx_client = client.client.get_httpx_client()
            response = httpx_client.get(f"/datasets/{dataset_uuid}")

            if response.status_code == 200:
                dataset_data = response.json()

                if ctx.obj['output'] == 'json':
                    format_json_output(dataset_data, f"Dataset {dataset_uuid}")
                else:
                    # Create dataset info panel
                    info_text = f"""
[bold green]Name:[/bold green] {dataset_data.get('name', 'N/A')}
[bold blue]UUID:[/bold blue] {dataset_data.get('uuid', 'N/A')}
[bold yellow]Subject:[/bold yellow] {dataset_data.get('subject_name', 'N/A')}
[bold cyan]Owner:[/bold cyan] {dataset_data.get('owner_name', 'N/A')}
[bold magenta]Size:[/bold magenta] {dataset_data.get('size', 'N/A')}
[bold red]Created:[/bold red] {dataset_data.get('created_at', 'N/A')}
[bold white]Description:[/bold white] {dataset_data.get('description', 'N/A')}
                    """
                    console.print(
                        Panel(
                            info_text,
                            title=
                            f"Dataset: {dataset_data.get('name', 'Unknown')}",
                            border_style="blue"))

                    # Show metadata if available
                    if 'metadata' in dataset_data and dataset_data['metadata']:
                        metadata_table = Table(title="Metadata")
                        metadata_table.add_column("Key", style="cyan")
                        metadata_table.add_column("Value", style="green")

                        for key, value in dataset_data['metadata'].items():
                            metadata_table.add_row(key, str(value))

                        console.print(metadata_table)
            else:
                console.print(
                    f"[red]Error: {response.status_code} - {response.text}[/red]"
                )

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")


# Subject commands
@cli.group()
@click.pass_context
def subjects(ctx):
    """Manage subjects"""
    pass


@subjects.command()
@click.option('--name', '-n', help='Filter by subject name')
@click.pass_context
def discover(ctx, name):
    """Discover available subjects"""
    try:
        client = get_client(ctx)

        params = {}
        if name:
            params['name'] = name

        with console.status("[bold green]Discovering subjects..."):
            httpx_client = client.client.get_httpx_client()
            response = httpx_client.get("/subjects/discover", params=params)

            if response.status_code == 200:
                subjects_data = response.json()

                if ctx.obj['output'] == 'json':
                    format_json_output(subjects_data, "Subjects")
                else:
                    table_data = []
                    for subject in subjects_data:
                        table_data.append({
                            'UUID':
                            subject.get('uuid', ''),
                            'Name':
                            subject.get('name', ''),
                            'Type':
                            subject.get('type', ''),
                            'Access':
                            subject.get('access_level', ''),
                            'Created':
                            subject.get('created_at', '')
                        })

                    table = create_table("Available Subjects", table_data)
                    console.print(table)
            else:
                console.print(
                    f"[red]Error: {response.status_code} - {response.text}[/red]"
                )

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")


@subjects.command(name="get")
@click.argument('subject_uuid')
@click.pass_context
def get_subject(ctx, subject_uuid):
    """Get details of a specific subject"""
    try:
        client = get_client(ctx)

        with console.status(f"[bold green]Fetching subject {subject_uuid}..."):
            httpx_client = client.client.get_httpx_client()
            response = httpx_client.get(f"/subjects/{subject_uuid}")

            if response.status_code == 200:
                subject_data = response.json()

                if ctx.obj['output'] == 'json':
                    format_json_output(subject_data, f"Subject {subject_uuid}")
                else:
                    # Create subject info panel
                    info_text = f"""
[bold green]Name:[/bold green] {subject_data.get('name', 'N/A')}
[bold blue]UUID:[/bold blue] {subject_data.get('uuid', 'N/A')}
[bold yellow]Type:[/bold yellow] {subject_data.get('type', 'N/A')}
[bold cyan]Access Level:[/bold cyan] {subject_data.get('access_level', 'N/A')}
[bold magenta]Owner:[/bold magenta] {subject_data.get('owner_name', 'N/A')}
[bold red]Created:[/bold red] {subject_data.get('created_at', 'N/A')}
[bold white]Description:[/bold white] {subject_data.get('description', 'N/A')}
                    """
                    console.print(
                        Panel(
                            info_text,
                            title=
                            f"Subject: {subject_data.get('name', 'Unknown')}",
                            border_style="yellow"))
            else:
                console.print(
                    f"[red]Error: {response.status_code} - {response.text}[/red]"
                )

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")


# Subscription commands
@cli.group()
@click.pass_context
def subscriptions(ctx):
    """Manage subscriptions"""
    pass


@subscriptions.command(name="list")
@click.pass_context
def list_subscriptions(ctx):
    """List all subscriptions"""
    try:
        client = get_client(ctx)

        with console.status("[bold green]Fetching subscriptions..."):
            httpx_client = client.client.get_httpx_client()
            response = httpx_client.get("/subscriptions")

            if response.status_code == 200:
                subscriptions_data = response.json()

                if ctx.obj['output'] == 'json':
                    format_json_output(subscriptions_data, "Subscriptions")
                else:
                    table_data = []
                    for subscription in subscriptions_data:
                        table_data.append({
                            'UUID':
                            subscription.get('uuid', ''),
                            'Name':
                            subscription.get('name', ''),
                            'Status':
                            subscription.get('status', ''),
                            'Subject Count':
                            subscription.get('subject_count', 0),
                            'Created':
                            subscription.get('created_at', '')
                        })

                    table = create_table("Subscriptions", table_data)
                    console.print(table)
            else:
                console.print(
                    f"[red]Error: {response.status_code} - {response.text}[/red]"
                )

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")


@subscriptions.command()
@click.argument('subscription_uuid')
@click.option('--max-messages',
              '-m',
              type=int,
              default=10,
              help='Maximum number of messages to consume')
@click.pass_context
def consume(ctx, subscription_uuid, max_messages):
    """Consume messages from a subscription"""
    try:
        client = get_client(ctx)

        with console.status(
                f"[bold green]Consuming messages from subscription {subscription_uuid}..."
        ):
            httpx_client = client.client.get_httpx_client()
            params = {'max_messages': max_messages}
            response = httpx_client.get(
                f"/subscriptions/{subscription_uuid}/consume", params=params)

            if response.status_code == 200:
                messages_data = response.json()

                if ctx.obj['output'] == 'json':
                    format_json_output(messages_data,
                                       f"Messages from {subscription_uuid}")
                else:
                    if 'messages' in messages_data and messages_data[
                            'messages']:
                        table_data = []
                        for msg in messages_data['messages']:
                            table_data.append({
                                'ID':
                                msg.get('id', ''),
                                'Subject':
                                msg.get('subject', ''),
                                'Timestamp':
                                msg.get('timestamp', ''),
                                'Size':
                                msg.get('size', ''),
                                'Type':
                                msg.get('type', '')
                            })

                        table = create_table(
                            f"Messages from Subscription {subscription_uuid}",
                            table_data)
                        console.print(table)
                    else:
                        console.print("[yellow]No messages available[/yellow]")
            else:
                console.print(
                    f"[red]Error: {response.status_code} - {response.text}[/red]"
                )

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")


# Utility commands
@cli.command()
@click.pass_context
def status(ctx):
    """Check API status and authentication"""
    try:
        client = get_client(ctx)

        with console.status("[bold green]Checking API status..."):
            httpx_client = client.client.get_httpx_client()

            # Check /endpoint/me endpoint
            response = httpx_client.get("/endpoint/me")

            if response.status_code == 200:
                me_data = response.json()

                # Create status panel
                status_text = f"""
[bold green]✓ API Connection:[/bold green] Successful
[bold green]✓ Authentication:[/bold green] Valid
[bold blue]Entity:[/bold blue] {client.entity_name}
[bold yellow]Endpoint Name:[/bold yellow] {me_data.get('name', 'Unknown')}
[bold cyan]Organization:[/bold cyan] {me_data.get('organization', 'Unknown')}
[bold magenta]Status:[/bold magenta] {me_data.get('status', 'Unknown')}
                """
                console.print(
                    Panel(status_text,
                          title="UUDEX API Status",
                          border_style="green"))
            else:
                console.print(
                    f"[red]✗ API Error: {response.status_code} - {response.text}[/red]"
                )

    except Exception as e:
        console.print(f"[red]✗ Connection Error: {str(e)}[/red]")


@cli.command()
@click.pass_context
def entities(ctx):
    """List available certificate entities"""
    try:
        cert_manager = CertificateManager(config.CERTS_DIR)

        with console.status("[bold green]Loading certificate entities..."):
            cert_manager.load_entities_from_certs()

        if cert_manager.available_entities:
            table = Table(title="Available Certificate Entities")
            table.add_column("Entity Name", style="green")
            table.add_column("Certificate Path", style="cyan")
            table.add_column("Auth Status", style="yellow")

            for entity in cert_manager.available_entities:
                cert_path = cert_manager.entity_cert_mapping.get(
                    entity, "Unknown")
                auth_status = "✓ Valid" if cert_manager.test_client_authentication(
                    entity) else "✗ Invalid"
                table.add_row(entity, cert_path, auth_status)

            console.print(table)
        else:
            console.print("[yellow]No certificate entities found[/yellow]")

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")


@cli.command()
@click.pass_context
def config_info(ctx):
    """Display configuration information"""
    config_text = f"""
[bold green]Certificate Directory:[/bold green] {config.CERTS_DIR}
[bold blue]Base URL:[/bold blue] {config.get_uudex_url()}
[bold yellow]API Base URL:[/bold yellow] {config.get_api_base_url()}
[bold cyan]Backend Port:[/bold cyan] {config.BACKEND_PORT}
[bold magenta]UUDEX Port:[/bold magenta] {config.UUDEX_PORT}
[bold red]Debug Mode:[/bold red] {config.DEBUG_MODE}
[bold white]Server Mode:[/bold white] {config.SERVER_MODE}
[bold green]Available Certificates:[/bold green] {', '.join(config.get_available_certs())}
    """
    console.print(
        Panel(config_text, title="Configuration", border_style="blue"))


if __name__ == '__main__':
    cli()
