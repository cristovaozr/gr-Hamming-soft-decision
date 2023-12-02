CCX := g++

CXXFLAGS += -O0 -ggdb -DNDEBUG
LIBS += -litpp
INCLUDEDIR += 

SRC += main.cpp rs.cpp convcode.cpp bpsk.cpp

OBJ := $(SRC:.cpp=.o)

all: $(OBJ)
	$(CXX) $(OBJ) $(LIBS) $(CFLAGS) -o main

clean:
	$(RM) $(OBJ) main