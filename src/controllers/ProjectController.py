from controllers import BaseController
import os

class ProjectController(BaseController):
    def __init__(self):
        super().__init__()

    def get_project_path(self, project_id: str):
        """
        Get the path for a specific project based on its ID. If the directory does not exist, it will be created.
        """
        project_dir = os.path.join(self.files_dir, project_id)
        if not os.path.exists(project_dir):
            os.makedirs(project_dir)
        print(f"Project directory for {project_id}: {project_dir}")  # Debugging line
        return project_dir 