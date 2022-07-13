from pathlib import Path


def get_path():
    open_path = input('Enter path to file:')
    """File should be in xlsx format"""
    file_to_process = input('Enter filename:')
    full_data_path = Path(open_path).joinpath(file_to_process)
    return full_data_path


if __name__ == "__main__":
    get_path()
