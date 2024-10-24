import importlib
import re
from abc import ABC, abstractmethod

import requests


class SubtypeExtractor(ABC):
    @classmethod
    def _split(cls, rule_text: str) -> set[str]:
        return {s.strip() for s in re.sub(r"and |\([^)]+\)", "", rule_text).split(",")}

    @classmethod
    def _to_constant_name(cls, raw_type: str) -> str:
        return re.sub("[^a-zA-Z]", "_", raw_type).upper()

    @abstractmethod
    def get_types(self, rules_text: str) -> set[str]:
        ...

    @abstractmethod
    def format_type(self, raw_type: str) -> str:
        ...

    def get_block(self, rules_text: str) -> str:
        return "\n".join(sorted(self.format_type(_t) for _t in self.get_types(rules_text)))


class ArtifactExtractor(SubtypeExtractor):
    def get_types(self, rules_text: str) -> set[str]:
        return self._split(re.search(r"\n205\.3g.*The artifact types are (.*)\.\n", rules_text).group(1))

    def format_type(self, raw_type: str) -> str:
        return f'{self._to_constant_name(raw_type)} = CardSubType("{raw_type}", (ARTIFACT,))'


class EnchantmentExtractor(SubtypeExtractor):
    def get_types(self, rules_text: str) -> set[str]:
        return self._split(re.search(r"\n205\.3h.*The enchantment types are (.*)\.\n", rules_text).group(1))

    def format_type(self, raw_type: str) -> str:
        return f'{self._to_constant_name(raw_type)} = CardSubType("{raw_type}", (ENCHANTMENT,))'


class LandExtractor(SubtypeExtractor):
    _BASIC_NAMES = {
        "Plains",
        "Island",
        "Swamp",
        "Mountain",
        "Forest",
    }

    def get_types(self, rules_text: str) -> set[str]:
        return self._split(re.search(r"\n205\.3i.*The land types are (.*)\. Of that list.*\.\n", rules_text).group(1))

    def format_type(self, raw_type: str) -> str:
        return f'{self._to_constant_name(raw_type)} = {"BasicLandType" if raw_type in self._BASIC_NAMES else "CardSubType"}("{raw_type}", (LAND,))'  # noqa: E501


class PlaneswalkerExtractor(SubtypeExtractor):
    def get_types(self, rules_text: str) -> set[str]:
        return self._split(re.search(r"\n205\.3j.*The planeswalker types are (.*)\.\n", rules_text).group(1))

    def format_type(self, raw_type: str) -> str:
        return f'{self._to_constant_name(raw_type)} = CardSubType("{raw_type}", (PLANESWALKER,))'


class SpellExtractor(SubtypeExtractor):
    def get_types(self, rules_text: str) -> set[str]:
        return self._split(re.search(r"\n205\.3k.*The spell types are (.*)\.\n", rules_text).group(1))

    def format_type(self, raw_type: str) -> str:
        return f'{self._to_constant_name(raw_type)} = CardSubType("{raw_type}", (INSTANT, SORCERY))'


class CreatureExtractor(SubtypeExtractor):
    def get_types(self, rules_text: str) -> set[str]:
        return self._split(re.search(r"\n205\.3m.*one word long: (.*)\.\n", rules_text).group(1)) | {"Time Lord"}

    def format_type(self, raw_type: str) -> str:
        return f'{self._to_constant_name(raw_type)} = CardSubType("{raw_type}", (CREATURE, TRIBAL))'


class BattleExtractor(SubtypeExtractor):
    def get_types(self, rules_text: str) -> set[str]:
        return {"Siege"}

    def format_type(self, raw_type: str) -> str:
        return f'{self._to_constant_name(raw_type)} = CardSubType("{raw_type}", (BATTLE,))'


def get_blocks(rules_text: str):
    return "\n\n".join(
        e().get_block(rules_text)
        for e in (
            ArtifactExtractor,
            EnchantmentExtractor,
            LandExtractor,
            PlaneswalkerExtractor,
            SpellExtractor,
            CreatureExtractor,
            BattleExtractor,
        )
    )


def update_code(blocks: str):
    m = importlib.import_module("mtgorp.models.persistent.attributes.typeline")
    with open(m.__file__, "r") as f:
        content = f.read()

    with open(m.__file__, "w") as f:
        f.write(
            re.sub(
                "# BEGIN DYNAMICSUBTYPES.*# END DYNAMICSUBTYPES",
                f"# BEGIN DYNAMICSUBTYPES\n\n{blocks}\n\n# END DYNAMICSUBTYPES",
                content,
                flags=re.DOTALL,
            )
        )


def main():
    update_code(
        get_blocks(
            requests.get("https://media.wizards.com/2024/downloads/MagicCompRules20240917.txt")
            .content.decode("utf8")
            .replace("\r\n", "\n")
        )
    )


if __name__ == "__main__":
    main()
