aname = digitAstar
idaname = digitIDAstar

all: departed initial uos

departed: $(aname)_departed.cpp
	g++ -o $(aname)_departed.out $(aname)_departed.cpp -Wall -O3 -g

initial: $(aname)_initial.cpp
	g++ -o $(aname)_initial.out $(aname)_initial.cpp -Wall -O3 -g
	
uos: $(aname)_unordered_set.cpp
	g++ -o $(aname)_unordered_set.out $(aname)_unordered_set.cpp -Wall -O3 -g

clean:
	rm *.out