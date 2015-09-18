BUILD_FILES := final.tex body.tex
# sed is to convert from ./example to example
TEX_FILES := $(filter-out $(BUILD_FILES), $(sort $(shell find . -name '*.tex' | sed 's/^\.\///g')))

DIA_DIAGRAMS := $(shell find . -name '*.dia' | sed 's/^\.\///g')
DIA_IMAGES := $(DIA_DIAGRAMS:.dia=.dia.png)

.PHONY: all
all: final.pdf
	@echo > /dev/null

final.pdf: $(BUILD_FILES) $(DIA_IMAGES) generated-images
	# Two compilations to get the TOC working
	xelatex $<
	xelatex $<
	rm body.tex *.aux *.log *.toc

body.tex: $(TEX_FILES)
	@echo $^
	cat $^ > $@

%.dia.svg: %.dia
	dia -t svg -e $@ $<

%.dia.png: %.dia
	dia -t png -e $@ $<

.PHONY: generated-images
generated-images:
	$(MAKE) -C gen

.PHONY: clean
clean:
	rm -f final.pdf body.tex $(DIA_IMAGES) *.aux *.log *.toc
	cd gen && $(MAKE) clean
