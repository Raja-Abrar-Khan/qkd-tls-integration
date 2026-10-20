
import json
import hashlib
import secrets
from datetime import datetime, timezone
from pathlib import Path


# --------------------------------------------------
# Configuration
# --------------------------------------------------

QLL_DIR = Path("qll")
KMS_POOL_DIR = Path("kms/key_pool")
RAW_KEY_FILE = QLL_DIR / "raw_key.txt"

# --------------------------------------------------
# Step 1: Read the BB84-generated binary key
# --------------------------------------------------

if not RAW_KEY_FILE.exists():
    raise SystemExit(
        "BB84 key not found. Run python bb84.py first."
    )

binary_key = RAW_KEY_FILE.read_text().strip()

if len(binary_key) != 256 or any(
    bit not in "01" for bit in binary_key
):
    raise SystemExit(
        "Invalid key: expected exactly 256 binary bits."
    )

# --------------------------------------------------
# Step 2: Convert 256 bits into 32 bytes
# --------------------------------------------------

key_bytes = int(binary_key, 2).to_bytes(32, byteorder="big")

# Represent the bytes as 64 hexadecimal characters
hex_key = key_bytes.hex()

assert len(key_bytes) == 32
assert len(hex_key) == 64

# --------------------------------------------------
# Step 3: Create a unique key-block ID
# --------------------------------------------------

block_id = "block_" + secrets.token_hex(8)

key_block = {
    "blockId": block_id,
    "key": hex_key,
    "size": len(key_bytes),
    "keyBits": len(binary_key),
    "createdAt": datetime.now(timezone.utc).isoformat(),
    "sha256": hashlib.sha256(key_bytes).hexdigest()
}

# --------------------------------------------------
# Step 4: Store a copy in the QLL directory
# --------------------------------------------------

QLL_DIR.mkdir(parents=True, exist_ok=True)
KMS_POOL_DIR.mkdir(parents=True, exist_ok=True)

qll_file = QLL_DIR / f"{block_id}.json"
kms_file = KMS_POOL_DIR / f"{block_id}.json"

# Use exclusive creation so an existing block is not overwritten.
with qll_file.open("x") as f:
    json.dump(key_block, f, indent=4)

try:
    with kms_file.open("x") as f:
        json.dump(key_block, f, indent=4)
except Exception:
    # Avoid leaving an incomplete pair of copies.
    qll_file.unlink(missing_ok=True)
    raise

# --------------------------------------------------
# Step 5: Verify both stored copies
# --------------------------------------------------

qll_block = json.loads(qll_file.read_text())
kms_block = json.loads(kms_file.read_text())

if qll_block != kms_block:
    raise SystemExit("ERROR: Stored key blocks differ.")

print("\n========== KEY BLOCK CREATED ==========")
print("Block ID:        ", block_id)
print("Key size:        ", len(key_bytes), "bytes")
print("Key length:      ", len(binary_key), "bits")
print("Hex characters:  ", len(hex_key))
print("QLL copy:        ", qll_file)
print("KMS pool copy:   ", kms_file)
print("Copies identical:", qll_block == kms_block)
print("=======================================")
