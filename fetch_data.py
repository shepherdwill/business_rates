"""
Run this first to download VOA rating list data.
Data is not committed to the repo — see README for instructions.
2026 data is currently draft (re-run after April 2026)
"""
import requests, os, zipfile, io

RAW_DIR = "data/raw"
os.makedirs(RAW_DIR, exist_ok=True)

FILES = {
    "voa_2026_draft_baseline.zip": "uk-englandwales-ndr-2026-draft-listentries-epoch-0002-baseline-csv.zip",
    "voa_2023_list.zip": "uk-englandwales-ndr-2023-listentries-compiled-epoch-0019-baseline-csv.zip"
}
BASE_URL = "https://voaratinglists.blob.core.windows.net/downloads/"

for local_name, remote_name in FILES.items():
    dest = os.path.join(RAW_DIR, local_name)
    if os.path.exists(dest):
        print(f"Already exists: {local_name}")
        continue
    print(f"Downloading {remote_name}...")
    r = requests.get(BASE_URL + remote_name, stream=True)
    with open(dest, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Saved to {dest}")


import requests
import xml.etree.ElementTree as ET

list_url = "https://voaratinglists.blob.core.windows.net/downloads?restype=container&comp=list"
response = requests.get(list_url)

root = ET.fromstring(response.content)
for blob in root.iter("Blob"):
    name = blob.find("Name").text
    if "2023" in name and "listentries" in name:
        print(name)