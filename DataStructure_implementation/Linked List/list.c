#include <stdlib.h>
#include <stdio.h>
#include <malloc.h>
#include <stdbool.h>
#include "list.h"

PNode list_create(void)
{
	int length;//length of linked list
	int value;//store the list values
	int i;//counter

	PNode pHead = (PNode)malloc(sizeof(Node));
	if(pHead == NULL){
		printf("Memory allocation failed\n");
		exit(-1);
	}
	
	PNode pTail = pHead; //first pTail is equal to pHead
	pTail->next = NULL;
	printf("Please Enter the number of linked list nodes: Length =");
	scanf("%d",&length);
	for(i=0;i<length;i++){
		printf("Please key in the #%d value",i+1);
		scanf("%d",&value);
		PNode pNew = (PNode)malloc(sizeof(Node));
		if (pNew == NULL){
			printf("Meomry allocation failed\n");
		}
		pNew->data = value;
		pTail->next = pNew;
		pNew->next = NULL;
		pTail = pNew;
	}
	return pHead;
}

int isEmpty(PNode pHead)
{
	if(pHead->next == NULL)
		return 1;
	else
		return 0;
}

void traverseLinklist(PNode pHead)
{
	PNode p = pHead->next;
	while(p != NULL){
		printf("%d  ",p->data);
		p = p->next;
	}
	printf("\n");
}

int getLength(PNode pHead)
{
	int len = 0;
	PNode p = pHead->next;
	while(p != NULL){
		len++;
		p = p->next;
	}
	return len;
}

PNode insert(PNode pHead, int pos, int val)
{
	int i = 0;
	PNode pre = pHead;
	if(pos == 0){
		PNode pNewhead = (PNode)malloc(sizeof(Node));
		if (pNewhead == NULL){
			printf("Memory allocation failed\n");
		}
		PNode fir = pHead->next;
		pNewhead->data = val;
		pNewhead->next = fir;
		pHead->next = pNewhead;
		return pHead;
	}else if (pos == getLength(pHead)+1){
		PNode pNewtail = (PNode)malloc(sizeof(Node));
		if (pNewtail == NULL){
			printf("Memory allocation failed\n");
		}
		pNewtail->data = val;
		int j = 0;
		PNode p = pHead->next;
		for(j = 0;j<getLength(pHead);j++){
			p = p->next;
		}
		p->next = pNewtail;
		pNewtail->next = NULL;
		return pHead;
	}else{
		while(pre!=NULL && i<pos-1){
		pre = pre->next;
		i++;
		}	
		PNode pNew = (PNode)malloc(sizeof(Node));
		if (pNew == NULL){
			printf("Memory allocation failed\n");
		}
		pNew->data = val;
		PNode aft = pre->next;
		pre->next = pNew;
		pNew->next = aft;
		return pHead;
	}
}

PNode remove_node(PNode pHead, int pos)
{
	if(pos==0){
		PNode tmp = pHead->next;
		pHead->next = tmp->next;
		free(tmp);
		return pHead;		
	}else if (pos>0 && pos<getLength(pHead)-1){
		PNode pre = get(pHead, pos-1);
		PNode del = pre->next;
		PNode aft = del->next;
		pre->next = aft;
		free(del);
		return pHead;
	}else if (pos == getLength(pHead)-1){
		PNode pre = get(pHead, pos-1);
		pre->next = NULL;
		return pHead;	
	}else{
		printf("please enter a valid pos\n");
	}
}

PNode get(PNode pHead,int pos)
{
	
	PNode p = pHead->next;
	while(pos>0){
		p = p->next;
		pos--;
	}
	return p;
}

int search(PNode pHead, int val)
{
	PNode p = pHead->next;
	int length = getLength(pHead);
	int i = 0;
	while (i<length){
		if (p->data == val)
			return i;
		p = p->next;
		i++;
        }
	return -1;
}
int main()
{
	int leng;
	PNode pHead = NULL;
	pHead = list_create();
        traverseLinklist(pHead);
	leng = getLength(pHead);
	printf("The length of the linked list is %d\n",leng);
	pHead = insert(pHead,3,6);
        traverseLinklist(pHead);
	pHead = insert(pHead,6,5);
        traverseLinklist(pHead);
	leng = getLength(pHead);
	printf("The length of the linked list is %d\n",leng);
	printf("add 0 to position 0\n");
	pHead = insert(pHead,0,119);
	leng = getLength(pHead);
	printf("out of the function\n");
        traverseLinklist(pHead);
	printf("The length of the linked list is %d\n",leng);
	int find = search(pHead, 4);
	printf("value 4's position is %d\n",find);
	PNode tmpv = get(pHead, 3);
	int valueofnode3 = tmpv->data;
	printf("The value of node3 is %d\n",valueofnode3);
	pHead = remove_node(pHead, 3);
	printf("After delete the node3\n");
	traverseLinklist(pHead);
	pHead = remove_node(pHead, 0);
	printf("After delete the node0\n");
	traverseLinklist(pHead);
	pHead = remove_node(pHead, 5);
	printf("After delete the node5\n");
	traverseLinklist(pHead);
	return 1;
}
