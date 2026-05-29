#!/usr/bin/env python3
"""Adapter for running SID-SLAM on one TUM RGB-D dataset."""

from __future__ import annotations

import argparse
import os
import signal
import subprocess
import sys
from pathlib import Path
import shutil


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--algorithm-dir", type=Path, required=True)
    parser.add_argument("--algorithm-name", default="SID-SLAM")
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def count_files(path: Path) -> int:
    return sum(1 for item in path.iterdir() if item.is_file())


def camera_yaml(algorithm_dir: Path, dataset_name: str) -> Path:
    cameras_dir = algorithm_dir / "Examples" / "RGB-D" / "TUM" / "camerasTUM"
    lowered = dataset_name.lower()
    if "freiburg2" in lowered or "fr2" in lowered:
        return cameras_dir / "freiburg2.yaml"
    if "freiburg3" in lowered or "fr3" in lowered:
        return cameras_dir / "freiburg3.yaml"
    return cameras_dir / "freiburg1.yaml"


def write_system_settings(source: Path, destination: Path) -> None:
    text = source.read_text(encoding="utf-8")
    text = text.replace("visualization: 1", "visualization: 0")
    destination.write_text(text, encoding="utf-8")


def prepare_sequence(args: argparse.Namespace) -> Path:
    dataset = args.dataset.resolve()
    output = args.output.resolve()
    sequence_dir = output / "sequence_config"
    sequence_dir.mkdir(parents=True, exist_ok=True)

    required = ["rgb", "depth", "rgb.txt", "depth.txt", "associations.txt", "groundtruth.txt"]
    missing = [name for name in required if not (dataset / name).exists()]
    if missing:
        raise SystemExit(f"Dataset is missing SID-SLAM TUM inputs: {', '.join(missing)}")

    camera = camera_yaml(args.algorithm_dir.resolve(), dataset.name).resolve()
    if not camera.is_file():
        raise SystemExit(f"Camera YAML not found: {camera}")

    sequence_settings = f"""%YAML:1.0

sequenceSettings:
   sequenceName: {dataset.name}
   cameraYAML: {camera}

RGBD_TUM_dataset:
   numRGB: {count_files(dataset / "rgb")}
   numDepth: {count_files(dataset / "depth")}
   associationsTxt: associations.txt
   groundtruthTxt: groundtruth.txt
"""
    (sequence_dir / "sequenceSettings.yaml").write_text(sequence_settings, encoding="utf-8")

    write_system_settings(
        args.algorithm_dir.resolve() / "systemSettings.yaml",
        output / "systemSettings.headless.yaml",
    )
    return sequence_dir


def main() -> int:
    args = parse_args()
    algorithm_dir = args.algorithm_dir.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)

    executable = algorithm_dir / "Examples" / "RGB-D" / "TUM" / "rgbdTUM"
    if not executable.is_file() or not os.access(executable, os.X_OK):
        raise SystemExit(f"SID-SLAM executable not found or not executable: {executable}")

    sequence_dir = prepare_sequence(args)
    system_settings = output / "systemSettings.headless.yaml"
    dataset_root = args.dataset.resolve().parent
    command = [
        str(executable),
        str(sequence_dir),
        str(system_settings),
        "0",
        str(output),
        str(dataset_root),
    ]
    (output / "command.txt").write_text(" ".join(command) + "\n", encoding="utf-8")

    if args.dry_run:
        print(" ".join(command))
        return 0

    with (output / "run.log").open("w", encoding="utf-8") as log:
        env = os.environ.copy()
        env["SID_SLAM_SKIP_WAITS"] = "1"
        proc = subprocess.Popen(
            command,
            cwd=algorithm_dir,
            env=env,
            stdout=log,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
        try:
            return_code = proc.wait()
        except KeyboardInterrupt:
            os.killpg(proc.pid, signal.SIGTERM)
            try:
                return_code = proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(proc.pid, signal.SIGKILL)
                return_code = proc.wait()
            raise

    produced = output / "00000_CameraTrajectory.txt"
    canonical = output / "CameraTrajectory.txt"
    if produced.is_file() and produced.stat().st_size > 0:
        shutil.copy2(produced, canonical)

    return return_code


if __name__ == "__main__":
    raise SystemExit(main())
