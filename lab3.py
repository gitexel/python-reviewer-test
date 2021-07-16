# Make sure to update the <FMI1> with your bucket

import subprocess
import sys
import boto3
import datetime

s3 = boto3.client('s3')


def main(argv):
    cmd = determine_command(int(sys.argv[1]))
    log_file_name = datetime.datetime.now(datetime.timezone.utc).strftime("%m_%d_%Y") + "_logfile"
    kickoff_subprocess(cmd, log_file_name)
    upload_output_to_s3(log_file_name)


# instead of allowing free-form input
# we instead have them enter a number
# which corresponds to a command that is pre-written
# you also could present a menu that allows them to select the command
# but either way we are avoiding allowing free-form entry
def determine_command(user_input):
    if user_input == 1:
        return ['echo', "command1"]
    if user_input == 2:
        return ['echo', "command2"]
    if user_input == 3:
        return ['echo', "command3"]
    else:
        return ['echo', "default"]


def kickoff_subprocess(cmd, log_file_name):
    # Linux
    process = subprocess.call(cmd, shell=False)

    # Windows
    # process = subprocess.call(['cmd', '/c'], shell=False)

    file = open(log_file_name, "a+")
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%m/%d/%Y, %H:%M:%S")
    output = timestamp + " Command: " + cmd[0] + " | Return Code: " + str(process) + "\n"
    # context manager https://book.pythontips.com/en/latest/context_managers.html
    with open(log_file_name, 'a+') as file:
        file.write(output)


def upload_output_to_s3(log_file_name):
    # context manager https://book.pythontips.com/en/latest/context_managers.html
    with open(log_file_name, 'rb') as opened_file:
        file = open(log_file_name, "rb")
        s3.upload_fileobj(file, "<FMI1>", log_file_name)
        file.close()


if __name__ == "__main__":
    main(sys.argv[1:])
