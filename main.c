/*
 *  Routines to access hardware
 *
 *  Copyright (c) 2016 Realtek Semiconductor Corp.
 *
 *  This module is a confidential and proprietary property of RealTek and
 *  possession or use of this module requires written permission of RealTek.
 */
#include "cmsis.h"
#include "cmsis_os.h"
#include "hal_timer.h"
#include "timer_api.h"
#include "hal_uart.h"
#include "dma_api.h"
#include "hal_gdma.h"
#include "memory.h"


/*UART pin location:
   UART0: 
   PIN_A11  (TX)
   PIN_A12  (RX)
   */
#define UART_TX    PIN_A11
#define UART_RX    PIN_A12
#define DMA_BUFFER __ALIGNED(32)

#if 0
// Use Cacheable DMA buffer
#define TEST_BUF_SIZE       (1188*32)  // DMA buffer size should be multiple of 32

DMA_BUFFER char uart_test_tx_buf[TEST_BUF_SIZE];
DMA_BUFFER char uart_test_rx_buf[TEST_BUF_SIZE];
#else
// Use non-cacheable DMA buffer
#define TEST_BUF_SIZE       (4096)  // DMA buffer size should be multiple of 32

NC_BSS_SECTION char uart_test_tx_buf[TEST_BUF_SIZE];
NC_BSS_SECTION char uart_test_rx_buf[TEST_BUF_SIZE];
#endif

uint32_t test_len = 16;
#define MAX_TEST_TIMER_ID       16


#define DMA_CPY_LEN     256
#define DMA_SRC_OFFSET  0
#define DMA_DST_OFFSET  0

//gdma_t gdma;
uint8_t TestBuf1[512];
uint8_t TestBuf2[512];
volatile uint8_t dma_done;
hal_gdma_adaptor_t gdma_adaptor;
hal_gdma_group_t gdma_group;


#if CONFIG_CMSIS_RTX_EN | CONFIG_CMSIS_FREERTOS_EN
void Timer_Thread_Oneshot( void *pvParameters ); // one-shot timer
void Timer_Thread_Periodical( void *pvParameters ); // periodical timer
void UART_Thread( void *pvParameters );
void GDMA_Thread( void *pvParameters );

osThreadId tid_timer_Oneshot;                             // thread id
osThreadDef (Timer_Thread_Oneshot, osPriorityNormal, 1, 2048);      // thread object

osThreadId tid_timer_Periodical;                             // thread id
osThreadDef (Timer_Thread_Periodical, osPriorityNormal, 1, 2048);      // thread object

osThreadId tid_uart;                             // thread id
osThreadDef (UART_Thread, osPriorityNormal, 1, 2048);      // thread object

osThreadId tid_gdma;                             // thread id
osThreadDef (GDMA_Thread, osPriorityNormal, 1, 2048);      // thread object

#endif




/* Used as a loop counter to create a very crude delay. */
#define mainDELAY_LOOP_COUNT		( 0xfff )

char rc;
hal_timer_group_adapter_t test_timer_group1;
//hal_timer_adapter_t test_timer[MAX_TEST_TIMER_ID];
hal_uart_adapter_t test_uart;
hal_timer_adapter_t ptimer_oneshot;
hal_timer_adapter_t ptimer_periodical;

volatile uint32_t time1_expired=0;
volatile uint32_t time2_not_opened=1;
volatile char tx_done=0;
volatile char rx_done=0;
u32 countforerr_inuart=0;
u32 countforerr_ingdma=0;

/**
  * @brief  Main program.
  * @param  None
  * @retval None
  */
/*-----------------------------------------------------------*/
void timer_test_callback_oneshot (void *hid)
{
    dbg_printf("One shot timer has reached its callback handler\r\n");
    time1_expired = 1;
}

void timer_test_callback_periodical (void *hid)
{
    dbg_printf("periodical timer has reached its callback handler\r\n");
}


void dma_done_handler(int id) 
{
    dbg_printf("DMA Copy Done!!\r\n");
    dma_done = 1;    
}

void uart_txdone_callback(void *arg)
{
    dbg_printf("%s==> arg=0x%x\r\n", __FUNCTION__, arg);
    tx_done = 1;
}

