server:
	./bin/python taasks/manage.py runserver

clean:
	for f in `find . -name '*.pyc'`; do rm -f $$f; done
	for f in `find . -name '*.pyo'`; do rm -f $$f; done
