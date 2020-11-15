.PHONY: blog pages listening deploy images gemini

images:
	./scripts/makebw.sh

pages:
	./venv/bin/python3 -m engine.build pages

blog:
	./venv/bin/python3 -m engine.build blog

listening:
	./venv/bin/python3 -m engine.build listening

gemini:
	./scripts/makegemini.sh

all: images pages blog listening gemini

deploy:
	rsync -avz static/ deploy@radio.af:/srv/www/hecanjog.com
