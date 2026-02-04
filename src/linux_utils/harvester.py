import os
import subprocess
from linux_utils.requirements import auto_setup


@auto_setup
def run_harvest(root_dir, output_file):
    root_dir = os.path.abspath(os.path.expanduser(root_dir))
    output_path = os.path.abspath(output_file)

    ignore_exts = {
        ".ttf",
        ".otf",
        ".png",
        ".jpg",
        ".pdf",
        ".pyc",
        ".exe",
        ".deb",
        ".zip",
    }
    ignore_dirs = {"node_modules", "__pycache__", ".git", "local-repo"}
    skip_files = {"secrets.yml", os.path.basename(output_path)}

    print(f"Harvesting: {root_dir}")

    with open(output_path, "w", encoding="utf-8") as f_out:
        f_out.write(f"=== DIRECTORY STRUCTURE ===\n\n")

        exclude_pattern = "|".join(skip_files)
        tree_cmd = ["tree", "-a", "-I", exclude_pattern, root_dir]
        f_out.write(subprocess.check_output(tree_cmd, text=True))

        f_out.write("\n\n=== FILE CONTENTS ===\n")
        for root, dirs, files in os.walk(root_dir):
            dirs[:] = [
                d for d in dirs if not d.startswith(".") and d not in ignore_dirs
            ]

            for name in sorted(files):
                full_path = os.path.join(root, name)
                if (
                    name in skip_files
                    or name.startswith(".")
                    or any(name.lower().endswith(e) for e in ignore_exts)
                ):
                    continue

                f_out.write(
                    f"\n{'#' * 40}\n### {os.path.relpath(full_path, root_dir)}\n{'#' * 40}\n"
                )
                try:
                    with open(
                        full_path, "r", encoding="utf-8", errors="ignore"
                    ) as f_in:
                        f_out.write(f_in.read())
                except Exception as e:
                    f_out.write(f"[Error: {e}]")

    print(f"Done! Saved to {output_path}")
