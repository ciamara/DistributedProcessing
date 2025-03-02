#include <stdio.h>
#include <stdlib.h>
#include "element.h"

struct element *begin = NULL;

struct element *Insert(int obj, struct element *ptr) {

    struct element *newElement = (struct element *)malloc(sizeof(struct element));
    if (!newElement) {
        printf("Memory allocation failed\n");
        return ptr;
    }

    newElement->number = obj;
    newElement->next = NULL;
    newElement->previous = NULL;

    //jesli lista pusta, nowy element staje sie pierwszym
    if (ptr == NULL) {
        return newElement;
    }

    struct element *current = ptr;
    
    // nowy element na poczatek
    if (obj < current->number) {
        newElement->next = current;
        current->previous = newElement;
        return newElement; //nowa glowa
    }

    // szukanie odpowiedniego miejsca
    while (current->next != NULL && obj > current->next->number) {
        current = current->next;
    }

    // wlozenie nowego elementu
    newElement->next = current->next;
    if (current->next != NULL) {
        current->next->previous = newElement;
    }
    current->next = newElement;
    newElement->previous = current;

    return ptr; //zwrocenie glowy
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


void Remove(int obj) {

    struct element *temp = begin;

    while (temp != NULL) {

        if (temp->number == obj) {

            if (temp->previous) {

                temp->previous->next = temp->next;
            } 
            else{

                begin = temp->next;
            }
            if (temp->next) {

                temp->next->previous = temp->previous;
            }

            free(temp);
            return;
        }

        temp = temp->next;
    }
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

