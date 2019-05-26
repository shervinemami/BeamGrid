# coding: utf-8
# Dictionary of my non-alphabet letter mappings. Saying the phrase on the left should generate the symbol on the right.
# Use unicode symbols that are a single word (thus can be easy to say, and allows more symbols for mouse grid modes).
# Symbols that are easier to use should be placed near the top of the list, since some screens won't need to show the symbols on the bottom of the list.
# Note that it's still beneficial to put a few easy symbols near the end to line up with the bottom or right edges of your screen, for easy clicking on the taskbar and/or scroll bars.
# Order is preserved, since we use the order as the way to find the index that directly controls the mouse position.
# By Shervin Emami (www.shervinemami.info), 2019.

from collections import OrderedDict     # Allows ordered dictionaries even in Python 2
symbolMap1 = OrderedDict()
symbolMap2 = OrderedDict()

symbolMap1["music"] = u"♫"
symbolMap1["note"] = u"♩"
symbolMap1["flag"] = u"⚑"
symbolMap1["triangle"] = u"△"
symbolMap1["square"] = u"□"
symbolMap1["rectangle"] = u"⌷"
symbolMap1["circle"] = u"○"
symbolMap1["oval"] = u"⬯"          # Not showing up properly in Windows when using DejaVu Sans Mono font!
symbolMap1["anchor"] = u"⚓"
symbolMap1["disabled"] = u"♿"
symbolMap1["heart"] = u"♥"
symbolMap1["clubs"] = u"♣"
symbolMap1["spade"] = u"♠"
symbolMap1["diamond"] = u"♦"
symbolMap1["joker"] = u"J"
symbolMap1["dashed"] = u"╏"
symbolMap1["dotted"] = u"┋"
symbolMap1["solid"] = u"│"           # "line" is too similar to "nine"
symbolMap1["cents"] = u"¢"
symbolMap1["coin"] = u""        # Not showing up properly in Windows when using DejaVu Sans Mono font!
symbolMap1["euros"] = u"€"
symbolMap1["pounds"] = u"£"
symbolMap1["yen"] = u"¥"
symbolMap1["rupees"] = u"₨"
symbolMap1["lira"] = u"₺"
symbolMap1["pesos"] = u"₱"
symbolMap1["degrees"] = u"°"
symbolMap1["angle"] = u"⦞"         # Not showing up properly in Windows when using DejaVu Sans Mono font!
symbolMap1["perpendicular"] = u"⟂"
symbolMap1["divide"] = u"÷"
symbolMap1["half"] = u"½"
symbolMap1["quarter"] = u"¼"
symbolMap1["squared"] = u"²"
symbolMap1["cubed"] = u"³"
symbolMap1["root"] = u"√"
symbolMap1["pi"] = u"π"
symbolMap1["infinity"] = u"∞"
#symbolMap1["sum"] = u"Ʃ"        # Too similar sounding to "sun"
symbolMap1["integral"] = u"ʃ"
symbolMap1["intersect"] = u"∩"
symbolMap1["union"] = u"∪"
symbolMap1["and"] = u"∧"
symbolMap1["or"] = u"∨"
symbolMap1["alpha"] = u"α"
symbolMap1["beta"] = u"β"
symbolMap1["gamma"] = u"Ɣ"
symbolMap1["delta"] = u"δ"
symbolMap1["epsilon"] = u"ϵ"
symbolMap1["zeta"] = u"ζ"
symbolMap1["lambda"] = u"λ"
symbolMap1["psi"] = u"ψ"
symbolMap1["phi"] = u"φ"
#symbolMap1["chi"] = u"χ"       # Too hard to pronouce for some people?
symbolMap1["umlaut"] = u"ö"
symbolMap1["strike"] = u"Ø"
symbolMap1["start"] = u"⍃"
symbolMap1["finish"] = u"⍄"
symbolMap1["top"] = u"⍓"
symbolMap1["bottom"] = u"⍌"
symbolMap1["sun"] = u"☼"
symbolMap1["moon"] = u"☽"
symbolMap1["star"] = u"★"
symbolMap1["cloud"] = u"☁"
symbolMap1["umbrella"] = u"☂"
symbolMap1["smiley"] = u"☺"
symbolMap1["sad"] = u"☹"
symbolMap1["girl"] = u"♀"
symbolMap1["guy"] = u"♂"
symbolMap1["man"] = u"ᛉ"
symbolMap1["fish"] = u"ᛟ"
symbolMap1["hook"] = u"Ⴑ"
symbolMap1["bow"] = u"⦈"
symbolMap1["arrow"] = u"➚"
symbolMap1["target"] = u"⊙"
symbolMap1["hammer"] = u"⚒"
symbolMap1["scissors"] = u"✂"
symbolMap1["swords"] = u"⚔"
symbolMap1["house"] = u"☖"
symbolMap1["plane"] = u"✈"
symbolMap1["phone"] = u"☎"
symbolMap1["mail"] = u"✉"
symbolMap1["ying"] = u"☯"
symbolMap1["yang"] = u"☯"
symbolMap1["peace"] = u"☮"
symbolMap1["recycle"] = u"♺"
symbolMap1["flower"] = u"❀"
#symbolMap1["pencil"] = u"✎"     # Pencil sounds too much like "cancel"
symbolMap1["pen"] = u"✎"
#symbolMap1["pen"] = u"✑"
symbolMap1["dice"] = u"⚁"
symbolMap1["cross"] = u"✝"
symbolMap1["single"] = u"꠳"       # Not showing up properly in Windows when using DejaVu Sans Mono font!
symbolMap1["dual"] = u"꠴"         # Not showing up properly in Windows when using DejaVu Sans Mono font!
symbolMap1["triple"] = u"꠵"       # Not showing up properly in Windows when using DejaVu Sans Mono font!
symbolMap1["king"] = u"♔"
#symbolMap1["queen"] = u"♛"      # Identical to my word for "q"
symbolMap1["rook"] = u"♜"
symbolMap1["bishop"] = u"♗"
symbolMap1["knight"] = u"♘"
symbolMap1["pawn"] = u"♙"
symbolMap1["check"] = u"✔"      # "tick" sounds too much like "click" or "kick"
symbolMap1["ground"] = u"⏚"       # Not showing up properly in Windows when using DejaVu Sans Mono font!
symbolMap1["danger"] = u"☠"

