import re
from datetime import datetime
from typing import List, Dict, Any
from backend.utitlites.s3_storage import list_files, delete_file as s3_delete_file, get_s3_key, S3_BASE_PREFIX


class ProjectFileService:

    @staticmethod
    def get_project_files(project_id: str, category: str) -> List[Dict[str, Any]]:
        prefix = f"{S3_BASE_PREFIX}/pmo/{project_id}/"
        s3_objects = list_files(prefix)

        if not s3_objects:
            return []

        files_list = []
        category_pattern = re.compile(f"(?i)(^|_{re.escape(category)})_")

        for obj in s3_objects:
            s3_key = obj["Key"]
            filename = s3_key.split("/")[-1]

            if not filename:
                continue

            match = category_pattern.search(filename)

            if match:
                size_kb = obj.get("Size", 0) / 1024
                upload_time = obj.get("LastModified", datetime.now())

                clean_display_name = filename[match.end():]

                files_list.append({
                    "file_name": filename,
                    "display_name": clean_display_name,
                    "size": f"{size_kb:.2f} KB",
                    "upload_date": upload_time,
                    "upload_date_str": upload_time.strftime("%Y-%m-%d %H:%M:%S")
                })

        files_list.sort(key=lambda x: x['upload_date'], reverse=True)
        return files_list

    @staticmethod
    def delete_project_file(project_id: str, filename: str) -> bool:
        s3_key = get_s3_key(project_id, filename, subfolder="pmo")
        try:
            s3_delete_file(s3_key)
            return True
        except Exception as e:
            print(f"Error deleting file from S3 {s3_key}: {e}")
            return False