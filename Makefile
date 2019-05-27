update:
	git pull

run:
	python3 starpars.py

analyze:
	python3 analyze.py

clean:
	rm -f data/corpus.{sentences,tags,words}
