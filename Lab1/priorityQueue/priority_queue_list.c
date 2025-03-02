#include <stdio.h>
#include <stdlib.h>
#include "priority_queue_list.h"

void
qlist(pqueue *head, void (*print_data)(void *)) {
	pqueue *p;
	
	for (p = head; p != NULL; p = p->next) {
		printf("%d: ", p->k);
		print_data(p->data);
		printf("\n");
	}
	
}

void
qinsert(pqueue **phead, void *data, int k) {

	//pamiec na nowy proces
    pqueue *new_node = (pqueue *)malloc(sizeof(pqueue));
    new_node->data = data;
    new_node->k = k;
    new_node->next = NULL;
    new_node->prev = NULL;

	//jesli kolejka jest pusta albo nowy proces ma wiekszy priorytet niz glowa
    if (*phead == NULL || (*phead)->k > k) {

        new_node->next = *phead; //next node nowego procesu na glowe
        if (*phead != NULL) {
            (*phead)->prev = new_node; //previous node glowy na nowy proces
        }
        *phead = new_node; //nowy proces staje sie glowa
    } 
	else {
       
		//szukam miejsca gdzie wstawic nowy proces
        pqueue *current = *phead;
        while (current->next != NULL && current->next->k <= k) {
            current = current->next;
        }
		//wstawianie nowego procesu
        new_node->next = current->next;
        new_node->prev = current;
        current->next = new_node;
        if (new_node->next != NULL) {
            new_node->next->prev = new_node;
        }
    }
}


void
qremove(pqueue **phead, int k) {

	if (*phead == NULL) return; // jesli kolejka pusta to nie ma co usunac

    pqueue *current = *phead;

    // sprawdzam czy to glowa musi byc usunieta
    if (current->k == k) {
        *phead = current->next; // przesuniecie glowy na nastepny node
        if (*phead != NULL) {
            (*phead)->prev = NULL; // update poprzednika nowej glowy
        }
        free(current);
        return;
    }

    //szukanie procesu do usuniecia
    while (current != NULL && current->k != k) {
        current = current->next; // przejscie do nastepnego procesu
    }

    //znaleziony proces do usuniecia
    if (current != NULL) {
        //polaczenie poprzednika i nastepnika usuwanego procesu
        if (current->prev != NULL) {
            current->prev->next = current->next;
        }
        if (current->next != NULL) {
            current->next->prev = current->prev;
        }
        free(current);
    }
}

