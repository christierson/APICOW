import os
import subprocess


def main():
    blacklist = ["testing.py", "upload.py"]
    command = "ampy -p /dev/ttyACM0 put".split(" ")
    files = [file for file in os.listdir("pico") if file.endswith(".py")]
    for file in [file for file in files if file not in blacklist]:
        print("Uploading", file)
        subprocess.run(command + [file])
    pass


if __name__ == "__main__":
    main()


# ampy -p /dev/ttyACM0 put main.py
# ampy -p / dev/ttyACM0 put component.py
# ampy -p / dev/ttyACM0 put api.py
# ampy -p / dev/ttyACM0 put board.py
