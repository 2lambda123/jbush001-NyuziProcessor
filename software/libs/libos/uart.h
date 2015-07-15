// 
// Copyright 2011-2015 Jeff Bush
// 
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
// 
//     http://www.apache.org/licenses/LICENSE-2.0
// 
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
// 


#pragma once

#ifdef __cplusplus
extern "C" {
#endif

#define UART_STATUS_DR		0x6		// Rx Data Ready
#define UART_STATUS_THRR	0x5		// Transmitter Hold Register (THR) Ready
									// Tx has space for a new character
#define UART_STATUS_BI		0x4		// Rx Break Interrupt
#define UART_STATUS_FE		0x3		// Rx Frame Error
#define UART_STATUS_PE		0x2		// Rx Parity Error
#define UART_STATUS_OE		0x1		// Rx Overrun Error

	
void writeUart(char ch);
unsigned char readUart();

#ifdef __cplusplus
}
#endif

