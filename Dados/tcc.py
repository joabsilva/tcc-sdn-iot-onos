import RPi.GPIO as GPIO
import time
import paramiko
from scp import SCPClient

#Inicia a sessao SSH	
#ssh = paramiko.SSHClient() 
#Add o computador remoto ao arquivo Trusted do SSH
#ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#Conecta ao host remoto
#ssh.connect('10.1.131.10', username='joab', password='n3verm0re')

#Inicia a sessao de transferencia de Arquivo
#ftp_client=ssh.open_sftp() 

mpin=22
tpin=23
servo_pin = 17 
GPIO.setmode(GPIO.BCM)
cap=0.000001
adj=2.130620985
i=0
t=0
GPIO.setwarnings(False)

#Ajuste estes valores para obter o intervalo completo do movimento do servo
deg_0_pulse   = 0.5 
deg_180_pulse = 2.5
f = 50.0

# Faca alguns calculos dos parametros da largura do pulso
period = 1000/f
k      = 100/period
deg_0_duty = deg_0_pulse*k
pulse_range = deg_180_pulse - deg_0_pulse
duty_range = pulse_range * k

#Iniciar o pino gpio
GPIO.setup(servo_pin,GPIO.OUT)
pwm = GPIO.PWM(servo_pin,f)
pwm.start(0)

#Define os pinos dos leds como saida
GPIO.setup(26, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)

def set_angle(angle):
	duty = deg_0_duty + (angle/180.0)* duty_range
	pwm.ChangeDutyCycle(duty)


while True:
    GPIO.setup(mpin, GPIO.OUT)
    GPIO.setup(tpin, GPIO.OUT)
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
    t=t+res
    if i==10:
		t=t/i
		if t > 3000:
			print "Acima do limiar"
			#deixa o motor em 0 graus
			GPIO.output(26, 0)
			GPIO.output(20, 0)
			GPIO.output(21, 0)
			GPIO.output(19, 0)
			set_angle(0)
		if t >= 0 and t <= 3000:
			
						
			if t >= 0 and t <= 750:
				
				print(t)
				ftp_client.put('/home/raspberry/Documentos/led3.txt', '/home/joab/Documentos/ledVerde.txt') 
				GPIO.output(21, 1)
				GPIO.output(26, 0)
				GPIO.output(20, 0)
				GPIO.output(19, 0)
				set_angle(180)
				
			if t > 750 and t <= 1500:
				
				print(t)
				ftp_client.put('/home/raspberry/Documentos/led2.txt', '/home/joab/Documentos/ledAmarelo.txt')
				GPIO.output(20, 1)
				GPIO.output(26, 0)
				GPIO.output(21, 0)
				GPIO.output(19, 0)
				set_angle(135)
				
			if t > 1500 and t <= 2250:
				
				print(t)
				ftp_client.put('/home/raspberry/Documentos/led1.txt', '/home/joab/Documentos/ledVermelho.txt') 
				GPIO.output(26, 1)
				GPIO.output(20, 0)
				GPIO.output(21, 0)
				GPIO.output(19, 0)
				set_angle(90)
				
			if t > 2250 and t <= 3000:
				
				print(t)
				ftp_client.put('/home/raspberry/Documentos/led4.txt', '/home/joab/Documentos/ledBranco.txt') 
				GPIO.output(19, 1)
				GPIO.output(20, 0)
				GPIO.output(21, 0)
				GPIO.output(26, 0)
				set_angle(45)
		i=0
		t=0
	
