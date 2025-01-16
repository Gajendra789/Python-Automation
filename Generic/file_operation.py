import os
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import Optional


# Function to read a file with better error handling and support for both text and binary formats
def read_file(file_path: str, mode: str = 'r', encoding: Optional[str] = None) -> Optional[str]:
    try:
        with open(file_path, mode, encoding=encoding) as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    except PermissionError:
        print(f"Error: Permission denied when trying to read '{file_path}'.")
    except IOError as e:
        print(f"Error reading the file '{file_path}': {e}")
    return None


# Function to write to a file with better error handling and flexible encoding
def write_to_file(file_path: str, content: str, mode: str = 'w', encoding: Optional[str] = 'utf-8') -> None:
    try:
        with open(file_path, mode, encoding=encoding) as file:
            file.write(content)
            # Optionally, seek and check pointer position after write
            file.seek(10)
            position = file.tell()
            print(f"Current position in file: {position}")
        print(f"Content successfully written to '{file_path}' in '{mode}' mode.")
    except PermissionError:
        print(f"Error: Permission denied when trying to write to '{file_path}'.")
    except IOError as e:
        print(f"Error writing to the file '{file_path}': {e}")


# Function to process content with flexible transformations
def process_content(content: str, transformation: str = 'uppercase') -> str:
    transformations = {
        'uppercase': content.upper(),
        'lowercase': content.lower(),
        'capitalize': content.capitalize(),
        'titlecase': content.title()
    }
    return transformations.get(transformation, content)


# Function to process a file with options to handle large files more efficiently (line by line or in chunks)
def process_files(input_file: str, output_file: str, transformation: str = 'uppercase', append: bool = False,
                  chunk_size: Optional[int] = 1024) -> None:
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            content = ""
            if chunk_size:
                while chunk := file.read(chunk_size):
                    content += process_content(chunk, transformation)
            else:
                content = process_content(file.read(), transformation)

        mode = 'a' if append else 'w'
        write_to_file(output_file, content, mode)
    except Exception as e:
        print(f"Error processing file: {e}")


# Function to process multiple files concurrently using ThreadPoolExecutor or ProcessPoolExecutor
def process_multiple_files(files: list, transformation: str = 'uppercase', append: bool = False,
                           executor_type: str = 'thread', chunk_size: Optional[int] = 1024) -> None:
    # Choose executor type based on whether we want to process concurrently with threads or processes
    executor_class = ThreadPoolExecutor if executor_type == 'thread' else ProcessPoolExecutor
    
    with executor_class() as executor:
        futures = []
        for input_file in files:
            output_file = f"output_{os.path.basename(input_file)}"  # Dynamic output file name
            futures.append(executor.submit(process_files, input_file, output_file, transformation, append, chunk_size))

        # Wait for all futures to complete
        for future in futures:
            future.result()  # Get result (or exception if any)

# Example usage
if __name__ == '__main__':
    input_file = 'input.txt'  # Modify to actual file path
    output_file = 'output.txt'  # Modify to actual output file path

    # Single file processing
    process_files(input_file, output_file, transformation='uppercase', append=False)

    # Example with multiple files
    files_to_process = ['file1.txt', 'file2.txt', 'file3.txt']  # List of input files
    process_multiple_files(files_to_process, transformation='lowercase', append=True, executor_type='thread')
