F77        = gfortran
F90        = gfortran
CC         = gcc
FCCPP      = cpp
FLINKER    = $(F90)
FCCPPFLAGS = -ansi -DLIBXC_VERSION=400
FFLAGS     = -O3 -ffast-math -funroll-loops
CFLAGS     = -O3
LIBS       =  -llapack -lblas
OBJS_LIBXC = exc_libxc_stub.o
