from enum import Enum

class ResponseSignal(Enum):
    FILE_UPLOAD_SUCCESS = "File uploaded successfully."
    FILE_UPLOAD_FAILURE = "File upload failed."
    FILE_SIZE_EXCEEDED = "File size exceeds the maximum limit."
    FILE_TYPE_NOT_ALLOWED = "File type is not allowed."