CLASSES := $(wildcard classes/*.md)
USE_CASES := $(wildcard use-cases/*.md)

all: final.pdf
	@echo > /dev/null

final.pdf: class-diagram.md $(CLASSES) use-cases.md $(USE_CASES)
	pandoc $(PANDOC_FLAGS) --toc -N --from=markdown_github -o $@ $^

class-diagram.md: class-diagram.dia.png
	touch $@

use-cases.md: use-cases.dia.png
	touch $@

%.dia.png: %.dia
	dia -t png -e $@ $<
