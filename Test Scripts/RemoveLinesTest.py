def remove_blank_lines(text):
    lines = text.splitlines()
    non_empty_lines = [line for line in lines if line.strip() != ""]
    return '\n'.join(non_empty_lines)

# Example usage
text = """This is a line.

This is another line.


This is yet another line."""

new_text = remove_blank_lines(text)
print(new_text)