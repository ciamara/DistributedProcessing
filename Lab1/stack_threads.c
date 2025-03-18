#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

struct node{
    int number;
    struct node *next;
};