def _write_file(path: str, content: str, label: str) -> None:
    """
    Writes content to a file in a safe and reusable way, following the
    "Don't Repeat Yourself" (DRY) principle.

    This helper method centralizes file-writing logic to avoid duplicating
    try/except blocks across the codebase. It is intended to be reused for
    writing any document-related output (HTML, CSS, JS, JSON, etc.).

    The method:
    - Opens the file using a context manager to ensure proper resource cleanup.
    - Writes the provided content to disk.
    - Translates low-level I/O errors into a domain-specific runtime error
      with a clear, descriptive message.

    Args:
        path (str):
            Target file path where the content will be written.
        content (str):
            The content to write to the file.
        label (str):
            Human-readable identifier used for error reporting
            (e.g. "HTML", "CSS", "JS").

    Raises:
        RuntimeError:
            If the file cannot be written due to an I/O-related error.
    """
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    except OSError as e:
        raise RuntimeError(f"Failed to write {label} file: {path}") from e
