#This file is part of SuperNu.  SuperNu is released under the terms of the GNU GPLv3, see COPYING.
#Copyright (c) 2013-2019 Ryan T. Wollaeger and Daniel R. van Rossum.  All rights reserved.
TOP := $(CURDIR)/..

include $(TOP)/Makefile.compiler
include $(TOP)/Makefile.include

LIBRARY = source.a
FILES := sourceenergy.o sourceenergy_analytic.o sourceenergy_misc.o \
  sourcenumbers.o vacancies.o \
  boundary_source.o interior_source.o initialnumbers.o initial_particles.o \
  source_transformdirection.o analytic_initial.o

.PHONY: all clean

all: $(LIBRARY)
Makefile.depend:
	$(TOP)/depend.sh $(FILES) >Makefile.depend
clean:
	rm -f *.o *.mod *.MOD Makefile.depend $(LIBRARY)

$(LIBRARY): $(FILES)

include Makefile.depend
