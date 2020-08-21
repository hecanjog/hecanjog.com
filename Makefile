.PHONY: build deploy images txt

images:
	./scripts/makebw.sh

build:
	./venv/bin/python3 -m engine.build

txt:
	./scripts/twtxt.sh

deploy:
	rsync -avz static/ deploy@radio.af:/srv/www/hecanjog.com
