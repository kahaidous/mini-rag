from .BaseController import BaseController
from fastapi import UploadFile
from models import ResponseSignal
class DataController(BaseController):

    def __init__(self):
        super().__init__()

    def validate_upload_file(self, file: UploadFile):
        if file.content_type not in self.settings.FILE_ALLOWED_TYPES:
            return False, ResponseSignal.FILE_TYPE_NOT_ALLOWED
        if file.size > self.settings.FILE_MAX_SIZE * 1024 * 1024:
            return False, ResponseSignal.FILE_SIZE_EXCEEDED
        return True, ResponseSignal.FILE_UPLOAD_SUCCESS