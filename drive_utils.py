#  Auth + folder lookup + save/load helpers, shared by every notebook.
#  save_or_upload_csv/geojson/text default to config.SAVE_MODE.

import io
import pickle
import re
import tempfile
import time
from pathlib import Path

import pandas as pd

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import (
    MediaFileUpload,
    MediaIoBaseDownload,
    MediaIoBaseUpload,
)

from config import CREDENTIALS_JSON, SAVE_MODE as _DEFAULT_SAVE_MODE, TOKEN_PICKLE

DRIVE_SCOPES = ["https://www.googleapis.com/auth/drive"]

_service_cache = None


def get_drive_service():
    # authenticated Drive v3 service, cached across calls in this process
    global _service_cache
    if _service_cache is not None:
        return _service_cache
    creds = None
    token_path = Path(TOKEN_PICKLE)
    if token_path.exists():
        with open(token_path, "rb") as f:
            creds = pickle.load(f)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_JSON, DRIVE_SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, "wb") as f:
            pickle.dump(creds, f)
    _service_cache = build("drive", "v3", credentials=creds)
    return _service_cache


# Folders

def find_folder(service, name, parent_id=None):
    # folder id by name, optionally scoped to a parent, None if not found
    if service is None:
        return None
    try:
        q = (f"name='{name}' and "
             "mimeType='application/vnd.google-apps.folder' and trashed=false")
        if parent_id:
            q += f" and '{parent_id}' in parents"
        files = service.files().list(
            q=q, fields="files(id,name)",
            supportsAllDrives=True, includeItemsFromAllDrives=True,
        ).execute().get("files", [])
        return files[0]["id"] if files else None
    except Exception:
        return None


def get_or_create_folder(service, name, parent_id=None, max_retries=5):
    # folder id by name, creating it under parent_id if missing
    if service is None:
        return None
    fid = find_folder(service, name, parent_id)
    if fid:
        return fid
    body = {"name": name, "mimeType": "application/vnd.google-apps.folder"}
    if parent_id:
        body["parents"] = [parent_id]
    for attempt in range(max_retries):
        try:
            return service.files().create(body=body, fields="id", supportsAllDrives=True).execute()["id"]
        except Exception as e:
            if "429" in str(e) or "ratelimitexceeded" in str(e).lower():
                wait = 10 * (attempt + 1)
                print(f"  Rate limit — folder create waiting {wait}s")
                time.sleep(wait)
            else:
                print(f"  WARNING: could not create folder {name} — {e}")
                return None
    return None


def list_files_in_folder(service, folder_id):
    # all files directly inside a folder, paginated
    if service is None or not folder_id:
        return []
    try:
        files, page_token = [], None
        while True:
            kwargs = dict(
                q=f"'{folder_id}' in parents and trashed=false",
                fields="nextPageToken,files(id,name,createdTime,modifiedTime,mimeType)",
                pageSize=1000, supportsAllDrives=True, includeItemsFromAllDrives=True,
                orderBy="createdTime desc",
            )
            if page_token:
                kwargs["pageToken"] = page_token
            resp = service.files().list(**kwargs).execute()
            files.extend(resp.get("files", []))
            page_token = resp.get("nextPageToken")
            if not page_token:
                break
        return files
    except Exception:
        return []


def drive_file_exists(service, folder_id, filename):
    # file id of filename inside folder_id, or None
    if service is None or folder_id is None:
        return None
    try:
        q = f"name='{filename}' and '{folder_id}' in parents and trashed=false"
        files = service.files().list(q=q, fields="files(id, name)").execute().get("files", [])
        return files[0]["id"] if files else None
    except Exception:
        return None


# Downloads 

def _drain(request):
    # runs a media request to completion, returns the bytes
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    return fh.getvalue()


def download_bytes(service, file_id):
    # raw bytes of a Drive file
    request = service.files().get_media(fileId=file_id, supportsAllDrives=True)
    return _drain(request)


def download_text(service, file_id):
    # Drive file content as text, exporting Docs/Sheets to plain text/csv
    meta = service.files().get(fileId=file_id, fields="mimeType", supportsAllDrives=True).execute()
    mime = meta.get("mimeType", "")
    if mime == "application/vnd.google-apps.document":
        request = service.files().export_media(fileId=file_id, mimeType="text/plain")
    elif mime == "application/vnd.google-apps.spreadsheet":
        request = service.files().export_media(fileId=file_id, mimeType="text/csv")
    else:
        request = service.files().get_media(fileId=file_id)
    return _drain(request).decode("utf-8-sig")


