#ifndef _LIST_H
#define _LIST_H

typedef struct _Node{
	int data;
	struct _Node *next;
}Node, *PNode;
PNode list_creat(void);
int isEmpty(PNode pHead);
void traverseLinklist(PNode pHead);
int getLength(PNode pHead);
PNode intsert(PNode pHead, int pos, int val);
PNode remove_node(PNode pHead, int pos);
PNode get(PNode pHead, int pos);
int search(PNode pHead, int val);

#endif
