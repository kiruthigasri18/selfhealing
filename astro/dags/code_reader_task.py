import os


def code_reader_task(code_file_path):

    current_dir = os.path.dirname(
        os.path.abspath(__file__)
    )

    file_path = os.path.join(
        current_dir,
        code_file_path
    )

    print("Reading file from:")
    print(file_path)

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"{file_path} does not exist"
        )

    with open(
            file_path,
            "r",
            encoding="utf-8"
    ) as f:

        code = f.read()

    return code