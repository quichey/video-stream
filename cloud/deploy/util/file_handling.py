def update_file(file_path, line_to_replace, new_string):
    with open(file_path, "r") as f:
        lines = f.readlines()

    with open(file_path, "w") as f:
        for line in lines:
            if line.startswith(line_to_replace):
                f.write(new_string)
            else:
                f.write(line)
