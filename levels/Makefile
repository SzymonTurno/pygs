.PHONY: all clean

PYTHON := py
JAVA := java

all: output

output: ../plantuml.jar level0.puml level1.puml
	$(JAVA) -jar ../plantuml.jar *.puml -tsvg -o "$@"

level0.puml level1.puml:
	$(PYTHON) level1.py

clean:
	rm -f level0.puml level1.puml
	rm -rf output/
