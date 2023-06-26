#!env/bin/python3
import os
import subprocess
from pathlib import Path

import click

from .utils import gen_port, nginx_cleanup, nginx_render


@click.group()
def main():
    pass


@main.command()
def build():
    """Build all containers"""
    path = Path(__file__).parent/"containers"
    containers = os.listdir(path)
    for container in containers:
        subprocess.run(["docker", "build", "-t", container, f"{path}/{container}"])
    
@main.command()
def prune():
    nginx_cleanup()