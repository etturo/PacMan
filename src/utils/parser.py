from pathlib import Path
import json
import re

from pydantic import ValidationError

from src.utils.models import BaseSettings, ParsingError


class SettingParser:
    def __init__(self) -> None:
        self.__parsed_settings: BaseSettings | None = None

    @staticmethod
    def _clean_text(text: str) -> str:
        pattern = re.compile(
            r'("(?:\\.|[^"\\])*")|(/\*.*?\*/|//[^\n]*|#[^\n]*)',
            re.DOTALL,
        )
        return pattern.sub(lambda m: m.group(1) if m.group(1) else "", text)

    def parse(self, file_path: str) -> BaseSettings:
        path = Path(file_path)

        try:
            raw_text: str = path.read_text(encoding="utf-8")
        except OSError as exc:
            raise ParsingError(
                f"Could not read config file '{path}'.") from exc

        clean_text = self._clean_text(raw_text)
        try:
            parsed_dict = json.loads(clean_text)
        except json.JSONDecodeError as exc:
            raise ParsingError(
                f"Failed to load JSON file '{path}': {exc.msg} "
                f"(line {exc.lineno}, column {exc.colno})."
            ) from exc

        try:
            results = BaseSettings(**parsed_dict)
        except ValidationError as exc:
            error_messages = []

            for error in exc.errors():
                location = " -> ".join(str(loc) for loc in error["loc"])
                message = error["msg"]
                error_messages.append(f"Field '{location}': {message}")

            clean_error = "\n".join(error_messages)
            raise ParsingError(
                f"Failed to load configuration:\n{clean_error}") from exc

        self.__parsed_settings = results
        return results
