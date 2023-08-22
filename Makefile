.PHONY: all clean

PYTHON := py
JAVA := java

all: output

output: plantuml.jar stock.puml
	$(JAVA) -jar plantuml.jar stock.puml -tsvg -o "$@"

stock.puml:
	$(PYTHON) example.py > "$@"

clean:
	rm -f stock.puml
	rm -rf output/
