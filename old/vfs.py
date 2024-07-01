class VirtualFileSystem:
    def __init__(self) -> None:
        self.fs_type = "nestedfs"
        self.fs = ['fd', '', {}]

    def resolve_path(self, path):
        if path == '/':
            return self.fs
        parts = path.strip('/').split('/')
        destination = self.fs
        for part in parts:
            if destination[0] != "fd":
                raise FileNotFoundError(f"{part} is not a directory")
            if part in destination[2]:
                destination = destination[2][part]
            else:
                raise FileNotFoundError(f"No such file or directory: {part}")
        return destination

    def register_file(self, path, contents):
        folder_path, file_name = '/'.join(path.strip('/').split('/')[:-1]), path.strip('/').split('/')[-1]
        folder = self.resolve_path(folder_path)
        if folder[0] != 'fd':
            raise NotADirectoryError(f"{folder_path} is not a directory")
        folder[2][file_name] = ['f', file_name, contents]

    def register_folder(self, path):
        parts = path.strip('/').split('/')
        current_path = ''
        for part in parts:
            current_path = f"{current_path}/{part}".strip('/')
            try:
                self.resolve_path(current_path)
            except FileNotFoundError:
                parent_path, folder_name = '/'.join(current_path.split('/')[:-1]), current_path.split('/')[-1]
                parent_folder = self.resolve_path(parent_path) if parent_path else self.fs
                if parent_folder[0] != 'fd':
                    raise NotADirectoryError(f"{parent_path} is not a directory")
                parent_folder[2][folder_name] = ['fd', folder_name, {}]

    def get_file(self, path):
        file_obj = self.resolve_path(path)
        if file_obj[0] != 'f':
            raise FileNotFoundError(f"{path} is not a file")
        return file_obj

    def get_folder(self, path):
        folder_obj = self.resolve_path(path)
        if folder_obj[0] != 'fd':
            raise NotADirectoryError(f"{path} is not a directory")
        return folder_obj

    def delete_folder(self, path):
        if path == '/':
            raise ValueError("Cannot delete the root directory")
        parts = path.strip('/').split('/')
        parent_path = '/'.join(parts[:-1])
        folder_name = parts[-1]

        parent_folder = self.resolve_path(parent_path) if parent_path else self.fs
        if parent_folder[0] != 'fd':
            raise NotADirectoryError(f"{parent_path} is not a directory")
        if folder_name not in parent_folder[2]:
            raise FileNotFoundError(f"No such directory: {folder_name}")

        folder = parent_folder[2][folder_name]
        if folder[0] != 'fd':
            raise NotADirectoryError(f"{path} is not a directory")

        # Remove the folder from its parent
        del parent_folder[2][folder_name]
        # Custom functionality: logging the deletion of a folder
        #print(f"Deleted folder: {path}")

class CustomFileHandler:
    def __init__(self, vfs, file_path, mode='r'):
        self.vfs = vfs
        self.file_path = file_path
        self.mode = mode
        self._file = None
        self.position = 0

        if 'r' in mode:
            self._file = self.vfs.get_file(file_path)
            self.contents = self._file[2]
        elif 'w' in mode:
            folder_path, file_name = '/'.join(file_path.split('/')[:-1]), file_path.split('/')[-1]
            self.vfs.register_folder(folder_path)
            self.vfs.register_file(file_path, b'')
            self._file = self.vfs.get_file(file_path)
            self.contents = self._file[2]
        else:
            raise ValueError(f"Unsupported mode: {mode}")

        # Custom functionality: logging the opening of a file
        #print(f"Opening file: {file_path} in mode: {mode}")

    def read(self, size=-1):
        if 'r' not in self.mode:
            raise IOError("File not open for reading")
        if size == -1:
            size = len(self.contents) - self.position
        data = self.contents[self.position:self.position + size]
        self.position += size
        # Custom functionality: logging the read operation
        #print(f"Read {len(data)} bytes from file: {self.file_path}")
        return data

    def write(self, data):
        if 'w' not in self.mode:
            raise IOError("File not open for writing")
        if isinstance(data, str):
            data = data.encode('utf-8')
        self.contents = self.contents[:self.position] + data + self.contents[self.position + len(data):]
        self.position += len(data)
        self._file[2] = self.contents
        # Custom functionality: logging the write operation
        #print(f"Wrote {len(data)} bytes to file: {self.file_path}")
        return len(data)

    def seek(self, offset, whence=0):
        if whence == 0:
            self.position = offset
        elif whence == 1:
            self.position += offset
        elif whence == 2:
            self.position = len(self.contents) + offset
        else:
            raise ValueError(f"Invalid value for whence: {whence}")
        # Custom functionality: logging the seek operation
        # print(f"Seek to offset: {self.position}, whence: {whence} in file: {self.file_path}")

    def tell(self):
        # Custom functionality: logging the tell operation
        # print(f"Current file position: {self.position} in file: {self.file_path}")
        return self.position

    def close(self):
        pass
        # Custom functionality: logging the close operation
        # print(f"Closed file: {self.file_path}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        # Custom functionality: logging the context manager exit
        # print(f"Exited context manager for file: {self.file_path}")

# Example usage
vfs = VirtualFileSystem()
vfs.register_folder('/documents/work')
vfs.register_file('/documents/work/example.txt', b'Hello, VFS!')

with CustomFileHandler(vfs, '/documents/work/example.txt', 'r') as f:
    print(f.read())

with CustomFileHandler(vfs, '/documents/work/new_file.txt', 'w') as f:
    f.write("Hello, new file!")

vfs.delete_folder('/documents/work')
with CustomFileHandler(vfs, '/documents/work/example.txt', 'r') as f:
    print(f.read())
