from src.utils.models import BaseSettings
from pathlib import Path
import re
import json

class SettingParser:
    def __init__(self) -> None:
        self.__parsed_settings: BaseSettings

    @staticmethod
    def _clean_text(text: str) -> str:
        pattern = re.compile(
            r'("(?:\\.|[^"\\])*")|(/\*.*?\*/|//[^\n]*|#[^\n]*)',
            re.DOTALL
        )
        return pattern.sub(lambda m: m.group(1) if m.group(1) else "", text)

    def parse(self, file_path: str) -> BaseSettings:
        path = Path(file_path)

        raw_tex: str = path.read_text(encoding="utf-8")
        clean_text = self._clean_text(raw_tex)
        parsed_dict = json.loads(clean_text)

        return BaseSettings(**parsed_dict)
