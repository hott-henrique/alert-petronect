import enum


class PetronectScope(str, enum.Enum):
    ALL = ""
    NATIONAL = "N"
    INTERNATIONAL = "I"

    @staticmethod
    def parse(value: str) -> "PetronectScope":
        match (value.upper()):
            case "":
                return PetronectScope.ALL

            case "INTERNACIONAL":
                return PetronectScope.INTERNATIONAL

            case "NACIONAL":
                return PetronectScope.NATIONAL

        raise Exception(f"Unknown PetronectScope: '{value}'")
