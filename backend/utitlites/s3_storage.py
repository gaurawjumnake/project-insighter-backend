import os
import boto3
from pathlib import Path

s3 = boto3.client("s3")
BUCKET = os.getenv("S3_BUCKET_NAME", "nit-project-insighter")
S3_BASE_PREFIX = "uploaded_docs"


def get_s3_key(account_id: str, filename: str, subfolder: str = "project_docs") -> str:
    return f"{S3_BASE_PREFIX}/{subfolder}/{account_id}/{filename}"


def upload_to_s3(local_path: Path, s3_key: str):
    s3.upload_file(str(local_path), BUCKET, s3_key)


def download_from_s3(s3_key: str, local_path: Path):
    s3.download_file(BUCKET, s3_key, str(local_path))


def list_files(prefix: str) -> list[dict]:
    resp = s3.list_objects_v2(Bucket=BUCKET, Prefix=prefix)
    return resp.get("Contents", [])


def delete_file(s3_key: str):
    s3.delete_object(Bucket=BUCKET, Key=s3_key)


def get_presigned_url(s3_key: str, expires: int = 3600) -> str:
    return s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": BUCKET, "Key": s3_key},
        ExpiresIn=expires,
    )
