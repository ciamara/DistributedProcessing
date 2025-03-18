#include <stddef.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>

#define ll_contetnt_t int

#define LL_ALLOC_ERROR  1
#define LL_INVALID_HEAD 2
#define LL_INVALID      INT_MAX

typedef struct ll_node_t {
	struct ll_node_t *next;
	ll_contetnt_t content;
} ll_node_t;

ll_node_t *ll_init(void)
{
	ll_node_t *head = malloc(sizeof(ll_node_t));

	if (!head) {
		return NULL;
	}

	head->next = NULL;
	return head;
}

ll_contetnt_t ll_at(ll_node_t *head, size_t index)
{
	if (head == NULL || head->next == NULL) {
		return LL_INVALID;
	}

	head = head->next;
	size_t current_index = 0;

	while (head->next != NULL && current_index < index) {
		head = head->next;
		current_index++;
	}

	return head->content;
}


void ll_free(ll_node_t *head)
{
	if (head == NULL) {
		return;
	}

	ll_node_t *prev = head;
	ll_node_t *current = head->next;

	while (current != NULL) {
		free(prev);
		prev = current;
		current = current->next;
	}

	free(prev);
}

void ll_print(ll_node_t *head)
{
	if (head == NULL) {
		return;
	}

	head = head->next;

	while (head != NULL) {
		printf("%d -> ", head->content);
		head = head->next;
	}

	printf("NULL\n");
}

size_t ll_length(ll_node_t *head)
{
	size_t len = 0;
	while (head->next != NULL)
	{
		len++;
		head = head->next;
	}

	return len;
}

int ll_add_at(ll_node_t *head, size_t index, ll_contetnt_t content)
{
	if (head == NULL) {
		return LL_INVALID_HEAD;
	}

	size_t current_index = 0;

	while (head->next != NULL && current_index < index) {
		head = head->next;
		current_index++;
	}
	
	ll_node_t *prev = head;
	head = head->next;
	
	prev->next = malloc(sizeof(ll_node_t));
	if (!prev->next) {
		return LL_ALLOC_ERROR;
	}

	prev->next->next = head;
	prev->next->content = content;

	return 0;
}

int ll_remove_at(ll_node_t *head, size_t index)
{
	size_t current_index = 0;
	if (head == NULL) {
		return LL_INVALID;
	}

	if (ll_length(head) == 0) {
		return 0;
	}
	
	while (head->next != NULL && current_index < index) {
		head = head->next;
		current_index++;
	}

	ll_node_t *prev = head;
	head = head->next;

	ll_node_t *tmp = head == NULL ? NULL : head->next;

	free(head);

	prev->next = tmp;
	return 0;
}

int empty(ll_node_t *stack)
{
	return ll_length(stack) == 0;
}

void push(ll_node_t *stack, ll_contetnt_t val)
{
	ll_add_at(stack, 0, val);
}

ll_contetnt_t pop(ll_node_t *stack)
{
	if (empty(stack)) {
		return LL_INVALID;
	}

	ll_contetnt_t tmp = ll_at(stack, 0);
	ll_remove_at(stack, 0);
	return tmp;
}

ll_node_t *stack;

#define PUSH_COUNT 10000

sem_t sem_even;
sem_t sem_odd;

void *push_even(void * args)
{

	for (int i = 0; i < PUSH_COUNT; i++) {
		sem_wait(&sem_even);
		printf("EVEN: %d\n", i*2);
		push(stack, i*2);
		sem_post(&sem_odd);
	}


	return NULL;
}

void *push_odd(void * args)
{

	for (int i = 0; i < PUSH_COUNT; i++) {
		sem_wait(&sem_odd);
		printf("ODD: %d\n", i*2 + 1);
		push(stack, i*2 + 1);
		sem_post(&sem_even);
	}


	return NULL;
}

int main(void)
{
	stack = ll_init();

	if (sem_init(&sem_even, 0, 1) != 0) {
		fprintf(stderr, "sem_init() falied at %s %d\n", __FILE__, __LINE__);
		return 1;
	}

	if (sem_init(&sem_odd, 0, 0) != 0) {
		fprintf(stderr, "sem_init() falied at %s %d\n", __FILE__, __LINE__);
		return 1;
	}
	
	pthread_t even, odd;

	pthread_create(&odd, NULL, push_odd, NULL);
	pthread_create(&even, NULL, push_even, NULL);

	pthread_join(even, NULL);
	pthread_join(odd, NULL);
	
	printf("len %lu\n", ll_length(stack));

	sem_destroy(&sem_even);
	sem_destroy(&sem_odd);
	ll_free(stack);
	
	return 0;
}
