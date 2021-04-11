.PHONY: blog pages listening deploy images

images:
	./scripts/makebw.sh

pages:
	./venv/bin/python3 -m engine.build pages

blog:
	./venv/bin/python3 -m engine.build blog

listening:
	./venv/bin/python3 -m engine.build listening

releases:
	./venv/bin/python3 -m engine.build releases

research:
	./venv/bin/python3 -m engine.build research

all: images pages blog listening releases research

deploy:
	rsync -avz static/ deploy@radio.af:/srv/www/hecanjog.com