# Symbols that are mostly less obvious.
symbolMap2["serious"] = u"⁈"
symbolMap2["trademark"] = u"™"
symbolMap2["copyright"] = u"©"
symbolMap2["registered"] = u"®"
symbolMap2["omega"] = u"Ω"
symbolMap2["theta"] = u"θ"
symbolMap2["mew"] = u"μ"      # mu is pronounced more like mew
symbolMap2["row"] = u"ρ"      # rho is pronounced more like row
symbolMap2["sigma"] = u"σ"
symbolMap2["taow"] = u"τ"      # tau is pronounced more like taow
symbolMap2["thus"] = u"∴"
symbolMap2["identical"] = u"≡"
symbolMap2["proportional"] = u"∝"
symbolMap2["roughly"] = u"≈"
symbolMap2["corner"] = u"⌜"
symbolMap2["pulse"] = u"⎍"       # Not showing up properly in Windows when using DejaVu Sans Mono font!
symbolMap2["eject"] = u"⏏"
symbolMap2["record"] = u"●"
symbolMap2["play"] = u"‣"
symbolMap2["pause"] = u"‖"
symbolMap2["rewind"] = u"◄"
symbolMap2["stop"] = u"▪"
symbolMap2["forward"] = u"►"
symbolMap2["print"] = u"⎙"       # Not showing up properly in Windows when using DejaVu Sans Mono font!
symbolMap2["horizontal"] = u"─"
symbolMap2["vertical"] = u"│"
symbolMap2["slanted"] = u"╱"
symbolMap2["subset"] = u"⊂"
symbolMap2["superset"] = u"⊃"