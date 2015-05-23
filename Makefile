TEX_FILES := $(wildcard */*.tex)
DIA_DIAGRAMS := $(wildcard */*.dia)
DIA_IMAGES := $(DIA_DIAGRAMS:.dia=.dia.png)

.PHONY: all clean

all: final.pdf
	@echo > /dev/null

final.pdf: final.tex body.tex $(DIA_IMAGES)
	xelatex $<

body.tex: $(TEX_FILES)
	@echo $^
	cat $^ > $@

%.dia.png: %.dia
	dia -t png -e $@ $<

clean:
	rm -f final.pdf $(DIA_IMAGES) body.tex
