struct element {
	int number ;
	struct element * next ;

};

extern struct element *begin;

struct element * Insert(int obj, struct element *ptr);

void Print();

void ReversePrint();

void Remove(int obj);

void FreeList();