def download_drive_file(service, file_id, dest_path):
    # downloads a Drive file straight to a local path
    with open(dest_path, "wb") as f:
        f.write(download_bytes(service, file_id))


# Uploads

def upload_bytes(service, data, filename, mimetype, folder_id, max_retries=5):
    # uploads bytes to Drive, overwriting any same-named file
    if service is None or folder_id is None:
        return
    try:
        existing = service.files().list(
            q=f"name='{filename}' and '{folder_id}' in parents and trashed=false",
            fields="files(id)", supportsAllDrives=True, includeItemsFromAllDrives=True,
        ).execute().get("files", [])
        for f in existing:
            service.files().delete(fileId=f["id"]).execute()
    except Exception:
        pass
    buffer = io.BytesIO(data)
    media = MediaIoBaseUpload(buffer, mimetype=mimetype, resumable=False)
    for attempt in range(max_retries):
        try:
            service.files().create(
                body={"name": filename, "parents": [folder_id]},
                media_body=media, fields="id", supportsAllDrives=True,
            ).execute()
            return
        except Exception as e:
            if "429" in str(e) or "ratelimitexceeded" in str(e).lower():
                wait = 10 * (attempt + 1)
                print(f"  Rate limit hit — waiting {wait}s (attempt {attempt + 1}/{max_retries})")
                time.sleep(wait)
            else:
                print(f"  WARNING: upload failed for {filename} — {e}")
                return


def upload_text(service, text, filename, folder_id):
    # uploads text to Drive as a plain file, not converted to Sheets
    mimetype = (
        "text/csv" if filename.endswith(".csv")
        else "text/markdown" if filename.endswith(".md")
        else "text/plain"
    )
    upload_bytes(service, text.encode("utf-8"), filename, mimetype, folder_id)


def upload_file(service, local_path, folder_id, overwrite=True):
    # uploads an existing local file to Drive
    if service is None or folder_id is None:
        return
    local_path = Path(local_path)
    existing_id = drive_file_exists(service, folder_id, local_path.name)
    media = MediaFileUpload(str(local_path), resumable=True)
    if existing_id and overwrite:
        service.files().update(fileId=existing_id, media_body=media).execute()
    else:
        service.files().create(
            body={"name": local_path.name, "parents": [folder_id]},
            media_body=media, fields="id",
        ).execute()


def upload_with_retry(service, body, media, max_retries=5):
    # create() with backoff retry, for flaky uploads
    for attempt in range(max_retries):
        try:
            return service.files().create(body=body, media_body=media, fields="id").execute()
        except (TimeoutError, HttpError, Exception) as e:
            wait = 2 ** attempt
            print(f"  Upload failed (attempt {attempt + 1}/{max_retries}): {e}. Retrying in {wait}s...")
            time.sleep(wait)
    raise Exception("Failed to upload after retries")


# "Find latest" helpers 
# For pipeline stages that pick up the newest output of an earlier stage automatically (e.g. the newest eval_all_ run, the newest scores_cache_N.json)


def find_latest_folder_local(base_dir, prefix, prefer_prefix=None):
    # newest local subfolder starting with prefix, by mtime
    folders = list_latest_folders_local(base_dir, prefix, prefer_prefix=prefer_prefix)
    return folders[0] if folders else None


def find_latest_folder_drive(service, parent_folder_id, prefix, prefer_prefix=None):
    # same as find_latest_folder_local, via Drive
    folders = list_latest_folders_drive(service, parent_folder_id, prefix, prefer_prefix=prefer_prefix)
    return folders[0] if folders else None


def list_latest_folders_local(base_dir, prefix, prefer_prefix=None):
    # local subfolders starting with prefix, newest first
    base_dir = Path(base_dir)
    if not base_dir.exists():
        return []
    candidates = [d for d in base_dir.iterdir() if d.is_dir() and d.name.startswith(prefix)]
    if prefer_prefix:
        preferred = [d for d in candidates if d.name.startswith(prefer_prefix)]
        if preferred:
            candidates = preferred
    return sorted(candidates, key=lambda d: d.stat().st_mtime, reverse=True)


