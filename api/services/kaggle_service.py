import json
import os
import shutil
from kaggle.api.kaggle_api_extended import KaggleApi
from api.core.config import get_settings

class KaggleService:
    def __init__(self, username: str = None, key: str = None, nb_path: str = None, metadata_path: str = None):
        self.settings = get_settings()
        
        # Use provided args or default to settings (Musetalk defaults)
        self.username = username or self.settings.KAGGLE_USERNAME
        self.key = key or self.settings.KAGGLE_KEY
        self.nb_path = nb_path or self.settings.NB_PATH
        self.metadata_path = metadata_path or self.settings.METADATA_PATH

        self._setup_auth()
        self.api = KaggleApi()
        self.api.authenticate()

    def _setup_auth(self):
        if not self.username or not self.key:
            raise ValueError("Kaggle credentials not provided. Please set KAGGLE_USERNAME and KAGGLE_KEY environment variables.")
            
        # Set environment variables for Kaggle API to pick up
        os.environ["KAGGLE_USERNAME"] = self.username
        os.environ["KAGGLE_KEY"] = self.key

    def prepare_and_push(self, clean_metadata: bool = False) -> str:
        """
        Copies notebook and metadata to /tmp, updates metadata for GPU, and pushes.
        Returns the kernel ID status message.
        """
        # Vercel (and Lambda) writable directory is /tmp
        # Use a unique dir based on username to avoid conflicts if needed
        work_dir = f"/tmp/kaggle_work_{self.username}_{clean_metadata}"
        if os.path.exists(work_dir):
            shutil.rmtree(work_dir)
        os.makedirs(work_dir)

        # Copy files to proper locations in /tmp
        
        # We need to find where 'data' actually is.
        base_dir = os.getcwd()
        nb_src = os.path.join(base_dir, self.nb_path)
        meta_src = os.path.join(base_dir, self.metadata_path)

        if not os.path.exists(nb_src):
            raise FileNotFoundError(f"Notebook not found at {nb_src}")

        # Destination filenames must match what is expected in metadata if it refers to code_file
        # We grab the code_file name from metadata
        with open(meta_src, 'r') as f:
            metadata = json.load(f)
            
        code_file_name = metadata.get("code_file", "notebook.ipynb")
        
        # Sanitize Notebook Content (remove TPU accelerator from internal metadata)
        with open(nb_src, 'r') as f:
            nb_content = json.load(f)
            
        if "metadata" in nb_content and "kaggle" in nb_content["metadata"]:
            k_meta = nb_content["metadata"]["kaggle"]
            if "accelerator" in k_meta:
                del k_meta["accelerator"]
            if "dockerImageVersionId" in k_meta:
                del k_meta["dockerImageVersionId"]
            k_meta["isGpuEnabled"] = True
            
        # Write the sanitized notebook to work_dir
        with open(os.path.join(work_dir, code_file_name), 'w') as f:
            json.dump(nb_content, f, indent=4)
        
        # Force GPU settings
        metadata["enable_gpu"] = True
        metadata["enable_tpu"] = False
        if "machine_shape" in metadata:
            del metadata["machine_shape"]
            
        if clean_metadata:
            if "id_no" in metadata:
                del metadata["id_no"]
            if "docker_image" in metadata:
                del metadata["docker_image"]
            
        # Write modified metadata to work_dir
        with open(os.path.join(work_dir, "kernel-metadata.json"), 'w') as f:
            json.dump(metadata, f, indent=4)
            
        print(f"DEBUG: Files in {work_dir}: {os.listdir(work_dir)}")

        # Push
        # kernels_push expects the directory containing kernel-metadata.json
        try:
            result = self.api.kernels_push(work_dir)
            return f"Push success: {result}"
        except Exception as e:
            # Catch KaggleApi errors
            raise e
