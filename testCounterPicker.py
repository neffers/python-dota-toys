import od_counterpicker
import steamTools
import dotaTools

print od_counterpicker.getGeneralHeroWinrate(dotaTools.parseHeroName(raw_input('what hero: ')),steamTools.getUserInput32withShortcuts())
