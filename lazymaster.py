from os import listdir, path, rename, mkdir
import json

def main():
    home_directory = path.expanduser("~")
    download_directory = path.join(home_directory, "Downloads")
    translation = {}

    # Read json config file and add to translation (extension -> directory)
    with open("config.json") as file:
        config = json.load(file)
        for subdirectory, extensions in config.items():
            for ext in extensions:
                translation[ext] = path.join(download_directory, subdirectory)

    # Build files with absolute path
    files = map(
        lambda file: path.join(download_directory, file),
        listdir(download_directory))

    # Index extensions for comparison
    registered_extensions = tuple(translation.keys())

    # Process collected files
    for file in files:
        # Skip directories
        if path.isdir(file):
            continue

        # Get basename and extension:
        basename = path.basename(file)
        name, ext = path.splitext(basename)

        # Move file
        if basename.endswith(registered_extensions):
            subdirectory = path.join(download_directory, translation[ext])
            if not path.exists(subdirectory):
                mkdir(subdirectory)
            new_file = path.join(subdirectory, basename)
            rename(src=file, dst=new_file)

if __name__ == "__main__":
    main()