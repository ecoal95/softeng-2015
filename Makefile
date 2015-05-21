CLASSES := $(wildcard classes/*.tex)
USE_CASES := $(wildcard use-cases/*.tex)
TEX_FILES := class-diagram.tex $(CLASSES) use-cases.tex $(USE_CASES)
PANDOC_FLAGS := $(PANDOC_FLAGS) --latex-engine xelatex --template template.tex -V geometry:margin=1in  -V toc-depth=3
PANDOC_FLAGS := $(PANDOC_FLAGS) -V title="Example title blah blah and a bit of bleh too because if not..." -V subtitle="Test subtitle lorem ipsum blah blah blah" -V version="0.1.0"
PANDOC_FLAGS := $(PANDOC_FLAGS) -V author="Emilio Cobos Álvarez" -V author="Celia Herrera Ferreira" -V author="Víctor Barrueco Gutiérrez" -V date="Tuesday..."


.PHONY: all clean

all: final.pdf
	@echo > /dev/null

final.pdf: template.tex $(TEX_FILES)
	pandoc $(PANDOC_FLAGS) --toc -N -o $@ $(TEX_FILES)

class-diagram.tex: class-diagram.dia.png
	touch $@

use-cases.tex: use-cases.dia.png
	touch $@

%.dia.png: %.dia
	dia -t png -e $@ $<

clean:
	rm final.pdf *.dia.png
