#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "element.h"

int main() {

    printf("Inserting elements: 20, 10, 30, 40\n");

    begin = Insert(20, begin);
    begin = Insert(10, begin);
    begin = Insert(30, begin);
    begin = Insert(40, begin);
    Print();
    ReversePrint();

    printf("Removing element: 20\n");
    Remove(20);
    Print();
    ReversePrint();

    printf("Removing element: 40\n");
    Remove(40);
    Print();
    ReversePrint();

    printf("Removing element: 10\n");
    Remove(10);
    Print();
    ReversePrint();

    printf("Removing element: 30\n");
    Remove(30);
    Print();
    ReversePrint();

    FreeList();

    return 0;
}