void uart_rxdone_callback(phal_uart_adapter_t puart_adp)
{
    uint32_t rxed_len;
    uint32_t i;
    uint32_t dump_i=0;
    
    dbg_printf("%s==> stat=0x%x prx_buf_dar=0x%x\r\n", __FUNCTION__, puart_adp->state, puart_adp->prx_buf_dar);
    rxed_len = (uint32_t)(puart_adp->prx_buf) - (uint32_t)(puart_adp->prx_buf_dar);

    dbg_printf("Received data(len = %u): 0x%x -> 0x%x \r\n", rxed_len, (uint32_t)(puart_adp->prx_buf_dar), (uint32_t)(puart_adp->prx_buf));
    if (rxed_len != test_len) {
        dbg_printf("Received data(%lu) != Initialated RX_Len(%lu) \r\n", rxed_len, test_len);
        while(1);
    }

    for (i=0; i<rxed_len; i++) {
        if (uart_test_tx_buf[i] != uart_test_rx_buf[i]) {
            if (i >= dump_i) {
                dump_i = i+16;
                dbg_printf ("\r\nTX Data:\r\n");
                dump_bytes((u8 *)&uart_test_tx_buf[i], 16);
                dbg_printf ("\r\nRX Data:\r\n");
                dump_bytes((u8*)&uart_test_rx_buf[i], 16);
            }
        }
    }

    if (dump_i == 0) {        
        dbg_printf ("Data Verify OK!\r\n");
    } else {
        dbg_printf ("Data Verify Err!\r\n");
//        while(1);
    }
#if 0    
    if (memcmp (uart_test_tx_buf, uart_test_rx_buf, rxed_len) != 0) {
        dbg_printf ("!!Data Verify Error!!!!");
        dbg_printf ("TX Data:\r\n");
        dump_bytes(uart_test_tx_buf, rxed_len);
        dbg_printf ("RX Data:\r\n");
        dump_bytes(uart_test_rx_buf, rxed_len);
    } else {
        dbg_printf ("Data Verify OK!\r\n");
    }
#endif

    rx_done = 1;
    __DSB();
    __ISB();
}

void main( void )
{
    dbg_printf("enter into main\r\n");
    /*variables declaration*/
	int i;
	uint32_t ret;
	u8 Uart_loop_back_val;
	/*Init timer*/
	hal_timer_group_init (&test_timer_group1, 1);
    hal_timer_group_sclk_sel (&test_timer_group1, 32000);
    //ptimer = &test_timer[3];
    ret = hal_timer_init (&ptimer_oneshot, 3);//init timer 3
    ret = hal_timer_init (&ptimer_periodical, 4);//init timer 4
	time1_expired = 0;
    hal_timer_start_one_shot (&ptimer_oneshot, 50000, (timer_callback_t)timer_test_callback_oneshot, (void *)NULL);// start a timer for test

	/*Init UART*/
    hal_uart_init (&test_uart, UART_TX, UART_RX, NULL);
    hal_uart_set_baudrate (&test_uart, 115200);
    hal_uart_set_format (&test_uart, 8, 0, 1);
    hal_uart_set_flow_control (&test_uart, UartFlowCtlNone);
	hal_uart_rxdone_hook (&test_uart, uart_rxdone_callback, &test_uart);
	hal_uart_txdone_hook (&test_uart, uart_txdone_callback, &test_uart);
	Uart_loop_back_val = HAL_READ8(0x40003000,0x10);
	HAL_WRITE8(0x40003000,0x10,Uart_loop_back_val|0x10);
    for (i=0;i<test_len;i+=4) {
        uart_test_tx_buf[i] = 'I';
        uart_test_tx_buf[i+1] = 'T';
        uart_test_tx_buf[i+2] = 'I';
        uart_test_tx_buf[i+3] = 'R';
    }	
	/*Init GDMA*/
	hal_gdma_memcpy_init(&gdma_adaptor);
    hal_gdma_memcpy_irq_hook(&gdma_adaptor,(irq_handler_t)dma_done_handler,0);
	
    for (i=0;i< 512;i++) {
        TestBuf1[i] = i;
    }
    memset(TestBuf2, 0xff, 512);
	
#if CONFIG_CMSIS_RTX_EN | CONFIG_CMSIS_FREERTOS_EN
	ret = osKernelInitialize ();					// initialize CMSIS-RTOS
	if (ret != osOK) {
	    dbg_printf ("KernelInitErr(0x%x)\r\n", ret);
		while(1);
	}

	tid_timer_Oneshot = osThreadCreate (osThread(Timer_Thread_Oneshot), NULL);
	if (tid_timer_Oneshot == 0) {
		dbg_printf ("Create Timer_Thread_Oneshot error\r\n");
	}
	tid_timer_Periodical= osThreadCreate (osThread(Timer_Thread_Periodical), NULL);
	if (tid_timer_Periodical == 0) {
		dbg_printf ("Create tid_timer_Periodical error\r\n");
	}
	tid_uart = osThreadCreate (osThread(UART_Thread), NULL);
	if (tid_uart == 0) {
		dbg_printf ("Create UART_Thread error\r\n");
	}
	tid_gdma = osThreadCreate (osThread(GDMA_Thread), NULL);
	if (tid_gdma == 0) {
		dbg_printf ("Create GDMA_Thread error\r\n");
	}
	ret = osKernelStart (); 						// start thread execution 
	while(1);
#endif
}
/*-----------------------------------------------------------*/

