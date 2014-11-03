#include <stdlib.h>
#include <stdio.h>
#ifndef H_SUDOKU
#include "libsudoku.h"
#endif

//Implement the partition function
//Each time choose the pivot as the 
// left most element and partition the 
// array based on this pivot
//  Return the index of Pivot
int Partition(int A[], Cell CA[], int l, int r){
    
    int pivot = A[l], wall = l, pivotN = CA[pivot].N; 
    int temp,i; 
    for (i = l+1; i <= r; ++i)
        if(CA[A[i]].N < pivotN) {
            ++wall; 
            temp = A[i];
            A[i] = A[wall];
            A[wall] = temp;
        }
    temp = A[l];
    A[l] = A[wall];
    A[wall] = temp;
    return wall; 
}


//Write the quicksort recursive calls
//This function performs  the quicksort
void QuickSort(int A[], Cell CA[], int l, int r)
{
    if(l<r) {
        int pivot_pos = Partition(A, CA, l, r);
        QuickSort(A,CA,l,pivot_pos-1); 
        QuickSort(A,CA,pivot_pos+1,r); 
    }
}

//Implement the selection sub routine
//Partition the array into pivots and 
//recurse to one of the subarrays
/*
int selection(int *A, int left, int right, int r)
{
    int piv_pos = Partition(A,left,right);
    if((piv_pos+1) == r) {
	    return A[piv_pos];
    }
    else if((piv_pos+1) > r) {
	    return selection(A, left, piv_pos-1, r);
    }
    else   { //r > piv_pos + 1
	    return selection(A, piv_pos+1,right, r);
    }
}
   
*/
