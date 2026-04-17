def check_for_errors(file_path):
    try:
        with open(file_path, 'r') as f:
            source = f.read()
        compile(source, file_path, 'exec')
        print(f"No syntax errors in {file_path}.")
    except SyntaxError as e:
        print(f"Syntax error in {file_path}: {e}")
    except Exception as e:
        print(f"Error checking {file_path}: {e}")

if __name__ == "__main__":
    check_for_errors('main.py')