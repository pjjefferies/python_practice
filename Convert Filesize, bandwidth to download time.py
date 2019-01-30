def convert_seconds(seconds):
    minutes = int(float(seconds) // 60)
    seconds = float(seconds) % 60
    hours   = int(float(minutes) // 60)
    minutes = int(float(minutes) % 60)
    if hours == 1:
        return_string = "1 hour, "
    else:
        return_string = str(hours) + " hours, "
    if minutes == 1:
        return_string += "1 minute, "
    else:
        return_string = return_string + str(minutes) + " minutes, "
    if seconds == 1:
        return_string += "1 second"
    else:
        return_string = return_string + str(seconds) + " seconds"
    return return_string

def download_time(file_size, file_size_units, bandwidth, bandwidth_units):
    if file_size_units == "kb":
        file_size_bytes = file_size * 2 ** 10
    elif file_size_units == "kB":
        file_size_bytes = file_size * 2 ** 10 * 8
    elif file_size_units == "Mb":
        file_size_bytes = file_size * 2 ** 20
    elif file_size_units == "MB":
        file_size_bytes = file_size * 2 ** 20 * 8
    elif file_size_units == "Gb":
        file_size_bytes = file_size * 2 ** 30
    elif file_size_units == "GB":
        file_size_bytes = file_size * 2 ** 30 * 8
    elif file_size_units == "Tb":
        file_size_bytes = file_size * 2 ** 40
    elif file_size_units == "TB":
        file_size_bytes = file_size * 2 ** 40 * 8
    else:
        return "Unidentified Filesize Unit"
    if bandwidth_units == "kb":
        bandwidth_bytes = bandwidth * 2 ** 10
    elif bandwidth_units == "kB":
        bandwidth_bytes = bandwidth * 2 ** 10 * 8
    elif bandwidth_units == "Mb":
        bandwidth_bytes = bandwidth * 2 ** 20
    elif bandwidth_units == "MB":
        bandwidth_bytes = bandwidth * 2 ** 20 * 8
    elif bandwidth_units == "Gb":
        bandwidth_bytes = bandwidth * 2 ** 30
    elif bandwidth_units == "GB":
        bandwidth_bytes = bandwidth * 2 ** 30 * 8
    elif bandwidth_units == "Tb":
        bandwidth_bytes = bandwidth * 2 ** 40
    elif bandwidth_units == "TB":
        bandwidth_bytes = bandwidth * 2 ** 40 * 8
    else:
        return "Unidentified Filesize Unit"
#    print file_size_bytes, bandwidth_bytes
    return convert_seconds(float(file_size_bytes) / bandwidth_bytes)