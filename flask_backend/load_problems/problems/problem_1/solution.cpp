#include <iostream>

// Function that calculates and returns the square of a number
double square(double number) {
    return number * number;
}

int main() {
    double num1;
    std::cin >> num1;
    std::cout << square(num1);
    return 0;
}