import json
import os
import shutil
import socket
import subprocess

from jinja2 import Template

nginx_template = Template(open("nginx.conf", "r", encoding="utf-8").read())


def nginx_cleanup():
    directories = [
        "/etc/nginx/conf.d",
        "/etc/nginx/sites-enabled",
        "/etc/nginx/sites-available",
    ]

    for directory in directories:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                    print(f"Deleted {file_path}")
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    print(f"Deleted {file_path}")
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")


def nginx_render(name: str, port: int):
    """Render nginx configuration"""
    for path in [
        "/etc/nginx/conf.d",
        "/etc/nginx/sites-enabled",
        "/etc/nginx/sites-available",
    ]:
        os.makedirs(path, exist_ok=True)
        with open(f"{path}/{name}.conf", "w", encoding="utf-8") as f:
            f.write(nginx_template.render(name=name, port=port))

    subprocess.run(["nginx", "-s", "reload"])


def gen_port():
    """Generate a random port"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def aws_parse(items: list) -> dict:
    return {item["Name"]: item["Value"] for item in items}
