#!python3

import os
import shutil
import platform
import argparse
import subprocess
import pathlib

requirements = ["build_pfs0", "build_romfs"]


def check_reqs() -> bool:
    system = platform.system()

    for req in requirements:
        if system in ["Linux", "Darwin"]:
            out = subprocess.run(
                ["whereis", req], stdout=subprocess.PIPE
            ).stdout.decode("utf-8")
            path = out.lstrip(f"{req}:").strip()
        elif system in ["Windows"]:
            out = subprocess.run(
                ["where.exe", req], stdout=subprocess.PIPE
            ).stdout.decode("utf-8")
            path = out.strip()

        path = pathlib.Path(path).absolute()

        if not path.exists():
            print(f"{req} ot found")
            return False
    return True


def get_objects(path: pathlib.Path):
    if not path.is_dir():
        raise ValueError("Path must be a directory")

    files = []
    for el_path in path.iterdir():
        if el_path.is_dir():
            files += get_objects(el_path)
            files.append(el_path)
        else:
            files.append(el_path)

    return files


def parse_manifest(file_path: pathlib.Path) -> dict:
    manifest = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            key, value = line.split('=', 1)
            manifest[key.lower().strip()] = value.lower().strip()
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input", type=str, default=".", help="Input directory"
    )
    parser.add_argument(
        "-o", "--output", type=str, default="./mod.msp", help="Output file"
    )
    parser.add_argument(
        "-m", "--manifest",
        type=str, default="./manifest", help="Manifest file"
    )
    args = parser.parse_args()

    input_path = pathlib.Path(args.input).absolute()
    output_path = pathlib.Path(args.output).absolute()
    manifest_path = pathlib.Path(args.manifest).absolute()

    assert manifest_path.exists(), f"{manifest_path} does not exists"
    assert input_path.exists(), f"{input_path} does not exists"
    assert input_path.is_dir(), "Input path must be directory"
    assert not output_path.exists(), f"{output_path} path already exists"

    temp_dir = output_path.parent.joinpath("tmp")
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    os.mkdir(temp_dir)

    # manifest = parse_manifest(manifest_path)
    shutil.copyfile(manifest_path, f"{temp_dir}/manifest")

    all_objects = get_objects(input_path)

    mod_files = []
    files_to_copy = ["romfs.bin", "exefs.nsp", "rtld", "main", "main.npdm", "compat0", "compat1", "compat2", "compat3",
                     "compat4",
                     "compat5", "compat6", "compat7", "compat8", "compat9", "subsdk0", "subsdk1", "subsdk2", "subsdk3",
                     "subsdk4", "subsdk5", "subsdk6", "subsdk7", "subsdk8", "subsdk9", "sdk", "config.ini", "icon.jpg"]
    for path in all_objects:
        name = path.name.lower()

        if path.is_dir() and name == "romfs":
            print("Found romfs dir. Building romfs.bin...")
            cmd = ["build_romfs", path, f"{temp_dir}/romfs.bin"]
            subprocess.run(cmd)

        if name in files_to_copy:
            print(f"Found {name}, copying...")
            shutil.copyfile(path, f"{temp_dir}/{name}")

        if name.endswith(".ips"):
            print(f"Found {name}, copying...")
            shutil.copyfile(path, f"{temp_dir}/{name}")

    print("Building pfs0...")
    cmd = ["build_pfs0", temp_dir, output_path]
    subprocess.run(cmd)

    shutil.rmtree(temp_dir)

    if not check_reqs():
        exit()
