import time

from getchar import getkeys


def main() -> None:
    while True:
        print("Press any key, or F4 to quit:")
        while not len((c := getkeys())):
            time.sleep(.1)
        if not c:
            continue
        print("You pressed:", c)
        if c[0] == "\x00>":
            break


if __name__ == "__main__":
    main()
