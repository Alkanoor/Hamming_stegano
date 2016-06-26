clean:
	@rm -rf *.pyc
	@for f in "."; \
	do \
		rm -rf $f/*.pyc; \
	done