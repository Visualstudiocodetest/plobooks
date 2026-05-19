import os
import hashlib
from typing import Optional

import httpx


def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def _ext_from_content_type(ct: str) -> Optional[str]:
    if not ct:
        return None
    ct = ct.lower()
    if ct.startswith('image/'):
        ext = ct.split('image/')[-1].split(';')[0].strip()
        if ext == 'jpeg':
            return 'jpg'
        # guard simple cases
        if '/' in ext or ext == '':
            return None
        return ext
    return None


def download_image(url: str, save_dir: str = 'static/images/books', max_bytes: int = 5 * 1024 * 1024) -> str:
    """
    Download an image from `url`, save it under `save_dir` (raw bytes) and return the relative path
    (eg. '/static/images/books/<hash>.jpg'). Raises Exception on failure.
    """
    if not url or not url.lower().startswith(('http://', 'https://')):
        raise ValueError('Invalid URL')

    _ensure_dir(save_dir)

    # Use a stable filename based on the URL
    h = hashlib.sha256(url.encode('utf-8')).hexdigest()

    with httpx.Client(timeout=10.0) as client:
        with client.stream('GET', url, follow_redirects=True, timeout=10.0) as resp:
            resp.raise_for_status()
            content_type = resp.headers.get('content-type', '')
            ext = _ext_from_content_type(content_type)

            # fallback to extension from URL
            if not ext:
                path_part = url.split('?')[0]
                maybe = os.path.splitext(path_part)[1].lstrip('.')
                ext = maybe or 'jpg'

            filename = f"{h}.{ext}"
            tmp_path = os.path.join(save_dir, f"{h}.tmp")
            final_path = os.path.join(save_dir, filename)

            # If already exists, return quickly
            if os.path.exists(final_path):
                return f"/static/images/books/{filename}"

            bytes_written = 0
            with open(tmp_path, 'wb') as f:
                for chunk in resp.iter_bytes():
                    if not chunk:
                        continue
                    bytes_written += len(chunk)
                    if bytes_written > max_bytes:
                        # cleanup
                        try:
                            f.close()
                        except Exception:
                            pass
                        try:
                            os.remove(tmp_path)
                        except Exception:
                            pass
                        raise Exception('Image too large')
                    f.write(chunk)

            os.replace(tmp_path, final_path)

    return f"/static/images/books/{filename}"
