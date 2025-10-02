from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    YamlConfigSettingsSource,
)
from pydantic import Field
from pathlib import Path
from typing import List


class GlobalSettings(BaseSettings):
    media_dir_path: Path = Field(default_factory=lambda: Path("/data"))
    allow_midia_suffixs: List[str] = Field(default_factory=lambda: ["m3u8", "mp4"])
    midia_name_block_strs: List[str] = Field(default_factory=list)

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            YamlConfigSettingsSource(
                settings_cls,
                yaml_file=Path("config.local.yaml"),
                yaml_file_encoding="utf-8",
            ),
        )