def list_latest_folders_drive(service, parent_folder_id, prefix, prefer_prefix=None):
    # same as list_latest_folders_local, via Drive
    if service is None or not parent_folder_id:
        return []
    candidates = [
        f for f in list_files_in_folder(service, parent_folder_id)
        if f.get("mimeType") == "application/vnd.google-apps.folder" and f["name"].startswith(prefix)
    ]
    if prefer_prefix:
        preferred = [f for f in candidates if f["name"].startswith(prefer_prefix)]
        if preferred:
            candidates = preferred
    return sorted(candidates, key=lambda f: f["createdTime"], reverse=True)


def find_latest_versioned_file_local(base_dir, base_name, ext):
    # highest-numbered base_name_N.ext file locally
    base_dir = Path(base_dir)
    if not base_dir.exists():
        return None, None
    pattern = re.compile(rf"^{re.escape(base_name)}_(\d+)\.{re.escape(ext)}$")
    candidates = []
    for f in base_dir.iterdir():
        m = pattern.match(f.name)
        if m:
            candidates.append((int(m.group(1)), f))
    if not candidates:
        return None, None
    version, path = max(candidates, key=lambda x: x[0])
    return path, version


def find_latest_versioned_file_drive(service, folder_id, base_name, ext):
    # same as find_latest_versioned_file_local, via Drive
    if service is None or not folder_id:
        return None, None
    pattern = re.compile(rf"^{re.escape(base_name)}_(\d+)\.{re.escape(ext)}$")
    candidates = []
    for f in list_files_in_folder(service, folder_id):
        m = pattern.match(f["name"])
        if m:
            candidates.append((int(m.group(1)), f))
    if not candidates:
        return None, None
    version, file_resource = max(candidates, key=lambda x: x[0])
    return file_resource, version


#  Local + Drive save
# save_mode defaults to config.SAVE_MODE when the caller doesn't pass one

_TIER_FLOAT_RE = re.compile(r"^-?\d+\.0$")

def normalize_tier_column(df, col="geocoding_tier"):
    # strips trailing '.0' from numeric tier values (e.g. 9.0 -> 9)
    if col not in df.columns:
        return df
    df = df.copy()
    def _fix(v):
        if v is None:
            return v
        s = str(v).strip()
        if _TIER_FLOAT_RE.match(s):
            return s[:-2]
        return v
    df[col] = df[col].apply(_fix)
    return df


def save_or_upload_csv(df, path, service=None, folder_id=None, save_mode=None):
    # writes a df locally and/or to Drive per save_mode
    save_mode = save_mode or _DEFAULT_SAVE_MODE
    if save_mode in ("local", "both"):
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(path, index=False)
        except OSError as e:
            print(f"  WARNING: local write failed for {path.name} — {e}")
    if save_mode in ("drive", "both") and service and folder_id:
        buf = io.StringIO()
        df.to_csv(buf, index=False)
        upload_text(service, buf.getvalue(), path.name, folder_id)


def save_or_upload_geojson(gdf, path, service=None, folder_id=None, save_mode=None):
    # writes a gdf locally and/or to Drive per save_mode
    save_mode = save_mode or _DEFAULT_SAVE_MODE
    if save_mode in ("local", "both"):
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            gdf.to_file(path, driver="GeoJSON")
        except OSError as e:
            print(f"  WARNING: local write failed for {path.name} — {e}")
    if save_mode in ("drive", "both") and service and folder_id:
        with tempfile.NamedTemporaryFile(suffix=".geojson", delete=False) as tmp:
            tmp_path = Path(tmp.name)
        gdf.to_file(tmp_path, driver="GeoJSON")
        upload_bytes(service, tmp_path.read_bytes(), path.name, "application/geo+json", folder_id)
        tmp_path.unlink()


def save_or_upload_text(text, path, service=None, folder_id=None, save_mode=None):
    # writes text locally and/or to Drive per save_mode
    save_mode = save_mode or _DEFAULT_SAVE_MODE
    if save_mode in ("local", "both"):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    if save_mode in ("drive", "both") and service and folder_id:
        upload_text(service, text, path.name, folder_id)


def get_run_folder_id(root_folder_name, geospatial_folder_name, subfolder_name, run_name):
    # gets/creates ROOT/GEOSPATIAL/subfolder/run_name on Drive
    if _DEFAULT_SAVE_MODE not in ("drive", "both"):
        return None, None
    svc  = get_drive_service()
    root = find_folder(svc, root_folder_name)
    geo  = get_or_create_folder(svc, geospatial_folder_name, root)
    sub  = get_or_create_folder(svc, subfolder_name, geo)
    run  = get_or_create_folder(svc, run_name, sub)
    return svc, run


