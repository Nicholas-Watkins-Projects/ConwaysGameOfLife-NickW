#include <iostream>
#include <list>

using namespace std;

int main() {
    cout << "Hello World";
    return 0;
}

class Universe {
    public:
        int width;
        int height;
        int generations;
        int livingCells = 0;
        list<int[2]> positions;
        Universe(int w = 8, int h = 8, int gens = 0, list<int[2]> pos = {{5,5},{6,6},{7,6},{7,5},{7,4}}){
            width = w;
            height = h;
            generations = gens;
            positions = pos;
        }
};