#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "libsudoku.h"

void printArray(int A[], int N)
{
    int i=0;
    for(i=0; i<N; ++i){
        printf("%d ", A[i]);
    }
    printf("\n");
}

void printCA(Cell CA[])
{
    int i,j;
    printf("i\tR\tC\tN\tidx\tisEmpty\t A\n");
    for(i=0; i<81; i++){
        printf("%d\t%d\t%d\t%d\t%d\t%d\t" , i, CA[i].R, CA[i].C, CA[i].N, CA[i].idx, CA[i].isEmpty); 
        for(j=0; j<CA[i].N; ++j){
            printf("%d ", CA[i].A[j]);
        }
    printf("\n");
    }
}
