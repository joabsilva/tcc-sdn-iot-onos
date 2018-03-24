# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import paramiko
from scp import SCPClient

#Inicia a sessao SSH	
ssh = paramiko.SSHClient() 
#Add o computador remoto ao arquivo Trusted do SSH
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#Conecta ao host remoto
ssh.connect('ip_remoto', username='usuario_remoto', password='senha_remota')

#Inicia a sessao de transferencia de Arquivo
ftp_client=ssh.open_sftp() 

#Setando o modo do GPIO para BCM
GPIO.setmode(GPIO.BCM)

#Definindo variaveis para os pinos 
mpin=22
tpin=23
ledVerde=21
ledAmarelo=20
ledVermelho=26
ledBranco=19
servo_pin = 17 

#Definindo configuracoes para o sensor
cap=0.000001
adj=2.130620985
i=0
t=0

#Desabilitando mensagens de avisos
GPIO.setwarnings(False)

#Ajuste de valores para obter o intervalo completo do movimento do servo
deg_0_pulse   = 0.5 
deg_180_pulse = 2.5
f = 50.0

#Calculos dos parametros da largura do pulso
period = 1000/f
k      = 100/period
deg_0_duty = deg_0_pulse*k
pulse_range = deg_180_pulse - deg_0_pulse
duty_range = pulse_range * k

#Iniciar o pino GPIO do Servo Motor
GPIO.setup(servo_pin,GPIO.OUT)
pwm = GPIO.PWM(servo_pin,f)
pwm.start(0)

#Iniciar os pinos dos leds
GPIO.setup(ledVermelho, GPIO.OUT)
GPIO.setup(ledAmarelo, GPIO.OUT)
GPIO.setup(ledVerde, GPIO.OUT)
GPIO.setup(ledBranco, GPIO.OUT)

def set_angle(angle):
	duty = deg_0_duty + (angle/180.0)* duty_range
	pwm.ChangeDutyCycle(duty)


while True:
    GPIO.setup(mpin, GPIO.OUT) #Iniciar o pino 1 do sensor
    GPIO.setup(tpin, GPIO.OUT) #Iniciar o pino 2 do sensor
    GPIO.output(mpin, False)
    GPIO.output(tpin, False)
    time.sleep(0.2)
    GPIO.setup(mpin, GPIO.IN)
    time.sleep(0.2)
    GPIO.output(tpin, True)
    starttime=time.time()
    endtime=time.time()
    while (GPIO.input(mpin) == GPIO.LOW):
        endtime=time.time()
    measureresistance=endtime-starttime
    
    res=(measureresistance/cap)*adj
    i=i+1
    t=t+res #Limiar
    if i==10:
		t=t/i
		if t > 3000:
			print "Acima do limiar"
			#deixa o motor em 0 graus
			GPIO.output(ledVermelho, 0)
			GPIO.output(ledAmarelo, 0)
			GPIO.output(ledVerde, 0)
			GPIO.output(ledBranco, 0)
			set_angle(0)
		if t >= 0 and t <= 3000:
			
						
			if t >= 0 and t <= 750:
				
				print(t)
				ftp_client.put('caminho_local_do_arquivo', 'caminho_remoto_onde_ficara_o_arquivo') 
				#exemplo: ftp_client.put('/home/raspberry/Documentos/led2.txt', '/home/joab/Documentos/ledAmarelo.txt')				
				GPIO.output(ledVerde, 1)
				GPIO.output(ledVermelho, 0)
				GPIO.output(ledAmarelo, 0)
				GPIO.output(ledBranco, 0)
				set_angle(180)
				
			if t > 750 and t <= 1500:
				
				print(t)
				ftp_client.put('caminho_local_do_arquivo', 'caminho_remoto_onde_ficara_o_arquivo')
				GPIO.output(ledAmarelo, 1)
				GPIO.output(ledVermelho, 0)
				GPIO.output(ledVerde, 0)
				GPIO.output(ledBranco, 0)
				set_angle(135)
				
			if t > 1500 and t <= 2250:
				
				print(t)
				ftp_client.put('caminho_local_do_arquivo', 'caminho_remoto_onde_ficara_o_arquivo') 
				GPIO.output(ledVermelho, 1)
				GPIO.output(ledAmarelo, 0)
				GPIO.output(ledVerde, 0)
				GPIO.output(ledBranco, 0)
				set_angle(90)
				
			if t > 2250 and t <= 3000:
				
				print(t)
				ftp_client.put('caminho_local_do_arquivo', 'caminho_remoto_onde_ficara_o_arquivo') 
				GPIO.output(ledBranco, 1)
				GPIO.output(ledAmarelo, 0)
				GPIO.output(ledVerde, 0)
				GPIO.output(ledVermelho, 0)
				set_angle(45)
		i=0
		t=0
	