def find_csv_by_name(name_contains, local_dir, drive_folder_id, service=None,
                      exclude_prefixes=(), exclude_suffixes=(".geojson",)):
    # csv by partial filename match, local first then Drive
    def _is_candidate(name):
        return (name_contains in name
                and not any(name.endswith(s) for s in exclude_suffixes)
                and not any(name.startswith(p) for p in exclude_prefixes))

    local_dir = Path(local_dir)
    if _DEFAULT_SAVE_MODE in ("local", "both") and local_dir.exists():
        local_matches = [p for p in local_dir.rglob("*") if p.is_file() and _is_candidate(p.name)]
        if local_matches:
            local_matches.sort(key=lambda p: p.stat().st_mtime, reverse=True)
            p = local_matches[0]
            if len(local_matches) > 1:
                print(f"  NOTE: '{name_contains}' matched {len(local_matches)} local files — using newest: {p.name}")
            try:
                print(f"  Local: {p.name}")
                return pd.read_csv(p), {"name": p.name}
            except OSError as e:
                print(f"  WARNING: local read failed for {p.name} ({e}) — falling back to Drive.")

    service = service or get_drive_service()
    if _DEFAULT_SAVE_MODE not in ("drive", "both") or drive_folder_id is None:
        print(f"  WARNING: '{name_contains}' not found locally and Drive unavailable.")
        return pd.DataFrame(), None

    files = list_files_in_folder(service, drive_folder_id)
    matches = [x for x in files if _is_candidate(x["name"])]
    if not matches:
        print(f"  WARNING: '{name_contains}' not found locally or on Drive.")
        return pd.DataFrame(), None
    matches.sort(key=lambda x: x.get("createdTime", ""), reverse=True)
    f = matches[0]
    if len(matches) > 1:
        print(f"  NOTE: '{name_contains}' matched {len(matches)} Drive files — using newest: {f['name']}")
    print(f"  Drive: {f['name']}")
    try:
        return pd.read_csv(io.StringIO(download_text(service, f["id"]))), f
    except Exception as e:
        print(f"  WARNING: could not load {f['name']} — {e}")
        return pd.DataFrame(), None


def find_run_folder(local_base, drive_parent_id, name_prefix, required_substrings, service=None):
    # latest run folder containing all of required_substrings
    service = service or get_drive_service()
    local_base = Path(local_base)
    local_match = None
    if _DEFAULT_SAVE_MODE in ("local", "both") and local_base.exists():
        candidates = sorted(
            (d for d in local_base.iterdir() if d.is_dir() and d.name.startswith(name_prefix)),
            key=lambda d: d.name[len(name_prefix):], reverse=True
        )
        for d in candidates:
            names = [p.name for p in d.iterdir()]
            if all(any(req in n for n in names) for req in required_substrings):
                local_match = d
                break

    drive_id = drive_name = None
    if _DEFAULT_SAVE_MODE in ("drive", "both") and drive_parent_id is not None:
        if local_match is not None:
            _existing = service.files().list(
                q=f"name='{local_match.name}' and '{drive_parent_id}' in parents "
                  "and trashed=false and mimeType='application/vnd.google-apps.folder'",
                fields="files(id,name)",
                supportsAllDrives=True, includeItemsFromAllDrives=True
            ).execute().get("files", [])
            if _existing:
                drive_id, drive_name = _existing[0]["id"], _existing[0]["name"]
        else:
            folders = service.files().list(
                q=f"'{drive_parent_id}' in parents and trashed=false and "
                  "mimeType='application/vnd.google-apps.folder'",
                fields="files(id,name,createdTime)",
                orderBy="createdTime desc",
                supportsAllDrives=True, includeItemsFromAllDrives=True
            ).execute().get("files", [])
            for folder in folders:
                if not folder["name"].startswith(name_prefix):
                    continue
                contents = list_files_in_folder(service, folder["id"])
                names = [f["name"] for f in contents]
                if all(any(req in n for n in names) for req in required_substrings):
                    drive_id, drive_name = folder["id"], folder["name"]
                    break

    if local_match is not None:
        print(f"  Local run folder: {local_match.name}")
        return local_match, drive_id, local_match.name
    if drive_name:
        print(f"  Drive run folder: {drive_name}")
        return None, drive_id, drive_name
    return None, None, None
