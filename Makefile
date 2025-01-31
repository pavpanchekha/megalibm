

# Note: all these files should already be executable
PY_SCRIPTS = src/megalibm_identities.py \
			 src/megalibm_template_identities.py \
			 src/megalibm_generate.py \
			 src/make_website.py

PY_BINS = $(foreach p,${PY_SCRIPTS},$(patsubst src/%.py,bin/%,$p))

# Fill bin
.PHONY: build
build: ${PY_BINS}

# Link python scripts into bin
bin/%: src/%.py requirements/done | bin
	cd bin && $(RM) $* && ln -sF ../src/$*.py $*

# Create bin
bin:
	mkdir bin

# Run nightly
.PHONY: nightly
nightly: bin/nightly.sh
	$<

# Link nightly script into bin
bin/nightly.sh: src/nightly.sh build
	cd bin && $(RM) nightly.sh && ln -sF ../src/nightly.sh nightly.sh

# Build requirements
.PHONY: requirements
requirements: requirements/done

# Run requirements script
requirements/done: requirements/build.sh
	$<

# Normal clean
.PHONY: clean
clean:
	find . -type d -name "__pycache__" -exec ${RM} -r {} +
	$(MAKE) -C measurement clean

# Clean requirements
.PHONY: clean-requirements
clean-requirements: requirements/clean.sh
	$<

# Clean everything
.PHONY: distclean
distclean: clean clean-requirements
	$(RM) -r bin
	$(RM) -r nightlies
	$(MAKE) -C measurement distclean


