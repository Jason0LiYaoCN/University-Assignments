#include <system.h>
void state0(void);//initial state G0 on. G1,G2 OFF
void state1(void);//G0,G1 on. G2 OFF
void state2(void);//G0,G2 on. G1 OFF
void state3(void);//G0,G1,G2 on.
void state4(void);//Warning state, G0,G1,G2 OFF
void config(void);
//global variables declaration
unsigned char state, nxtstate, inbyte, sensor_s1 , sensor_s2;
int percent_60 = 9;//4 bits: 0xF in decimal is 15. so 0.6*15=9 
int percent_70 = 10;//4 bits: 0xF in decimal is 15. so 0.7*15=10.5  
int percent_90 = 14;//4 bits: 0xF in decimal is 15. so 0.9*15=14.5 

int main(void) {
    config();
    nxtstate=0;
    state=0;

    do{
        switch(state) {
            case 0: {state0(); state=nxtstate;  break;}
            case 1: {state1(); state=nxtstate;  break;}
            case 2: {state2(); state=nxtstate;  break;}
            case 3: {state3(); state=nxtstate;  break;}
            case 4: {state4(); state=nxtstate;  break;}
        }//end of switch. state machine transfer functions.
    }while(1);//end of do while loop
    return(0);
}

///////////////////PIC CONFIGURATION//////////////////////////////

void config(void) {
    cmcon = 0x07;   //this needed to make the porta see digital I/O 
    trisa = 0xff;	//set all the pins of port a as input direction
    trisb = 0x00;   //set all the pins of port b as output direction
    portb = 0;      //initial the value of port b to be 0
}

/////////////////DEFINING THE STATES//////////////////////////////

/*G0 on. G1, G2 LED OFF(Initial state) */
void state0(void){
    inbyte = porta;
    portb = 0x01;//G0 on. G1,G2 OFF
    sensor_s1 = inbyte & 0x0F; //first four bits as sensor s1
    sensor_s2 = inbyte >> 4; // the following four bits as sensor s2 data
    if((sensor_s1 <= percent_60) && (sensor_s2 <= percent_70)){
        nxtstate = 0;
    }
    else if ((sensor_s1 > percent_60) && (sensor_s2 <= percent_70)){
        nxtstate = 1;
    }
    else if ((sensor_s1 <= percent_60) && (sensor_s2 > percent_70)){
        nxtstate = 2;
    }
    else if ((sensor_s1 > percent_60) && (sensor_s2 > percent_70)){
        nxtstate = 3;
    }
}//end of state0.

/*G0, G1 on. G2 LED OFF*/
void state1(void){
    inbyte = porta;
    portb = 0x03; //G0,G1 on. G2 OFF
    sensor_s1 = inbyte & 0x0F; //first four bits as sensor s1
    sensor_s2 = inbyte >> 4; // the following four bits as sensor s2 data
    if(sensor_s1 <= percent_60){
        nxtstate = 0;
        return;
    }

    if(sensor_s2 <= percent_70){
        nxtstate = 1;
    }
    else {
        nxtstate = 3;
    }
}//end of state1.

/*G0, G2 on. G1 LED OFF*/
void state2(void){
    inbyte = porta;
    portb = 0x05;//G0,G2 on. G1 OFF
    sensor_s1 = inbyte & 0x0F; //first four bits as sensor s1
    sensor_s2 = inbyte >> 4; // the following four bits as sensor s2 data
    if(sensor_s2 <= percent_70){
        nxtstate = 0;
        return;
    }

    if(sensor_s1 <= percent_60){
        nxtstate = 2;
    }
    else {
        nxtstate = 3;
    }
}//end of state2.

/*G0, G1, G2 on.LED OFF*/
void state3(void){
    int count = 0;
    inbyte = porta;
    portb = 0x07;//G0,G1,G2 ON
    sensor_s1 = inbyte & 0x0F; //first four bits as sensor s1
    sensor_s2 = inbyte >> 4; // the following four bits as sensor s2 data
    if(sensor_s1 <= percent_60) {
        nxtstate = 1;
    }
    else if (sensor_s2 <= percent_70) {
        nxtstate = 2;
    }
    else if ((sensor_s1 <= percent_90)&&(sensor_s2 <= percent_90)){
        nxtstate = 3;
    }
    else if ((sensor_s1 > percent_90)&&(sensor_s2 > percent_90)){
        delay_s(3);//after 10 seconds check again.
        if((sensor_s1 > percent_90)&&(sensor_s2 > percent_90)){
            nxtstate = 4;
        }
        else{
            nxtstate = 3;
        }
    }
}//end of state3.
/*G0, G1, G2 OFF. LED ON(overloading, warning state)*/
void state4(void){
    inbyte = porta;
    portb = 0x80;//G0,G1,G2 OFF, warning LED bit(7) high
    sensor_s1 = inbyte & 0x0F; //first four bits as sensor s1
    sensor_s2 = inbyte >> 4; // the following four bits as sensor s2 data
    if((sensor_s1 == 0)&&(sensor_s2 == 0)) {
        nxtstate = 0;
    }
    else {
        nxtstate = 4;
    }
}//end of state4.