.PHONY: build deploy images txt feed

images:
	./scripts/makebw.sh

build:
	./venv/bin/python3 -m engine.build

txt:
	./scripts/twtxt.sh

feed:
	./venv/bin/python3 -m engine.twtxt --feed

deploy:
	rsync -avz static/ deploy@radio.af:/srv/www/hecanjog.com
