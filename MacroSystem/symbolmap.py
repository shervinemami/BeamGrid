# coding: utf-8
# Dictionary of my non-alphabet letter mappings. Saying the phrase on the left should generate the symbol on the right.
# Use unicode symbols that are a single word (thus can be easy to say, and allows more symbols for mouse grid modes).
# Symbols that are easier to use should be placed near the top of the list, since some screens won't need to show the symbols on the bottom of the list.
# Note that it's still beneficial to put a few easy symbols near the end to line up with the bottom or right edges of your screen, for easy clicking on the taskbar and/or scroll bars.
# Order is preserved, since we use the order as the way to find the index that directly controls the mouse position.
# Just be careful that when you move these symbols up and down, you ensure that the symbolMap number is ordered correctly.
# By Shervin Emami (www.shervinemami.info), 2019.

from collections import OrderedDict     # Allows ordered dictionaries even in Python 2
symbolMap1 = OrderedDict()
symbolMap2 = OrderedDict()
symbolMap3 = OrderedDict()

symbolMap1["flag"] = u"⚑"
symbolMap1["root"] = u"√"
symbolMap1["pi"] = u"π"
symbolMap1["phone"] = u"☎"
symbolMap1["sun"] = u"☼"
symbolMap1["moon"] = u"☽"
symbolMap1["star"] = u"★"
symbolMap1["print"] = u"⎙"       # Not showing up properly in Windows when using DejaVu Sans Mono font!
symbolMap1["pen"] = u"✎"
#symbolMap1["pen"] = u"✑"
symbolMap1["alpha"] = u"α"
symbolMap1["beta"] = u"β"
symbolMap1["gamma"] = u"Ɣ"
symbolMap1["delta"] = u"δ"
symbolMap1["mail"] = u"✉"
symbolMap1["pulse"] = u"⎍"       # Not showing up properly in Windows when using DejaVu Sans Mono font!
symbolMap1["fish"] = u"ᛟ"
symbolMap1["hook"] = u"Ⴑ"
symbolMap1["house"] = u"☖"
symbolMap1["plane"] = u"✈"
symbolMap1["music"] = u"♫"
symbolMap1["note"] = u"♩"
symbolMap1["peace"] = u"☮"
symbolMap1["angle"] = u"⦞"         # Not showing up properly in Windows when using DejaVu Sans Mono font!
symbolMap1["theta"] = u"θ"
symbolMap1["mew"] = u"μ"      # mu is pronounced more like mew
symbolMap1["row"] = u"ρ"      # rho is pronounced more like row
symbolMap1["taow"] = u"τ"      # tau is pronounced more like taow
symbolMap1["psi"] = u"ψ"
symbolMap1["phee"] = u"φ"        # some people refer to φ as "fee" and some as "fi", but "fi" sounds kind of like 5
symbolMap1["half"] = u"½"
symbolMap1["heart"] = u"♥"
symbolMap1["diamond"] = u"♦"
symbolMap1["ground"] = u"⏚"       # Not showing up properly in Windows when using DejaVu Sans Mono font!
symbolMap1["divide"] = u"÷"
symbolMap1["square"] = u"□"
symbolMap1["circle"] = u"○"
symbolMap1["triangle"] = u"△"
symbolMap1["rectangle"] = u"⌷"
symbolMap1["oval"] = u"⬯"          # Not showing up properly in Windows when using DejaVu Sans Mono font!

