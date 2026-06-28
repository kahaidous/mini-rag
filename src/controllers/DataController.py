import os

from fastapi import UploadFile
import re

from controllers import BaseController
from .ProjectController import ProjectController
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
    
    def generate_unique_filename(self, original_filename: str, project_id: str):
        """ Generate a unique filename by appending a random string to the original filename."""
        random_filename = self.generate_random_string()
        project_path = ProjectController().get_project_path(project_id)
        new_filepath = os.path.join(
            project_path,
            random_filename + "_" 
            + self.get_clean_filename(original_filename)
        )

        while os.path.exists(new_filepath):
            random_filename = self.generate_random_string()
            new_filepath = os.path.join(
                project_path,
                random_filename + "_" 
                + self.get_clean_filename(original_filename)
            )
        return new_filepath
    
    def get_clean_filename(self, original_filename:str):
        # Remove any special characters except underscores and periods
        clean_filename = re.sub(r'[^\w\.]', '', original_filename.strip()).replace(' ', '_')
        return clean_filename
        