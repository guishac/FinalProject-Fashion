import os
import mimetypes
import arrow


def datetimeformat(date_str):
    dt = arrow.get(date_str)
    return dt.humanize()


def file_type(key):
    file_info = os.path.splitext(key)
    file_extension = file_info[1]
    return file_extension
    # return file_info
    # return mimetypes.types_map[file_extension]
    # try:
    #     return mimetypes.types_map[file_extension]
    # except KeyError():
    #     return 'Unknown'
    # print(file_info)