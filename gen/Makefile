GENERICS := $(wildcard *.dia)
SVGS := $(GENERICS:.dia=.dia.svg)

ACTORS := BaseUser Admin User CenterManager
MODELS := Emergency Vehicle User Center Dotation InventoryItem

TARGET_SVGS := $(shell find target -type f -name '*.svg')
TARGET_PNGS := $(TARGET_SVGS:.svg=.svg.png)
TARGET_PNG_WIDTH := 1000

.PHONY: all
all: $(SVGS)
	./generate.py $(ACTORS) -- $(SVGS) -- $(MODELS)
	$(MAKE) target-pngs

target-pngs: $(TARGET_PNGS)
	@echo > /dev/null

.PHONY: clean
clean:
	rm *.dia.svg
	rm -rf target

%.dia.svg: %.dia
	dia -t svg -e $@ $<

%.svg.png: %.svg
	convert -density 1200 -resize $(TARGET_PNG_WIDTH) $< $@
