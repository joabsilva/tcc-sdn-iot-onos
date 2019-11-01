# -*- coding: utf-8 -*-
#Autor: Joab de Araújo
#Código para uso em aplicação IoT no Trabalho de Conclusão de Curso - TCC
#Título: APLICAÇÃO DE REDES DEFINIDAS POR SOFTWARE EM INTERNET DAS COISAS
#Data: 25/03/2018

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

servo_pin = 17 
ledBranco=19
ledAmarelo=20
ledVerde=21
mpin=22
tpin=23
ledVermelho=26


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

# percebi que ha repeticao de codigo, refatorando...
def outputGPIO(seq):
	# a funcao pega a sequencia de acordo com a cor
	# vermelho, amarelo, verde, branco
	GPIO.output(ledVermelho, seq[0])
	GPIO.output(ledAmarelo, seq[1])
	GPIO.output(ledVerde, seq[2])
	GPIO.output(ledBranco, seq[3])

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
			# mudei a ordem pra que esta no metodo
			# vermelho, amarelo, verde, branco 
			outputGPIO([0,0,0,0])
			set_angle(0)
			
		if t >= 0 and t <= 3000:	
			if t >= 0 and t <= 750:
				print(t)
				ftp_client.put('caminho_local_do_arquivo', 'caminho_remoto_onde_ficara_o_arquivo')
				# vermelho, amarelo, verde*, branco
				outputGPIO([0,0,1,0])
				set_angle(180)
				
			if t > 750 and t <= 1500:				
				print(t)
				ftp_client.put('caminho_local_do_arquivo', 'caminho_remoto_onde_ficara_o_arquivo')
				# vermelho, amarelo*, verde, branco
				outputGPIO([0,1,0,0])
				set_angle(135)
				
			if t > 1500 and t <= 2250:
				print(t)
				ftp_client.put('caminho_local_do_arquivo', 'caminho_remoto_onde_ficara_o_arquivo') 
				# vermelho*, amarelo, verde, branco
				outputGPIO([1,0,0,0])
				set_angle(90)
				
			if t > 2250 and t <= 3000:
				print(t)
				ftp_client.put('caminho_local_do_arquivo', 'caminho_remoto_onde_ficara_o_arquivo') 
				# vermelho, amarelo, verde, branco*
				outputGPIO([0,0,0,1])
				set_angle(45)
		i=0
		t=0
	
