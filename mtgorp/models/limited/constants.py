from mtgorp.models.limited.boostergen import KeySlot, Option
from mtgorp.models.persistent.attributes import typeline
from mtgorp.models.persistent.attributes.flags import Flag
from mtgorp.models.persistent.attributes.layout import Layout
from mtgorp.models.persistent.attributes.rarities import Rarity
from mtgorp.tools.search.pattern import CriteriaBuilder


COMMON = Option(CriteriaBuilder().rarity.equals(Rarity.COMMON).type_line.contains.no(typeline.BASIC).all())
UNCOMMON = Option(CriteriaBuilder().rarity.equals(Rarity.UNCOMMON).all())
RARE = Option(CriteriaBuilder().rarity.equals(Rarity.RARE).all())
MYTHIC = Option(CriteriaBuilder().rarity.equals(Rarity.MYTHIC).all())
SPECIAL = Option(CriteriaBuilder().rarity.equals(Rarity.SPECIAL).all())
TIMESHIFTED_COMMON = Option(
    CriteriaBuilder().rarity.equals(Rarity.COMMON).flags.contains(Flag.TIMESHIFTED).all(),
)
TIMESHIFTED_UNCOMMON = Option(
    CriteriaBuilder().rarity.equals(Rarity.UNCOMMON).flags.contains(Flag.TIMESHIFTED).all(),
)
TIMESHIFTED_RARE = Option(
    CriteriaBuilder().rarity.equals(Rarity.RARE).flags.contains(Flag.TIMESHIFTED).all(),
)
TIMESHIFTED_MYTHIC = Option(
    CriteriaBuilder().rarity.equals(Rarity.MYTHIC).flags.contains(Flag.TIMESHIFTED).all(),
)
DOUBLEFACED_COMMON = Option(
    CriteriaBuilder().rarity.equals(Rarity.COMMON).layout.equals(Layout.TRANSFORM).all(),
)
DOUBLEFACED_UNCOMMON = Option(
    CriteriaBuilder().rarity.equals(Rarity.UNCOMMON).layout.equals(Layout.TRANSFORM).all(),
)
DOUBLEFACED_RARE = Option(
    CriteriaBuilder().rarity.equals(Rarity.RARE).layout.equals(Layout.TRANSFORM).all(),
)
DOUBLEFACED_MYTHIC = Option(
    CriteriaBuilder().rarity.equals(Rarity.MYTHIC).layout.equals(Layout.TRANSFORM).all(),
)
PREMIUM = Option(
    CriteriaBuilder().all(),
    "premium",
)
BASIC = Option(
    CriteriaBuilder().type_line.contains(typeline.BASIC).all(),
    "basics",
)
DRAFT_MATTERS_COMMON = Option(
    CriteriaBuilder().flags.contains(Flag.DRAFT_MATTERS).rarity.equals(Rarity.COMMON).all(),
)
DRAFT_MATTERS_UNCOMMON = Option(
    CriteriaBuilder().flags.contains(Flag.DRAFT_MATTERS).rarity.equals(Rarity.UNCOMMON).all(),
)
DRAFT_MATTERS_RARE = Option(
    CriteriaBuilder().flags.contains(Flag.DRAFT_MATTERS).rarity.equals(Rarity.RARE).all(),
)
DRAFT_MATTERS_MYTHIC = Option(
    CriteriaBuilder().flags.contains(Flag.DRAFT_MATTERS).rarity.equals(Rarity.MYTHIC).all(),
)

COMMON_SLOT = KeySlot((COMMON,))
UNCOMMON_SLOT = KeySlot((UNCOMMON,))
RARE_SLOT = KeySlot((RARE,))
MYTHIC_SLOT = KeySlot((MYTHIC,))
SPECIAL_SLOT = KeySlot((SPECIAL,))
RARE_MYTHIC_SLOT = KeySlot(
    {
        RARE: 7,
        MYTHIC: 1,
    }
)
PREMIUM_SLOT = KeySlot((PREMIUM,))
BASIC_SLOT = KeySlot((BASIC,))
