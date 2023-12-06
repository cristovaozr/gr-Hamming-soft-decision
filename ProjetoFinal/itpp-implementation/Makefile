CCX := g++

CXXFLAGS += -O0 -ggdb -DNDEBUG
LIBS += -litpp
INCLUDEDIR += 

SRC += main.cpp \
	simulation.cpp \
	bpsk-simulation.cpp \
	rs-simulation.cpp \
	cc-simulation.cpp \
	conc-simulation.cpp

OBJ := $(SRC:.cpp=.o)

all: $(OBJ)
	$(CXX) $(OBJ) $(LIBS) $(CFLAGS) -o main

clean:
	$(RM) $(OBJ) main