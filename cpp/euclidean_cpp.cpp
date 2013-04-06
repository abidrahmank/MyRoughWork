// planning to find the squared euclidean distance of two arrays, arrayx and arrayy, in C++, ASM, MMX
// ie z^2 = x^2+y^2
// x<16 and y<16 to avoid overflow


#include <iostream>
#include <time.h>

using namespace std;

extern "C" void euclidean_ASM2(char* array1,char* array2,unsigned int count);
extern "C" void euclidean_MMX(char* array1,char* array2,unsigned int count);
extern "C" void euclidean_SSE(char* array1,char* array2,unsigned int count);

//#DEFINE count 1000000

int main(){
	srand(time(0));
	bool accuracy;
	unsigned int count = 1024*1024; // 256 KB
	unsigned int i = 0; //loop variable
	char* array_x = new char[count];
	char* array_y = new char[count];
	char* array_ASM = new char[count];
	char* array_cpp = new char[count]; // to store a copy of array_x
	double t1,t2,t3,t4,t5,t6;

	// elements of array
	cout << "creating arrays " << endl;
	for (i=0;i<count;i++){
		array_x[i] = rand()%10;
		array_y[i] = rand()%10;
		//array_xcopy[i] = array_x[i];
	}
	cout << "----------------------------------------------------------------------------" << endl;

	/*************************** euclidean in C++ ************************************/
	
	//int j = 0;
	//t1 = clock();
	//while(j<100){
	//for (i=0;i<count;i++){
	//	array_cpp[i] = (array_x[i]*array_x[i]) + (array_y[i]*array_y[i]);
	//}
	//j++;
	//}

	//
	//t2 = clock();
	//t3 = t2 - t1;
	//cout << "time for C++ : " << t3 << endl;
	//cout << "----------------------------------------------------------------------------" << endl;

	/*************************** euclidean in ASM ************************************/

	//j = 0;
	//t6 = 0;
	//while(j<100){
	//for (i=0;i<count;i++){
	//	array_ASM[i] = array_x[i];
	//}
	//t4 = clock();
	//euclidean_ASM2(array_ASM,array_y,count);
	//t5 = clock();
	//t6 = t6+(t5 - t4);
	//j++;
	//}
	//cout << "time in ASM : " << t6 << endl;
	//cout << "speed up ASM v/s C++ : " << t3/t6 << endl;
	//for (i=0;i<count;i++)
	//{
	//	if (array_ASM[i] != array_cpp[i])
	//	{
	//		accuracy = false;
	//		break;
	//	}
	//	else accuracy = true;
	//}
	//if (accuracy == true) cout << "Result is correct " << endl;
	//else cout << "Results do not match with C++ " << endl;
	//cout << "----------------------------------------------------------------------------" << endl;

	/*************************** euclidean in MMX ************************************/

	//j = 0;
	//t6 = 0;
	//while(j<100){
	//for (i=0;i<count;i++){
	//	array_ASM[i] = array_x[i];
	//}
	//t4 = clock();
	//euclidean_MMX(array_ASM,array_y,count);
	//t5 = clock();
	//t6 = t6+ (t5 - t4);
	//j++;
	//}
	//cout << "time in MMX : " << t6 << endl;
	//cout << "speed up MMX v/s C++ : " << t3/t6 << endl;
	//for (i=0;i<count;i++)
	//{
	//	if (array_ASM[i] != array_cpp[i])
	//	{
	//		accuracy = false;
	//		break;
	//	}
	//	else accuracy = true;
	//}
	//if (accuracy == true) cout << "Result is correct " << endl;
	//else cout << "Results do not match with C++ " << endl;
	//cout << "----------------------------------------------------------------------------" << endl;

		/*************************** euclidean in SSE ************************************/
	int j = 0;
	t6 = 0;
	while(j<100){
		for (i=0;i<count;i++){
			array_ASM[i] = array_x[i];
		}
		t4 = clock();
		euclidean_SSE(array_ASM,array_y,count);
		t5 = clock();
		t6 = t6+(t5 - t4);
		j++;
	}
	cout << "time in SSE : " << t6 << endl;
	//cout << "speed up SSE v/s C++ : " << t3/t6 << endl;
	//for (i=0;i<count;i++)
	//{
	//	if (array_ASM[i] != array_cpp[i])
	//	{
	//		accuracy = false;
	//		break;
	//	}
	//	else accuracy = true;
	//}
	//if (accuracy == true) cout << "Result is correct " << endl;
	//else cout << "Results do not match with C++ " << endl;
	//cout << "----------------------------------------------------------------------------" << endl;


	/* ***********************************************************************************************/
	/*								euclidean using SSE2 INTRINSICS									 */
	/* ***********************************************************************************************/

		// int j = 0;
	// t6 = 0;
	// while(j<100){
		// for (i=0;i<count;i++){
			// array_ASM[i] = array_x[i];
		// }
		// t4 = clock();

		// /* code here */




		// /* code ends */
		// t5 = clock();
		// t6 = t6+(t5 - t4);
		// j++;
	// }
	// cout << "time in SSE : " << t6 << endl;





	delete array_x;
	delete array_y;
	delete array_cpp;
	delete array_ASM;
	getchar();
	return 0;
}