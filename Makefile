
.PHONY: all

all:
	scripts/generate.sh sample.asc --outdir=outdir

clean:
	rm -rf outdir
