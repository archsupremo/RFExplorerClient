//============================================================================
//RF Explorer - A Handheld Spectrum Analyzer for everyone!
//  This is a simple capture tool for Linux
//  Developed by Cesar Lopez Ramirez from URJC, Madrid, Spain
//
//This application is free software; you can redistribute it and/or
//modify it under the terms of the GNU Lesser General Public
//License as published by the Free Software Foundation; either
//version 3.0 of the License, or (at your option) any later version.
//
//This software is distributed in the hope that it will be useful,
//but WITHOUT ANY WARRANTY; without even the implied warranty of
//MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
//General Public License for more details.
//
//You should have received a copy of the GNU General Public
//License along with this library; if not, write to the Free Software
//Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
//=============================================================================

/*
from Cesar Lopez Ramirez <cesarlr@gmail.com>
Here is the script for Linux. The usage is

    rfexplorer /dev/ttyUSB0 0400000 0500000 050 120

where
    1st parameter is linux device,
    2nd is start freq (7 chars)
    3rd is end freq (7 chars)
    4th is amp top (3 chars) (without minus)
    5th is amp bottom (3 chars) (without minus)

The output is a CSV file in the same way as the mac client does.
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <termios.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/signal.h>
#include <sys/types.h>
#define BAUDRATE B500000
#define FALSE 0
#define TRUE 1
void signal_handler_IO (int status);   /* definition of signal handler */

int main(int argc, char **argv)
{
  int fd,res,i;
  FILE *f;
  struct sigaction saio;
  struct termios oldtio,newtio;
  char fname[24];
  char line2[20];
  char sweep_steps;
  char *sweep_data;
  time_t t = time(0);
  struct tm *localt = localtime(&t);
  char buf[255];
  char sPortName[255];
  strcpy(sPortName,argv[1]);
  fd = open(sPortName, O_RDWR | O_NOCTTY | O_NONBLOCK);
  if (fd <0)
  {
      perror(sPortName);
      exit(-1);
  }
  /* install the signal handler before making the device asynchronous */
  memset(&saio,0x0,sizeof(saio));
  saio.sa_handler = signal_handler_IO;
  sigaction(SIGIO,&saio,NULL);
  /* allow the process to receive SIGIO */
  fcntl(fd, F_SETOWN, getpid());
  /* Make the file descriptor asynchronous (the manual page says only
     O_APPEND and O_NONBLOCK, will work with F_SETFL...) */
  fcntl(fd, F_SETFL, FASYNC);

  tcgetattr(fd,&oldtio); /* save current port settings */
  /* set new port settings for canonical input processing */
  newtio.c_cflag = BAUDRATE | CS8 | CLOCAL | CREAD;
  newtio.c_iflag = IGNPAR | ICRNL;
  newtio.c_oflag = 0;
  newtio.c_lflag = ICANON;
  newtio.c_cc[VMIN]=1;
  newtio.c_cc[VTIME]=0;
  tcflush(fd, TCIFLUSH);
  tcsetattr(fd,TCSAFLUSH,&newtio);
  buf[0]='#';
  buf[1]=32;
  buf[2]='C';
  buf[3]='2';
  buf[4]='-';
  buf[5]='F';
  buf[6]=':';
  buf[7]=argv[2][0];
  buf[8]=argv[2][1];
  buf[9]=argv[2][2];
  buf[10]=argv[2][3];
  buf[11]=argv[2][4];
  buf[12]=argv[2][5];
  buf[13]=argv[2][6];
  buf[14]=',';
  buf[15]=argv[3][0];
  buf[16]=argv[3][1];
  buf[17]=argv[3][2];
  buf[18]=argv[3][3];
  buf[19]=argv[3][4];
  buf[20]=argv[3][5];
  buf[21]=argv[3][6];
  buf[22]=',';
  buf[23]='-';
  buf[24]=argv[4][0];
  buf[25]=argv[4][1];
  buf[26]=argv[4][2];
  buf[27]=',';
  buf[28]='-';
  buf[29]=argv[5][0];
  buf[30]=argv[5][1];
  buf[31]=argv[5][2];
  write(fd,buf,32);
  do {
    memset(buf,0x0,sizeof(buf));
    pause();
    res = read(fd,buf,255);
  }while(buf[0]!='$');
  sweep_steps=buf[2];
  res=0;
  while(res<sweep_steps+5) {
    pause();
    res += read(fd,buf+res,255);
  }
  res=0;
  //strftime(fname,24,"%Y_%m_%d_%H_%M_%S.txt",localt);
  //strftime(fname,24,"%Y_%m_%d.txt",localt);
  //f=fopen(fname,"w");
  //fprintf(f,"--------------------\r\n");
  //strftime(line2,20,"%Y-%m-%d-%H:%M:%S",localt);
  //fprintf(f,"%s\r\n",line2);
  //fprintf(f,"\r\n");
  //fprintf(f,"\r\n");
  //fprintf(f,"Frequency(mHZ)\tSignal (dBm)\r\n");
  for(i=0;i<sweep_steps;i++){
    printf("%ld\t%6.6f\r\n",(atol(argv[2])+i*(atol(argv[3])-atol(argv[2]))/sweep_steps)*1000,-1*(((float)(unsigned char)buf[i+4]))/2);
    //fprintf(f,"%ld\t%6.6f\r\n",(atol(argv[2])+i*(atol(argv[3])-atol(argv[2]))/sweep_steps)*1000,-1*(((float)(unsigned char)buf[i+4]))/2);
  }
  //fclose(f);
  return 0;
}
void signal_handler_IO (int status)
{
}
