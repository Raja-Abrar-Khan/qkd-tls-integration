
import json
import hashlib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
QLL_DIR = BASE_DIR / "qll"
KMS_POOL_DIR = BASE_DIR / "kms" / "key_pool"


def _load_and_validate(path):
    """Load a key block and verify its basic integrity."""
    if not path.exists():
        raise FileNotFoundError(f"Key block not found: {path.name}")

    block = json.loads(path.read_text())

    block_id = block.get("blockId")
    key_hex = block.get("key")
    expected_hash = block.get("sha256")

    if not block_id or not isinstance(key_hex, str):
        raise ValueError("Invalid key-block metadata.")

    try:
        key_bytes = bytes.fromhex(key_hex)
    except ValueError as exc:
        raise ValueError("Invalid hexadecimal key.") from exc

    if len(key_bytes) != 32:
        raise ValueError("Expected a 256-bit (32-byte) key.")

    actual_hash = hashlib.sha256(key_bytes).hexdigest()

    if actual_hash != expected_hash:
        raise ValueError("Key integrity check failed.")

    if block.get("keyBits") != 256 or block.get("size") != 32:
        raise ValueError("Key-block size metadata is invalid.")

    return block


def New_Key(block_id):
    """Register a QLL key block in the KMS pool."""
    source = QLL_DIR / f"{block_id}.json"
    destination = KMS_POOL_DIR / f"{block_id}.json"

    block = _load_and_validate(source)

    if block["blockId"] != block_id:
        raise ValueError("Block ID does not match the filename.")

    KMS_POOL_DIR.mkdir(parents=True, exist_ok=True)

    if destination.exists():
        existing = _load_and_validate(destination)

        if existing != block:
            raise ValueError("A different block already uses this ID.")

        status = "already registered"
    else:
        with destination.open("x") as file:
            json.dump(block, file, indent=4)

        status = "registered successfully"

    return {
        "blockId": block_id,
        "status": status,
        "keyBits": block["keyBits"],
    }


def Get_Key(block_id):
    """Retrieve key material by its block ID."""
    path = KMS_POOL_DIR / f"{block_id}.json"
    block = _load_and_validate(path)

    if block["blockId"] != block_id:
        raise ValueError("Block ID does not match the filename.")

    # Return the secret to the calling application.
    # Never print the secret key to the terminal.
    return block["key"]
