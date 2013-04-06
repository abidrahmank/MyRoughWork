
.model C,flat

.data

.code

euclidean_ASM proc
	mov esi,[esp+1*4]	; x_ptr in edx
	mov edi,[esp+2*4]	; y_ptr in ebx
	mov ecx,[esp+3*4]	; counter in ecx
	
	MainLoop:
	mov al,[esi]		; al <- Y
	mul al				; Y2 <- Y*Y
	mov bl,al

	mov al,[edi]		; al <- X
	mul al				; X <- X*X

	add al,bl			; AL <- X2+Y2

	mov [esi],al		; answer in X[i]
	
	inc esi
	inc edi
	dec ecx				; decrement counter
	jnz MainLoop

	ret
euclidean_ASM endp

euclidean_ASM2 proc
	mov ebx,[esp+1*4]	; x_ptr in edx
	mov edx,[esp+2*4]	; y_ptr in ebx
	mov ecx,[esp+3*4]	; counter in ecx
	
	MainLoop:
	mov eax,dword ptr[edx]		; al <- Y
	mul al				; Y2 <- Y*Y
	push eax

	mov eax,dword ptr[ebx]		; al <- X
	mul al				; X <- X*X

	add eax,[esp]		; AL <- X2+Y2

	mov [ebx],al		; answer in X[i]
	pop eax
	
	inc ebx
	inc edx
	dec ecx				; decrement counter
	jnz MainLoop

	ret
euclidean_ASM2 endp


euclidean_MMX proc
	mov eax,[esp+1*4]	; x_ptr in eax
	mov ebx,[esp+2*4]	; y_ptr in ebx
	mov ecx,[esp+3*4]	; counter in ecx
	shr ecx,3;

	pxor mm7,mm7				; clear mm7 to store 0

	MainLoop:
	;
	; First do with X vector
	;
	movq mm0,qword ptr[eax]		; 8 bytes from EAX
	movq mm1,mm0				; make a copy of mm0

	punpckhbw mm1,mm7			; convert B -> W for upper half
	pmullw mm1,mm1				; square and keep the lower order

	punpcklbw mm0,mm7			; convert B -> W for lower half
	pmullw mm0,mm0				; square and keep the lower order
	
	packuswb mm0,mm1			; pack words into bytes
								; mm0 has X2

	;
	;Now with Y vector
	;
	movq mm1,qword ptr[ebx]		; 8 bytes from EAX
	movq mm2,mm1				; make a copy of mm0

	punpckhbw mm2,mm7			; convert B -> W for upper half
	pmullw mm2,mm2				; square and keep the lower order

	punpcklbw mm1,mm7			; convert B -> W for lower half
	pmullw mm1,mm1				; square and keep the lower order
	
	packuswb mm1,mm2			; pack words into bytes
								; mm1 has Y2

	; Now add them
	paddb mm0,mm1				; z2 = x2+y2
	movq [eax],mm0				; store back the results
	add eax,8					; move eax by 8 bytes
	add ebx,8					; move ebx by 8 bytes
	dec ecx
	jnz MainLoop
	
	emms
	ret
euclidean_MMX endp


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
;				SSE2 ASSEMBLY
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

euclidean_SSE proc
	mov eax,[esp+1*4]	; x_ptr in eax
	mov ebx,[esp+2*4]	; y_ptr in ebx
	mov ecx,[esp+3*4]	; counter in ecx
	shr ecx,4

	pxor xmm7,xmm7				; clear mm7 to store 0
	pxor xmm6,xmm6

	MainLoop:
	;
	; First do with X vector
	;
	movdqu xmm0,xmmword ptr[eax]; 16 bytes from EAX
	movdqu xmm1,xmm0			; make a copy of xmm0

	punpckhbw xmm1,xmm7			; convert B -> W for upper half
	pmullw xmm1,xmm1			; square and keep the lower order

	punpcklbw xmm0,xmm7			; convert B -> W for lower half
	pmullw xmm0,xmm0			; square and keep the lower order
	
	packuswb xmm0,xmm1			; pack words into bytes
								; xmm0 has X2

	;
	;Now with Y vector
	;
	movdqu xmm1,xmmword ptr[ebx]; 8 bytes from EAX
	movdqu xmm2,xmm1			; make a copy of mm0

	punpckhbw xmm2,xmm7			; convert B -> W for upper half
	pmullw xmm2,xmm2			; square and keep the lower order

	punpcklbw xmm1,xmm7			; convert B -> W for lower half
	pmullw xmm1,xmm1			; square and keep the lower order
	
	packuswb xmm1,xmm2			; pack words into bytes
								; mm1 has Y2

	; Now add them
	paddb xmm0,xmm1				; z2 = x2+y2
	movdqu [eax],xmm0			; store back the results
	add eax,16					; move eax by 16 bytes
	add ebx,16					; move ebx by 16 bytes
	dec ecx
	jnz MainLoop
	
	emms
	ret
euclidean_SSE endp
end
