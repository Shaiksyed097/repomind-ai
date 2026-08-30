import os
import shutil
import time


QDRANT_PATH = r"C:\RepoMindData\qdrant"


print("=" * 60)
print("REPOMIND QDRANT COMPLETE RESET")
print("=" * 60)

print()
print("Qdrant storage:")
print(QDRANT_PATH)


# ============================================================
# CHECK PATH
# ============================================================

if os.path.exists(QDRANT_PATH):

    print()
    print("Existing Qdrant storage found.")

    # --------------------------------------------------------
    # Try deleting the complete local Qdrant database
    # --------------------------------------------------------

    try:

        shutil.rmtree(
            QDRANT_PATH
        )

        print(
            "Old Qdrant storage deleted successfully."
        )

    except PermissionError:

        print()
        print(
            "ERROR: Qdrant storage is currently locked."
        )

        print()
        print(
            "Close Streamlit and all Python processes."
        )

        raise SystemExit(1)

    except OSError as error:

        print()
        print(
            f"ERROR: Could not delete Qdrant storage:\n"
            f"{error}"
        )

        raise SystemExit(1)

else:

    print()
    print(
        "No existing Qdrant storage found."
    )


# ============================================================
# CREATE EMPTY DIRECTORY
# ============================================================

os.makedirs(
    QDRANT_PATH,
    exist_ok=True
)

print()
print(
    "Created empty Qdrant storage directory."
)


# ============================================================
# VERIFY
# ============================================================

remaining_files = list(
    os.scandir(
        QDRANT_PATH
    )
)


print()

if remaining_files:

    print(
        "WARNING: Qdrant directory is not empty."
    )

    for item in remaining_files:

        print(
            f" - {item.name}"
        )

else:

    print(
        "Qdrant storage is completely empty."
    )


print()
print("=" * 60)
print("QDRANT RESET COMPLETED")
print("=" * 60)