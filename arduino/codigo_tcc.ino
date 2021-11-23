#include <PZEM004Tv30.h>

PZEM004Tv30 pzem(10, 11); // (RX,TX)connect to TX,RX of PZEM
PZEM004Tv30 pzem2(8, 9);  // (RX,TX) connect to TX,RX of PZEM

char caracter;
int geladeira = 7;
int motor = 5;
int lampada = 6;

String teste1 = "";
String teste2 = "";

void setup() {
  Serial.begin(9600);
  pinMode(geladeira, OUTPUT);
  pinMode(motor, OUTPUT);
  pinMode(lampada, OUTPUT);
}

void loop() {

  //main energy meter
  float voltage = pzem.voltage();
  float current = pzem.current();
  float power = pzem.power();
  float energy = pzem.energy();
  float frequency = pzem.frequency();
  float pf = pzem.pf();

  //energymeter 2
  float voltage2 = pzem2.voltage();
  float current2 = pzem2.current();
  float power2 = pzem2.power();
  float energy2 = pzem2.energy();
  float frequency2 = pzem2.frequency();
  float pf2 = pzem2.pf();

  //  if(current != NAN && voltage != NAN && current2 != NAN && voltage2 != NAN ){
  if ( current2 != NAN && voltage2 != NAN ) {

    //  Serial.print("Geladeira - Voltage: ");Serial.print("127.2");Serial.print("V|");
    //
    //  Serial.print("Current: ");Serial.print("9.44");Serial.print("A|");
    //
    //  Serial.print("Power: ");Serial.print("1204");Serial.print("W|||");

    String unidadetensao = "V|";
    String unidadecorrente = "A|";
    String unidadepotencia = "W|||";

    String nomeequip1 = "Geladeira - Voltage: ";
    String nomeequip2 = "Iluminacao - Voltage: ";
    String nomeequip3 = "Motor - Voltage: ";

    
    String tensao1 = "127.2";
    String corrente1 = "2.07";
    String potencia1 = "147";

    String string_final = nomeequip1+tensao1+unidadetensao+"Current: "+corrente1+unidadecorrente+"Power: "+potencia1+unidadepotencia+nomeequip2+voltage+unidadetensao+"Current: "+current+unidadecorrente+"Power: "+power+unidadepotencia+nomeequip3+voltage2+unidadetensao+"Current: "+current2+unidadecorrente+"Power: "+power2+unidadepotencia+"#";

    Serial.print(string_final);


//    Serial.print("Geladeira - Voltage: "); Serial.print("127.2"); Serial.print("V|");
//
//    Serial.print("Current: "); Serial.print("2.07"); Serial.print("A|");
//
//    Serial.print("Power: "); Serial.print("147"); Serial.print("W|||");
//
//
//    Serial.print("Iluminacao - Voltage: "); Serial.print(voltage); Serial.print("V|");
//
//    Serial.print("Current: "); Serial.print(current); Serial.print("A|");
//
//    Serial.print("Power: "); Serial.print(power); Serial.print("W|||");
//
//
//    Serial.print("Motor - Voltage: "); Serial.print(voltage2); Serial.print("V|");
//
//    Serial.print("Current: "); Serial.print(current2); Serial.print("A|");
//
//    Serial.print("Power: "); Serial.print(power2); Serial.print("W");
//
//    Serial.print("#");
  }
 

  else {
    Serial.println("Erro lendo energia");
  }

  String teste1 = "teste: ";
  String teste2 = "2A";
  
  String teste3 = teste1 + teste2;
  
  caracter = Serial.read();
  if (caracter == '1')
  {
    digitalWrite(geladeira, HIGH);
  }
  if (caracter == 'A')
  {
    digitalWrite(geladeira, LOW);
  }
  if (caracter == '2')
  {
    digitalWrite(motor, HIGH);
  }
  if (caracter == 'B')
  {
    digitalWrite(motor, LOW);
  }

  if (caracter == '3')
  {
    digitalWrite(lampada, HIGH);
  }
  if (caracter == 'C')
  {
    digitalWrite(lampada, LOW);
  }

  delay(1000);
}
