#include <iostream>

extern int reedsolomon();
extern int convcode();
extern int bpsk();

int main(int argc, char **argv)
{

    std::cout << "Hello world!" << std::endl;

    reedsolomon();
    std::cout << "*****************************" <<std::endl;
    convcode();
    std::cout << "*****************************" <<std::endl;
    bpsk();

    return 0;
}