void Timer_Thread_Oneshot( void *pvParameters )
{
    volatile uint32_t ul;
    while(1){
	/* Print out the name of this task. */
	dbg_printf("Task 1 is running\r\n");
        /* Delay for a period. */
        for( ul = 0; ul < mainDELAY_LOOP_COUNT; ul++ ){
            /* This loop is just a very crude delay implementation.  There is
	    	nothing to do in here.  Later exercises will replace this crude
	    	loop with a proper delay/sleep function. */
        }
        if (time1_expired) {
            time1_expired = 0;
            hal_timer_start_one_shot (&ptimer_oneshot, 50000, (timer_callback_t)timer_test_callback_oneshot, (void *)NULL);
        }
    }
}

/*-----------------------------------------------------------*/

void Timer_Thread_Periodical( void *pvParameters )
{
    volatile uint32_t ul;
    while(1){
	/* Print out the name of this task. */
	dbg_printf("Task 2 is running\r\n");
        /* Delay for a period. */
        for( ul = 0; ul < mainDELAY_LOOP_COUNT; ul++ ){
            /* This loop is just a very crude delay implementation.  There is
	    	nothing to do in here.  Later exercises will replace this crude
	    	loop with a proper delay/sleep function. */
        }
        if (time2_not_opened) {
            time2_not_opened = FALSE;
            hal_timer_start_periodical (&ptimer_periodical, 50000, (timer_callback_t)timer_test_callback_periodical, (void *)NULL);
        }
    }
}

/*-----------------------------------------------------------*/

void UART_Thread( void *pvParameters )
{
    volatile uint32_t ul;
	uint32_t ret;
    while(1){
        /* Print out the name of this task. */
	    dbg_printf("Task 3 is running\r\n");
        for( ul = 0; ul < mainDELAY_LOOP_COUNT; ul++ ){
            /* This loop is just a very crude delay implementation.  There is
	        nothing to do in here.  Later exercises will replace this crude
	        loop with a proper delay/sleep function. */
        }
		memset(uart_test_rx_buf, 0xff, test_len);
	    rx_done = 0;
		ret = hal_uart_int_recv (&test_uart, uart_test_rx_buf, test_len);
		tx_done = 0;
		if (ret != HAL_OK) {
		    dbg_printf("Err in uart int recv: 0x%x\r\n", ret);
			countforerr_inuart ++;
	    }
        ret = hal_uart_int_send (&test_uart, uart_test_tx_buf, test_len);
		if (ret != HAL_OK) {
			countforerr_inuart ++;
		    dbg_printf("Err in uart int send: 0x%x\r\n", ret);
	    }
		dbg_printf("countforerr_inuart is %d\r\n", countforerr_inuart);
		while(!tx_done);
    }
}

/*-----------------------------------------------------------*/
void GDMA_Thread( void *pvParameters )
{
    volatile uint32_t ul;
	uint32_t ret;
    while(1){
        /* Print out the name of this task. */
	    dbg_printf("Task 4 is running\r\n");
        for( ul = 0; ul < mainDELAY_LOOP_COUNT; ul++ ){
            /* This loop is just a very crude delay implementation.  There is
	        nothing to do in here.  Later exercises will replace this crude
	        loop with a proper delay/sleep function. */
        }
	    ret = hal_gdma_memcpy(&gdma_adaptor, TestBuf2 + DMA_DST_OFFSET, TestBuf1 + DMA_SRC_OFFSET, DMA_CPY_LEN);
		if (ret != HAL_OK) {
			countforerr_ingdma ++;
		    dbg_printf("Err in gdma copy: 0x%x\r\n", ret);
	    }
        for( ul = 0; ul < mainDELAY_LOOP_COUNT; ul++ ){
            /* This loop is just a very crude delay implementation.  There is
            nothing to do in here.  Later exercises will replace this crude
	        loop with a proper delay/sleep function. */
        }
		dbg_printf("countforerr_ingdma is %d\r\n", countforerr_ingdma);
        while (dma_done == 0);
    }
}





