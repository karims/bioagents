from pathlib import Path

from bioagents.datasources.base import DataSource


class FileDataSource(DataSource):
    def load(self, config: dict) -> str:
        path = Path(config["path"])

        if path.suffix.lower() == ".txt":
            return path.read_text(encoding="utf-8")

        if path.suffix.lower() == ".pdf":
            try:
                import PyPDF2

                text = ""
                with path.open("rb") as handle:
                    reader = PyPDF2.PdfReader(handle)
                    for page in reader.pages:
                        text += page.extract_text() or ""
                return text
            except Exception:
                return ""

        raise ValueError(f"Unsupported file type: {path.suffix}")
