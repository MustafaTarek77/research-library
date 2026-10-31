#!/usr/bin/env python3
"""Follow readable application messages from Airflow's JSON task logs."""

import argparse
import json
from pathlib import Path
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--once", action="store_true", help="Print existing progress and exit")
    args = parser.parse_args()
    offsets = {}
    print("Watching application events in .airflow/logs (Ctrl+C to stop)", flush=True)
    try:
        while True:
            events = []
            for path in Path(".airflow/logs/dag_id=paper_pipeline").glob("**/*.log"):
                with path.open() as stream:
                    stream.seek(offsets.get(path, 0))
                    while True:
                        start = stream.tell()
                        line = stream.readline()
                        if not line:
                            break
                        if not line.endswith("\n"):
                            stream.seek(start)
                            break
                        try:
                            event = json.loads(line)
                        except ValueError:
                            continue
                        if str(event.get("logger", "")).startswith("research_library"):
                            events.append((event.get("timestamp", ""), path, event))
                    offsets[path] = stream.tell()
            for timestamp, path, event in sorted(events, key=lambda item: (item[0], str(item[1]))):
                print(f"{timestamp} {event.get('level', 'info').upper():7} {event.get('event', '')}", flush=True)
            if args.once:
                return
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopped watching. Airflow continues running.")


if __name__ == "__main__":
    main()
