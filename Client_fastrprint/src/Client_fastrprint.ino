/*************************************************** 
  Client_fastrprint test

  Designed specifically to work with the Adafruit WiFi products:
  ----> https://www.adafruit.com/products/1469

  Adafruit invests time and resources providing this open source code, 
  please support Adafruit and open-source hardware by purchasing 
  products from Adafruit!

  Written by Tony DiCola, based on code example code written by
  Limor Fried & Kevin Townsend for Adafruit Industries.  
  BSD license, all text above must be included in any redistribution
 ****************************************************/
 
#include <Adafruit_CC3000.h>
#include <ccspi.h>
#include <SPI.h>
#include <string.h>
#include "utility/debug.h"

Adafruit_CC3000 cc3000 = Adafruit_CC3000(ADAFRUIT_CC3000_CS, ADAFRUIT_CC3000_IRQ, ADAFRUIT_CC3000_VBAT,
                                         SPI_CLOCK_DIV2); // you can change this clock speed

// Test server configuration
const uint8_t   SERVER_IP[4]   = { SERVER_IP_A, SERVER_IP_B, SERVER_IP_C, SERVER_IP_D };

#define ASSERT_EQ(expected, actual) { \
  if (actual != expected) { \
    Serial.print("FAILURE: Expected "); \
    Serial.print(actual); \
    Serial.print(" to equal "); \
    Serial.println(expected); \
  } \
}

#define TEST_FASTRPRINT(message, client) { \
  Serial.print("Testing fastrprint with char* input: "); \
  Serial.println(message); \
  unsigned long n = client.fastrprint(message); \
  ASSERT_EQ(sizeof(message)-1, n); \
}

#define TEST_FASTRPRINTLN(message, client) { \
  Serial.print("Testing fastrprintln with char* input: "); \
  Serial.println(message); \
  unsigned long n = client.fastrprintln(message); \
  ASSERT_EQ(sizeof(message)+1, n); \
}

#define TEST_FASTRPRINT_F(message, client) { \
  Serial.print("Testing fastrprint with flash string input: "); \
  Serial.println(F(message)); \
  unsigned long n = client.fastrprint(F(message)); \
  ASSERT_EQ(sizeof(message)-1, n); \
}

#define TEST_FASTRPRINTLN_F(message, client) { \
  Serial.print("Testing fastrprintln with flash string input: "); \
  Serial.println(F(message)); \
  unsigned long n = client.fastrprintln(F(message)); \
  ASSERT_EQ(sizeof(message)+1, n); \
}

// Run the test
void runTest(void) {
  // Make two connections to the server running listener.py
  Serial.println(F("Connecting to server..."));
  Adafruit_CC3000_Client client1 = cc3000.connectTCP(cc3000.IP2U32(SERVER_IP[0], SERVER_IP[1], SERVER_IP[2], SERVER_IP[3]), 
                                                     SERVER_PORT);
  if (!client1.connected()) {
    Serial.println(F("Couldn't connect to server! Make sure listener.py is running on the server."));
    while(1);
  }
  Adafruit_CC3000_Client client2 = cc3000.connectTCP(cc3000.IP2U32(SERVER_IP[0], SERVER_IP[1], SERVER_IP[2], SERVER_IP[3]), 
                                                     SERVER_PORT);
  if (!client2.connected()) {
    Serial.println(F("Couldn't connect to server! Make sure listener.py is running on the server."));
    while(1);
  }
  Serial.println(F("Connected!"));
  
  // Start the test
  Serial.print(F("Free RAM: ")); Serial.println(getFreeRam(), DEC);
  Serial.println(F("Starting tests..."));
  unsigned long start = millis();
  
  // Test character strings
  TEST_FASTRPRINT("Fastrprint string.", client1);
  TEST_FASTRPRINT("Fastrprint with a large (>32 character) character string!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", client1);
  TEST_FASTRPRINTLN("Fastrprintln string.", client1);
  TEST_FASTRPRINTLN("Fastrprintln with a large (>32 character) character string!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", client1);
  
  // Test flash strings
  TEST_FASTRPRINT_F("Fastrprint flash.", client1);
  TEST_FASTRPRINT_F("Fastrprint with a large (>32 character) flash string!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", client1);
  TEST_FASTRPRINTLN_F("Fastrprintln flash.", client1);
  TEST_FASTRPRINTLN_F("Fastrprintln with a large (>32 character) flash string!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", client1);
  
  // Test empty strings
  TEST_FASTRPRINT("", client1);
  TEST_FASTRPRINTLN("", client1);
  TEST_FASTRPRINT_F("", client1);
  TEST_FASTRPRINTLN_F("", client1);
  
  // Test printing to multiple clients
  TEST_FASTRPRINT("This is a message for client 1.", client1);
  TEST_FASTRPRINT("This is a message for client 2.", client2);
  TEST_FASTRPRINT_F("This is a flash message for client 1.", client1);
  TEST_FASTRPRINT_F("This is a flash message for client 2.", client2);
  TEST_FASTRPRINT_F("This is a large (>32 character) flash message for client 1!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", client1);
  TEST_FASTRPRINT_F("This is a large (>32 character) flash message for client 2!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", client2);

  unsigned long finish = millis();
  Serial.println(F("Tests finished!"));
  Serial.print(F("Free RAM: ")); Serial.println(getFreeRam(), DEC);
  Serial.print(F("Time taken to run test (MS): ")); Serial.println(finish - start, DEC);
  
  client1.close();
  client2.close();
  cc3000.disconnect();
}

// Set up the HW and the CC3000 module (called automatically on startup)
void setup(void)
{
  Serial.begin(115200);
  Serial.println(F("Hello, CC3000!\n")); 
  
  /* Initialise the module */
  Serial.println(F("\nInitializing..."));
  if (!cc3000.begin())
  {
    Serial.println(F("Couldn't begin()! Check your wiring?"));
    while(1);
  }
  
  if (!cc3000.connectToAP(WLAN_SSID, WLAN_PASS, WLAN_SECURITY)) {
    Serial.println(F("Failed!"));
    while(1);
  }
   
  Serial.println(F("Connected!"));
  
  /* Wait for DHCP to complete */
  Serial.println(F("Request DHCP"));
  while (!cc3000.checkDHCP())
  {
    delay(100); // ToDo: Insert a DHCP timeout!
  }  
  
  runTest();
}

void loop(void)
{
 delay(1000);
}
