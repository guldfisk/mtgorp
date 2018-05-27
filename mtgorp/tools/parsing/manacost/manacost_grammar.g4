grammar manacost_grammar;


start :
    EOF #Empty
    | mana_cost EOF #NonEmpty
;

mana_cost :
    mana_cost_atom #Atom
    | mana_cost mana_cost_atom #AtomManaCost
;

mana_cost_atom :
    mana_cost_symbol #Symbol
    | '{' mana_cost_atom '}' #BracedSymbol
    | '{' hybrid '}' #BracedHybrid
;

hybrid :
    mana_cost_atom #HybridAtom
    | mana_cost #HybridManaCost
    | mana_cost_atom '/' hybrid #AtomHybrid
    | mana_cost '/' hybrid #ManaCostHybrid
;

mana_cost_symbol :
    WHITE_SYMBOL #White
    | BLUE_SYMBOL #Blue
    | BLACK_SYMBOL #Black
    | RED_SYMBOL #Red
    | GREEN_SYMBOL #Green
    | PHYREXIAN_SYMBOL #Phyrexian
    | SNOW_SYMBOL #Snow
    | COLORLESS_SYMBOL #Colorless
    | GENERIC_SYMBOL #Generic
    | VARIABLE_SYMBOL #Variable
;


WHITE_SYMBOL : [wW];
BLUE_SYMBOL : [uU];
BLACK_SYMBOL : [bB];
RED_SYMBOL : [rR];
GREEN_SYMBOL : [gG];
PHYREXIAN_SYMBOL : [pP];
SNOW_SYMBOL : [sS];
COLORLESS_SYMBOL : [cC];
GENERIC_SYMBOL : [0-9]+;
VARIABLE_SYMBOL : [xX];