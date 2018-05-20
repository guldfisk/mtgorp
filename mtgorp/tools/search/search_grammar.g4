
grammar search_grammar;


start : operation EOF;

operation :
    restriction #RestrictionOperation
    | '!' operation #Not
    | '(' operation ')' #Paranthesis
    | operation restriction #And
    | operation '&' restriction #And
    | operation '|' operation #Or
;


restriction :
    name_restriction #NameRestriction
    | TYPE_CODE name_value #TypeRestriction
    | MANA_CODE mana_cost #ManaRestriction
    | ORACLE_CODE name_value #OracleRestriction
    | POWER_CODE name_value #PowerRestriction
    | TOUGHNESS_CODE name_value #ToughnessRestriction
    | LOYALTY_CODE name_value #LoyaltyRestriction
    | ARTIST_CODE name_value #ArtistRestriction
    | CMC_CODE name_value #CmcRestriction
    | FLAGS_CODE value_chain #FlagsRestriction
;

name_restriction :
    name_value
    | NAME_CODE name_value
;

value_chain :
    name_value
    | value_chain name_value
;

name_value :
    UNSIGNED_INTEGER
    | NAME_VALUE
    | QUOTED_NAME_VALUE
;



NAME_CODE : [nN]';';
TYPE_CODE : [tT]';';
MANA_CODE : [mM]';';
ORACLE_CODE : [oO]';';
POWER_CODE : [pP]';';
TOUGHNESS_CODE : [tT]';';
LOYALTY_CODE : [lL]';';
ARTIST_CODE : [aA]';';
CMC_CODE : ('cmc'|'CMC'|[cC])';';
FLAGS_CODE : [fF]';';

UNSIGNED_INTEGER: [0-9]+;

QUOTED_NAME_VALUE : '"'~('"')*'"';
NAME_VALUE : [a-zA-Z\-',:][a-zA-Z0-9\-',:]*;

WHITESPACE : [ \n\t\r] -> skip;
