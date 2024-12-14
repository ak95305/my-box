from flask import Response, json, Blueprint
import subprocess
from src import config

dashboard = Blueprint("dashboard", __name__)

@dashboard.route("/get-disk-storage", methods=['GET'])
def get_disk_storage():
    try:
        result = subprocess.run(['df', "-B1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        resp = dict()

        if result.returncode == 0:
            print("Disk Storage Information:")
            data = formatDiskStorageData(result.stdout)

            if(data['1B-blocks']):
                resp['total_space'] = convertBytes(data['1B-blocks'])
            if(data['Available']):
                resp['free_space'] = convertBytes(data['Available'])
            if(data['Used']):
                resp['used_spave'] = convertBytes(data['Used'])
        else:
            print("Error:", result.stderr)
        
        return Response(
            response=json.dumps({'status': True, "data": data}),
            status=200,
            mimetype='application/json'
        )

    except Exception as e:
        print(f"An error occurred: {e}")


def formatDiskStorageData(data):
    lines = data.strip().split("\n")
    header = lines[0].split()

    disks = []

    for line in lines[1:]:
        values = line.split()
        entry = dict(zip(header, values))
        disks.append(entry)

    storageDisk = None
    for disk in disks:
        if disk['Filesystem'] == config.DISKNAME:
            storageDisk = disk

    return storageDisk


def convertBytes(bytes, format = "GB"):
        bytes = int(bytes)

        if format == "GB":
            return ((bytes/1024)/1024)/1024
        elif format == "MB":
            return (bytes/1024)/1024
        elif format == "KB":
            return bytes/1024