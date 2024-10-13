import argparse


def display_timers():
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="start/finish timers")
    group_crud = parser.add_mutually_exclusive_group()

    group_crud.add_argument("-c", "--create", help="creates new timer of given label")
    group_crud.add_argument("-d", "--delete", help="delete timer of given label")
    group_crud.add_argument("-s", "--start", help="start timer of given label")
    group_crud.add_argument("-f", "--finish", help="stops timer of given label")
    group_crud.add_argument("-r", "--resume", help="resumes timer of given label")

    parser.add_argument("-v", "--view", action="store_false")

    args = parser.parse_args()

    if args.create:
        pass
    elif args.delete:
        pass
    elif args.start:
        pass
    elif args.finish:
        pass
    elif args.resume:
        pass

    if args.view:
        display_timers()
