import os
import boto3
import json
from pathlib import Path
from datetime import datetime
from typing import Optional
from uuid import UUID

s3 = boto3.client("s3")
BUCKET = os.getenv("S3_BUCKET_NAME", "nit-project-insighter")
S3_BASE_PREFIX = "uploaded_docs"
S3_TEMP_PREFIX = "temp"


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


def generate_data_s3_key(entity_id: str | UUID, entity_type: str) -> str:
    """
    Generate S3 key for DB-fetched data in temp folder.
    
    Args:
        entity_id: Account ID or Project ID
        entity_type: 'account', 'project', or 'private_equity'
    
    Returns:
        S3 key in format: temp/<entity_type>_<id>_<date>.json
    """
    entity_type = entity_type.lower()
    if entity_type not in ['account', 'project', 'private_equity']:
        raise ValueError("entity_type must be 'account', 'project', or 'private_equity'")
    
    date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{entity_type}_{str(entity_id)}_{date_str}.json"
    return f"{S3_TEMP_PREFIX}/{filename}"


def upload_data_to_s3(
    data: dict,
    entity_id: str | UUID,
    entity_type: str,
    custom_key: Optional[str] = None
) -> str:
    """
    Upload JSON data to S3 in temp folder with entity-aware naming.
    
    Args:
        data: Dictionary to upload as JSON
        entity_id: Account ID or Project ID
        entity_type: 'account', 'project', or 'private_equity'
        custom_key: Optional custom S3 key (generated if not provided)
    
    Returns:
        S3 key where data was uploaded
    """
    if custom_key:
        s3_key = custom_key
    else:
        s3_key = generate_data_s3_key(entity_id, entity_type)
    
    json_data = json.dumps(data, indent=2, default=str)
    s3.put_object(
        Bucket=BUCKET,
        Key=s3_key,
        Body=json_data.encode('utf-8'),
        ContentType='application/json'
    )
    return s3_key


def download_data_from_s3(s3_key: str) -> dict:
    """
    Download JSON data from S3.
    
    Args:
        s3_key: S3 key of the file
    
    Returns:
        Parsed JSON data as dictionary
    """
    response = s3.get_object(Bucket=BUCKET, Key=s3_key)
    data = json.loads(response['Body'].read().decode('utf-8'))
    return data


def download_data_to_local(
    s3_key: str,
    local_path: Optional[Path] = None
) -> Path:
    """
    Download data from S3 to local file.
    
    Args:
        s3_key: S3 key of the file
        local_path: Optional local path (generated if not provided)
    
    Returns:
        Path to downloaded file
    """
    if local_path is None:
        # Extract filename from S3 key
        filename = os.path.basename(s3_key)
        local_path = Path(f"./temp/{filename}")
        local_path.parent.mkdir(parents=True, exist_ok=True)
    
    download_from_s3(s3_key, local_path)
    return local_path
