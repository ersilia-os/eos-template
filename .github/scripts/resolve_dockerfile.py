import sys
import os
import requests

from ersilia_pack.parsers import DockerfileInstallParser, YAMLInstallParser

REPO_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../.."))
PY_VERSION_MAP = {
    '3.8': 'py38', 
    '3.9': 'py39',
    '3.10': 'py310',
    '3.11': 'py311',
    '3.12': 'py312'
}
model_id = sys.argv[1]
def resolve_parser():
    if os.path.exists(os.path.abspath(os.path.join(REPO_PATH, "Dockerfile"))):
        return DockerfileInstallParser(file_dir=REPO_PATH)
    elif os.path.exists(os.path.join(REPO_PATH, "install.yml")):
        return YAMLInstallParser(file_dir=REPO_PATH)
    else:
        raise ValueError("No install file found")
    
def resolve_python_version(parser):
    return parser._get_python_version()

def read_dockerfile(parser):
    commands = parser._get_commands()
    has_conda = parser._has_conda(commands)
    if has_conda:
        file_url = "https://raw.githubusercontent.com/ersilia-os/ersilia/master/dockerfiles/dockerize-ersiliapack/model/Dockerfile.conda"
    else:
        file_url = "https://raw.githubusercontent.com/ersilia-os/ersilia/master/dockerfiles/dockerize-ersiliapack/model/Dockerfile.pip"
    response = requests.get(file_url)
    return response.text

def write_version_and_model_id(file_content, python_version):
    python_version = PY_VERSION_MAP[python_version]
    file_content = file_content.replace("eos_identifier", model_id)
    lines = file_content.split("\n")
    lines[0] = lines[0].replace("VERSION", python_version)
    with open(os.path.join(REPO_PATH, "../", "Dockerfile"), "w") as f:
        f.write("\n".join(lines))

if __name__ == "__main__":
    parser = resolve_parser()
    python_version = resolve_python_version(parser)
    dockerfile = read_dockerfile(parser)
    write_version_and_model_id(dockerfile, python_version)