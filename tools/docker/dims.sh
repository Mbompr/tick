#/bin/sh

for PYBIN in "3.3.6" "3.4.5" "3.5.2"; do
	pyenv local $PYBIN
	python -c "print(\"Hello, world\")"
done