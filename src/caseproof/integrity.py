
import hashlib


def calculate_sha256(file_path):
    """
    Calculate the SHA-256 hash of a file.
    """

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def verify_integrity(file_path, original_hash):
    """
    Compare the current file hash with the recorded hash.
    """

    current_hash = calculate_sha256(file_path)

    if current_hash == original_hash:
        return True, "Evidence integrity verified."

    return False, "WARNING: Evidence file may have been modified."
