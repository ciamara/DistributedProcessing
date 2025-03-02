#include <stdio.h>
#include <stdlib.h>
#include "element.h"

struct element *begin = NULL;

struct element *Insert(int obj, struct element *ptr) {

    struct element *newElement = (struct element *)malloc(sizeof(struct element));
    if (newElement == NULL) {
        printf("Memory allocation failed.\n");
        return ptr;
    }

    newElement->number = obj;
    newElement->next = NULL;

    //list empty
    if (ptr == NULL) {
        return newElement;
    }

    //last node
    struct element *temp = ptr;
    while (temp->next != NULL) {
        temp = temp->next;
    }

    //add to the end
    temp->next = newElement;

    return ptr;
}



void Print() {
    struct element *temp = begin;
    if (temp == NULL) {
        printf("List is empty.\n");
        return;
    }
    printf("List: ");
    while (temp != NULL) {
        printf("%d ", temp->number);
        temp = temp->next;
    }
    printf("\n");
}

void PrintReverseHelper(struct element *node) {
    
    if (node == NULL)
        return;

    PrintReverseHelper(node->next);
    printf("%d ", node->number);
}

void ReversePrint() {

    if (begin == NULL) {
        printf("List is empty.\n");
        return;
    }
    
    printf("Reversed List: ");
    PrintReverseHelper(begin);
    printf("\n");
}


void Remove(int obj) {

    struct element *temp = begin, *prev = NULL;

    //empty?
    if (begin == NULL) {
        printf("List is empty.\n");
        return;
    }

    //first node
    if (begin->number == obj) {
        struct element *toDelete = begin;
        begin = begin->next;
        free(toDelete);
        
        return;
    }

    //searching for node to remove
    while (temp != NULL && temp->number != obj) {
        prev = temp;
        temp = temp->next;
    }

    //not found
    if (temp == NULL) {
        printf("Element not found.\n");
        return;
    }

    //removing last element
    prev->next = temp->next; //unlinking
    free(temp);
}

void FreeList() {

    struct element *temp = begin;

    while (temp != NULL) {

        struct element *next = temp->next;
        free(temp);
        temp = next;
    }
    begin = NULL;
}

