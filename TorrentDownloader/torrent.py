import os
import subprocess

def download_with_aria2(source, download_dir):
    # Check if it's a file or a magnet link
    is_magnet = source.startswith("magnet:?")

    if not is_magnet and not os.path.exists(source):
        print(f"\n❌ Torrent file not found: {source}")
        return

    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # Build the aria2c command
    command = [
        r"C:\Users\sansk\Downloads\aria2-1.36.0-win-64bit-build1\aria2c.exe",  # Or just "aria2c" if in PATH
        "--dir=" + os.path.abspath(download_dir),
        "--seed-time=0",
        "--summary-interval=5",
        "--check-integrity=true",
        "--follow-torrent=mem",
        "--enable-dht=true",
        "--bt-save-metadata=true",
        "--bt-tracker-timeout=60",
        source
    ]

    print("\n🚀 Starting download via aria2c...\n")
    try:
        subprocess.run(command, check=True)
        print("\n✅ Download complete!")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Download failed: {e}")

if __name__ == "__main__":
    print("📥 Hybrid Torrent Downloader (Torrent File or Magnet Link)")
    print("==========================================================")

    source = input("🔗 Paste the full path to .torrent file *or* magnet URI: ").strip('" ')
    download_dir = input("📁 Paste the folder path where you want to save the files: ").strip('" ')

    download_with_aria2(source, download_dir)
