# coding: utf-8
# Dictionary of my non-alphabet keyboard mappings, ie: for punctuation and similar letters that exist on the keyboard but aren't in the English alphabet.
# Saying the phrase on the left should generate the symbol on the right.
# Symbols that are easier to say should be placed in the top of the list, since some screens won't need to show the symbols on the bottom of the list.
# Order is preserved, since we use the order as the way to find the index that directly controls the mouse position.

from collections import OrderedDict     # Allows ordered dictionaries even in Python 2
punctuationMap1 = OrderedDict()
punctuationMap2 = OrderedDict()

# Keyboard characters that aren't numbers or letters
punctuationMap1["backtick"] = u"`"
punctuationMap1["tilda"] = u"~"
punctuationMap1["quotes"] = u'"'
punctuationMap1["exclamation"] = u"!"
punctuationMap1["at"] = u"@"
punctuationMap1["hash"] = u"#"
punctuationMap1["dollar"] = u"$"
punctuationMap1["percent"] = u"%"
punctuationMap1["caret"] = u"^"
punctuationMap1["ampersand"] = u"&"
punctuationMap1["asterisk"] = u"*"
punctuationMap1["plus"] = u"+"
punctuationMap1["minus"] = u"-"
punctuationMap1["equals"] = u"="
punctuationMap1["underscore"] = u"_"
punctuationMap1["semicolon"] = u";"
punctuationMap1["colon"] = u":"
punctuationMap1["slash"] = u"/"
punctuationMap1["backslash"] = u"\\"
punctuationMap1["pipe"] = u"|"
punctuationMap1["comma"] = u","
punctuationMap1["dot"] = u"."
punctuationMap1["question"] = u"?"

# These are part of normal keyboard characters, but since they are harder to say than most symbols, they are being added late so that they're less likely to be used (eg: Y axis on small screens probably won't use symbols this far down)
#punctuationMap2["("] = u"("
#punctuationMap2[")"] = u")"
#punctuationMap2["["] = u"["
#punctuationMap2["]"] = u"]"
#punctuationMap2["{"] = u"{"
#punctuationMap2["}"] = u"}"
#punctuationMap2["<"] = u"<"
#punctuationMap2[">"] = u">"
punctuationMap2["round bracket"] = u"("
punctuationMap2["close round"] = u")"
punctuationMap2["square bracket"] = u"["
punctuationMap2["close square"] = u"]"
punctuationMap2["curly brace"] = u"{"
punctuationMap2["close curly"] = u"}"
punctuationMap2["less than"] = u"<"
punctuationMap2["greater than"] = u">"
