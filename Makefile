linter: githooks
	uv tool run black --line-length 120 *.py
	uv tool run flake8 --config ~/.flake8 *.py
	uv tool run safety check -o bare

githooks:
	git config --local core.hooksPath .githooks
