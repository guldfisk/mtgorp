grammar search_grammar;


start : operation EOF;


operation :
    '!' operation #Not
    | '(' operation ')' #Parenthesis
    | restriction #RestrictionOperation
    | operation operation #And
    | operation '&' operation #And
    | operation '||' operation #Or
;

restriction :
    value #NameRestriction
    | NAME_CODE operator value #NameRestriction
    | TYPE_CODE operator value_chain #TypeRestriction
    | MANA_CODE operator value #ManaRestriction
    | COLOR_CODE operator value #ColorRestriction
    | ORACLE_CODE operator value #OracleRestriction
    | POWER_CODE operator value #PowerRestriction
    | TOUGHNESS_CODE operator value #ToughnessRestriction
    | LOYALTY_CODE operator value #LoyaltyRestriction
    | ARTIST_CODE operator value #ArtistRestriction
    | CMC_CODE operator UNSIGNED_INTEGER #CmcRestriction
    | CMC_CODE operator dynamic_value #CmcRestriction
    | RARITY_CODE '=' value #RarityRestriction
    | LAYOUT_CODE '=' value #LayoutRestriction
    | FLAGS_CODE operator value_chain #FlagsRestriction
    | EXPANSION_CODE '=' value #ExpansionRestriction
    | BLOCK_CODE '=' value #BlockRestriction
;

value_chain :
    static_value #ChainValue
    | value_chain value #ChainChain
;

value :
    static_value #StaticValue
    | dynamic_value #DynamicValue
;

static_value :
    VALUE #InferredValue
    | QUOTED_VALUE #QuotedValue
    | UNSIGNED_INTEGER #UnsignedIntegerValue
;

operator :
    ';' #IncludesOperator
    | '=' #EqualsOperator
    | '<' #LessThanOperator
    | '<=' #LessEqualOperator
    | '>' #GreaterThanOperator
    | '>=' #GreaterEqualOperator
;

dynamic_value :
    DYNAMIC_VALUE   #DynamicName
    | DYNAMIC_VALUE NAME_CODE #DynamicName
    | DYNAMIC_VALUE ORACLE_CODE #DynamicOracle
    | DYNAMIC_VALUE POWER_CODE #DynamicPower
    | DYNAMIC_VALUE TOUGHNESS_CODE #DynamicToughness
    | DYNAMIC_VALUE LOYALTY_CODE #DynamicLoyalty
    | DYNAMIC_VALUE ARTIST_CODE #DynamicArtist
    | DYNAMIC_VALUE CMC_CODE #DynamicCmc
;


DYNAMIC_VALUE : '@';

NAME_CODE : [nN]|'name'|'NAME';
TYPE_CODE : [tT]|'type';
MANA_CODE : [mM]|'manacost'|'MANACOST';
COLOR_CODE : 'color'|'COLOR';
ORACLE_CODE : [oO]|'oracle'|'ORACLE';
POWER_CODE : 'power'|'POWER'|'po'|'PO';
TOUGHNESS_CODE : 'toughness'|'TOUGHNESS'|'tough';
LOYALTY_CODE : 'loyalty'|'LOYALTY';
ARTIST_CODE : 'artist'|'ARTIST';
CMC_CODE : 'cmc'|'CMC';
RARITY_CODE : 'rarity'|'RARITY';
LAYOUT_CODE : 'layout'|'LAYOUT';
FLAGS_CODE : 'flags'|'FLAGS';
FLAVOR_CODE : 'flavor'|'FLAVOR';
EXPANSION_CODE : [eE]|'expansion'|'EXPANSION';
BLOCK_CODE : 'block'|'BLOCK';

CARDBOARD_CODE : 'ca'|'CA'|'cardboard'|'CARDBOARD';
PRINTING_CODE : 'pr'|'PR'|'printing'|'PRINTING';

UNSIGNED_INTEGER : [0-9]+;

QUOTED_VALUE : '"'~('"')*'"';
VALUE : [a-zA-Z0-9\-',:{}/*+âáéàíúöû]+;

WHITESPACE : [ \n\t\r] -> skip;
