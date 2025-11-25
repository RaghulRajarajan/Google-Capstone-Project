import sys
import io
import contextlib

class CodeExecutionTool:
    def __init__(self):
        self.output = ""

    def run_code(self, code: str):
        buffer = io.StringIO()
        try:
            with contextlib.redirect_stdout(buffer):
                exec(code, {})
            self.output = buffer.getvalue()
        except Exception as e:
            self.output = f"Error: {str(e)}"
        return self.output


if __name__ == "__main__":
    tool = CodeExecutionTool()
    print("Enter Python code to execute:")
    user_code = sys.stdin.read()
    print(tool.run_code(user_code))
