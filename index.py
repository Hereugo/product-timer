from datetime import datetime
from itertools import chain
from logging.handlers import RotatingFileHandler
import logging
import argparse
import typing
import csv
import os
import sys


class Timer(typing.TypedDict):
    id: int
    label: str
    created_at: datetime
    start: typing.Optional[datetime]
    end: typing.Optional[datetime]

    @staticmethod  # type: ignore
    def keys() -> typing.List[str]:
        return Timer.__dict__["__annotations__"].keys()


Timers = dict[str, typing.List[Timer]]


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = RotatingFileHandler("logs.log", maxBytes=5000000, backupCount=5)
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
handler = logging.StreamHandler(sys.stdout)
file_handler.setFormatter(formatter)
handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(handler)


def read_timers(reader: csv.DictReader) -> Timers:
    timers: Timers = {}

    _headers = next(reader)
    for row in reader:
        data: Timer = {
            "id": int(row["id"]),
            "label": row["label"],
            "start": (datetime.fromisoformat(row["start"]) if row["start"] else None),
            "end": datetime.fromisoformat(row["end"]) if row["end"] else None,
            "created_at": datetime.fromisoformat(row["created_at"]),
        }
        if not row["label"] in timers:
            timers[row["label"]] = []

        timers[row["label"]].append(data)
    return timers


def get_timer(timers: Timers, label: str) -> typing.Optional[Timer]:
    filtered_timers = timers.get(label, [])
    if len(filtered_timers) == 0:
        return None
    return filtered_timers[-1]


def display_timers(timers: typing.List[Timer], label: str):
    # TODO: better display
    if len(timers) == 0:
        print(f"No timers for label {label}")
        return

    print(label)
    for i, timer in enumerate(timers, 1):
        start = timer["start"].strftime("%H:%M:%S") if timer["start"] else "not started"
        end = (
            timer["end"].strftime("%H:%M:%S")
            if timer["end"]
            else "ongoing" if start != "not started" else "not started"
        )
        print(f"{i}. {start} - {end}")


if __name__ == "__main__":
    if not os.path.isfile("./timers.csv"):
        with open("./timers.csv", "w") as file:
            pass
    csvfile = open("./timers.csv", "r+")

    parser = argparse.ArgumentParser(description="start/finish timers")
    group_crud = parser.add_mutually_exclusive_group()

    group_crud.add_argument("-c", "--create", help="creates new timer of given label")
    group_crud.add_argument("-d", "--delete", help="delete timer of given label")
    group_crud.add_argument("-s", "--start", help="start timer of given label")
    group_crud.add_argument("-f", "--finish", help="stops timer of given label")
    group_crud.add_argument("-r", "--resume", help="resumes timer of given label")
    parser.add_argument(
        "--log",
        default=csvfile,
        type=argparse.FileType("r+"),
        help="the file where the timers should be appended to",
    )
    parser.add_argument("-v", "--view", help="view timers of given label")

    args = parser.parse_args()

    writer = csv.DictWriter(args.log, Timer.keys())
    if not os.path.isfile(args.log.name):
        with open(args.log.name, "w") as file:
            pass
    if os.path.getsize(args.log.name) == 0:
        writer.writeheader()

    args.log.seek(0)
    reader = csv.DictReader(args.log, Timer.keys())

    timers = read_timers(reader)

    if args.create:
        new_timer: Timer = {
            "id": len(timers.get(args.create, [])) + 1,
            "label": args.create,
            "start": None,
            "end": None,
            "created_at": datetime.now(),
        }

        if not args.create in timers:
            timers[args.create] = []
        timers[args.create].append(new_timer)

        logger.info(f"Created new timer: {new_timer['label']}; id: {new_timer['id']}")
    elif args.delete:
        options: typing.List[Timer] = timers.get(args.delete, [])
        pass
    elif args.start:
        timer: typing.Optional[Timer] = get_timer(timers, args.start)
        if not timer:
            logger.debug(f"Timer {args.start} doesn't exist")
            exit(1)

        if timer["end"]:
            logger.debug(f"Cannot start timer {timer['label']} as it was stopped")

        if timer["start"]:
            logger.debug(f"Timer {timer['label']} has already started")
            exit(1)

        timer["start"] = datetime.now()
        logger.info(f"Started timer: {timer['label']}; id: {timer['id']}")
    elif args.finish:
        timer: typing.Optional[Timer] = get_timer(timers, args.finish)
        if not timer:
            logger.debug(f"Timer {args.finish} doesn't exist")
            exit(1)

        if not timer["start"]:
            logger.debug(f"Timer {timer['label']} was not started")
            exit(1)

        if timer["end"]:
            logger.debug(f"Timer {timer['label']} has already stopped")
            exit(1)

        timer["end"] = datetime.now()
        logger.info(f"Stopped timer: {timer['label']}; id: {timer['id']}")
    elif args.resume:
        timer: typing.Optional[Timer] = get_timer(timers, args.resume)
        if not timer:
            logger.debug(f"Timer {args.resume} doesn't exist")
            exit(1)

        if not timer["start"]:
            logger.debug(f"Timer {timer['label']} was not started")
            exit(1)

        if not timer["end"]:
            logger.debug(f"Timer {timer['label']} was not yet stopped")
            exit(1)

        new_timer: Timer = {
            "id": len(timers.get(args.resume, [])) + 1,
            "label": args.resume,
            "start": datetime.now(),
            "end": None,
            "created_at": datetime.now(),
        }

        if not args.resume in timers:
            timers[args.resume] = []
        timers[args.resume].append(new_timer)
        logger.info(f"Resumed timer for: {new_timer['label']}; id: {new_timer['id']}")
    if args.view:
        display_timers(timers.get(args.view, []), args.view)

    args.log.seek(0)
    writer.writeheader()
    writer.writerows(list(chain(*timers.values())))
    args.log.close()
