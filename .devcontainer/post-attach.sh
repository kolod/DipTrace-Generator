# Install dependencies
poetry install

# Set poetry virtual env as default python interpreter
echo $(cat .vscode/settings.json) {\"python.defaultInterpreterPath\":\"$(poetry env info --executable)\"} | jq -s add > .vscode/settings.json