# Slightly harder symbols pronounce or remember:
symbolMap2["danger"] = u"☠"
symbolMap2["anchor"] = u"⚓"
symbolMap2["quarter"] = u"¼"
symbolMap2["cents"] = u"¢"
symbolMap2["coin"] = u""        # Not showing up properly in Windows when using DejaVu Sans Mono font!
symbolMap2["euros"] = u"€"
symbolMap2["pounds"] = u"£"
symbolMap2["yen"] = u"¥"
symbolMap2["rupees"] = u"₨"
symbolMap2["lira"] = u"₺"
symbolMap2["pesos"] = u"₱"
symbolMap2["degrees"] = u"°"
#symbolMap2["sum"] = u"Ʃ"        # Too similar sounding to "sun"
symbolMap2["infinity"] = u"∞"
symbolMap2["integral"] = u"ʃ"
symbolMap2["disabled"] = u"♿"
symbolMap2["epsilon"] = u"ϵ"
symbolMap2["zeta"] = u"ζ"
#symbolMap2["and"] = u"∧"
#symbolMap2["or"] = u"∨"         # Too similar sounding to "4"?
symbolMap2["clubs"] = u"♣"
symbolMap2["spade"] = u"♠"
symbolMap2["ace"] = u"A"
symbolMap2["joker"] = u"J"
symbolMap2["dashed"] = u"╏"
symbolMap2["dotted"] = u"┋"
symbolMap2["solid"] = u"│"           # "line" is too similar to "nine"
symbolMap2["perpendicular"] = u"⟂"
symbolMap2["squared"] = u"²"
symbolMap2["cubed"] = u"³"
symbolMap2["intersect"] = u"∩"
symbolMap2["union"] = u"∪"
#symbolMap2["chi"] = u"χ"       # Too hard to pronouce for some people?
symbolMap2["umlaut"] = u"ö"
symbolMap2["strike"] = u"Ø"
symbolMap2["begin"] = u"⍃"
symbolMap2["finish"] = u"⍄"
symbolMap2["top"] = u"⍓"
symbolMap2["bottom"] = u"⍌"
symbolMap2["umbrella"] = u"☂"
symbolMap2["cloud"] = u"☁"
symbolMap2["smiley"] = u"☺"
symbolMap2["sad"] = u"☹"
symbolMap2["girl"] = u"♀"
symbolMap2["guy"] = u"♂"
symbolMap2["man"] = u"ᛉ"
symbolMap2["bow"] = u"⦈"
symbolMap2["arrow"] = u"➚"
symbolMap2["target"] = u"⊙"
symbolMap2["hammer"] = u"⚒"
symbolMap2["scissors"] = u"✂"
symbolMap2["swords"] = u"⚔"
symbolMap2["ying"] = u"☯"
symbolMap2["yang"] = u"☯"
symbolMap2["recycle"] = u"♺"
symbolMap2["flower"] = u"❀"
#symbolMap2["pencil"] = u"✎"     # Pencil sounds too much like "cancel"
symbolMap2["dice"] = u"⚁"
symbolMap2["cross"] = u"✝"
symbolMap2["single"] = u"꠳"       # Not showing up properly in Windows when using DejaVu Sans Mono font!
symbolMap2["dual"] = u"꠴"         # Not showing up properly in Windows when using DejaVu Sans Mono font!
symbolMap2["triple"] = u"꠵"       # Not showing up properly in Windows when using DejaVu Sans Mono font!
symbolMap2["king"] = u"♔"
#symbolMap2["queen"] = u"♛"      # Identical to my word for "q"
symbolMap2["rook"] = u"♜"
symbolMap2["bishop"] = u"♗"
symbolMap2["knight"] = u"♘"
symbolMap2["pawn"] = u"♙"
symbolMap2["check"] = u"✔"      # "tick" sounds too much like "click" or "kick"

# Symbols that are mostly less obvious.
symbolMap3["serious"] = u"⁈"
symbolMap3["trademark"] = u"™"
symbolMap3["copyright"] = u"©"
symbolMap3["registered"] = u"®"
symbolMap3["omega"] = u"Ω"
symbolMap3["sigma"] = u"σ"
symbolMap3["thus"] = u"∴"
symbolMap3["identical"] = u"≡"
symbolMap3["proportional"] = u"∝"
symbolMap3["roughly"] = u"≈"
symbolMap3["corner"] = u"⌜"
symbolMap3["eject"] = u"⏏"
symbolMap3["record"] = u"●"
symbolMap3["play"] = u"‣"
symbolMap3["pause"] = u"‖"
symbolMap3["rewind"] = u"◄"
symbolMap3["stop"] = u"▪"
symbolMap3["forward"] = u"►"
symbolMap3["horizontal"] = u"─"
symbolMap3["vertical"] = u"│"
symbolMap3["slanted"] = u"╱"
symbolMap3["subset"] = u"⊂"
symbolMap3["superset"] = u"⊃"
