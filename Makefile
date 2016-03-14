
default: all


INPUT_FILES=$(wildcard input/*)
TARGET_FILES=$(addsuffix .csv,$(subst input,output,$(INPUT_FILES)))

output/%.csv: input/%
	python import_scoreboard.py $< $@

all: output $(TARGET_FILES)

output:
	mkdir output

clean:
	rm -rf output
