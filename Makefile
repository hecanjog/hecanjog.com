.PHONY: build deploy images

images:
	./scripts/makebw.sh

build:
	./venv/bin/python3 -m engine.build

deploy:
	rsync -avz static/ deploy@radio.af:/srv/www/hecanjog.com
