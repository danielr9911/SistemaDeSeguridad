
import os, subprocess, time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

##from yowsup.layers.interface                           import YowInterfaceLayer                 #Reply to the message
##from yowsup.layers.interface                           import ProtocolEntityCallback            #Reply to the message
##from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity         #Body message
##from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity         #Body message
##from yowsup.layers.protocol_presence.protocolentities  import AvailablePresenceProtocolEntity   #Online
##from yowsup.layers.protocol_presence.protocolentities  import UnavailablePresenceProtocolEntity #Offline
##from yowsup.layers.protocol_presence.protocolentities  import PresenceProtocolEntity            #Name presence
##from yowsup.layers.protocol_chatstate.protocolentities import OutgoingChatstateProtocolEntity   #is writing, writing pause
##from yowsup.common.tools                               import Jid                               #is writing, writing pause

from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.auth import YowAuthenticationProtocolLayer
from yowsup.layers import YowLayerEvent, EventCallback
from yowsup.layers.network import YowNetworkLayer
import sys
from yowsup.common import YowConstants
import datetime
import os
import logging
from yowsup.layers.protocol_groups.protocolentities      import *
from yowsup.layers.protocol_presence.protocolentities    import *
from yowsup.layers.protocol_messages.protocolentities    import *
from yowsup.layers.protocol_ib.protocolentities          import *
from yowsup.layers.protocol_iq.protocolentities          import *
from yowsup.layers.protocol_contacts.protocolentities    import *
from yowsup.layers.protocol_chatstate.protocolentities   import *
from yowsup.layers.protocol_privacy.protocolentities     import *
from yowsup.layers.protocol_media.protocolentities       import *
from yowsup.layers.protocol_media.mediauploader import MediaUploader
from yowsup.layers.protocol_profiles.protocolentities    import *
from yowsup.common.tools import Jid
from yowsup.common.optionalmodules import PILOptionalModule, AxolotlOptionalModule
from yowsup.demos.cli.layer import YowsupCliLayer
from yowsup.demos.cli.cli import Cli, clicmd
import testcam
import registros
import commands
import os

name = "NAMEPRESENCE"

print "Bienvenido, ya puede empezar a escribir !"

class EchoLayer(YowInterfaceLayer):
    
    entro = False
    
    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        if messageProtocolEntity.getType() == 'text':
            time.sleep(0.5)
            self.toLower(messageProtocolEntity.ack()) #Set received (double v)
            time.sleep(0.5)
            self.toLower(PresenceProtocolEntity(name = name)) #Set name Presence
            time.sleep(0.5)
            self.toLower(AvailablePresenceProtocolEntity()) #Set online
            time.sleep(0.5)
            self.toLower(messageProtocolEntity.ack(True)) #Set read (double v blue)
            time.sleep(0.5)
            self.toLower(OutgoingChatstateProtocolEntity(OutgoingChatstateProtocolEntity.STATE_TYPING, Jid.normalize(messageProtocolEntity.getFrom(False)) )) #Set is writing
            time.sleep(1)
            self.toLower(OutgoingChatstateProtocolEntity(OutgoingChatstateProtocolEntity.STATE_PAUSED, Jid.normalize(messageProtocolEntity.getFrom(False)) )) #Set no is writing
            time.sleep(1)
            self.onTextMessage(messageProtocolEntity) #Send the answer
            time.sleep(1)
            self.toLower(UnavailablePresenceProtocolEntity()) #Set offline

    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        print entity.ack()
        self.toLower(entity.ack())

    def onTextMessage(self,messageProtocolEntity):
        namemitt   = messageProtocolEntity.getNotify() #Nombre del que envia
        message    = messageProtocolEntity.getBody() #Mensaje recibido
        recipient  = messageProtocolEntity.getFrom() #Numero del que envia
        textmsg    = TextMessageProtocolEntity
        numero = recipient[:12]
        self.para = recipient
        self.activada = False
        message = message.lower() #Pasar a minusculas

        print "Recibido: "+str(message)

        
        
        if message == 'hola raspberry':
            answer = "Hola " + namemitt
            self.toLower(textmsg(answer, to = recipient ))
            print answer

        elif message == 'registrar test 123':
            outfile = open('registros.txt', 'a')
            numero = recipient[:12]
            outfile.write(numero)
            outfile.write('\n')
            outfile.close()
            answer = "El numero " + numero + " se ha registrado exitosamente"
            self.toLower(textmsg(answer, to = recipient ))
            print answer

        elif message == 'estado':
            if registros.verificar(numero):
                answer = "Usted esta identificado"
            else:
                answer = "Usted no esta identificado"
            self.toLower(textmsg(answer, to = recipient ))
            print answer
        
        elif message == 'activar sistema':
            if registros.verificar(numero):
                testcam.camara()
                comando = 'sudo yowsup-cli demos -c config -me ' + numero + ' /home/pi/Documents/Conmutacion/yowsup/save/fotoLadron.png image && sudo python run.py'
                commands.getoutput(comando)
                answer = "Se encontro un intruso"
            else:
                answer = "Usted no se ha identificado"    
            self.toLower(textmsg(answer, to = recipient ))
            print answer

        elif message == 'tomar foto':
            if registros.verificar(numero):
                testcam.foto()
                numero = recipient[:12]
                comando = 'sudo yowsup-cli demos -c config -me ' + numero + ' /home/pi/Documents/Conmutacion/yowsup/save/fotoManual.png image && sudo python run.py'
                commands.getoutput(comando)
                print "Foto enviada"
            else:
                answer = "Usted no se ha identificado"
                self.toLower(textmsg(answer, to = recipient ))
                print answer

        elif message == 'sonar alarma':
            if registros.verificar(numero):
                answer = "La alarma se ha encendido"
                GPIO.output(16, True) # Pin 2 en alto

            else:
                answer = "Usted no se ha identificado"

            self.toLower(textmsg(answer, to = recipient ))
            print answer
            
        elif message == 'silenciar alarma':
            if registros.verificar(numero):
                answer = "La alarma se ha silenciado"
                GPIO.output(16, False) # Pin 2 en alto
            else:
                answer = "Usted no se ha identificado"
            
            self.toLower(textmsg(answer, to = recipient ))
            print answer


        elif message == 'encender luces':
            if registros.verificar(numero):
                answer = "La luz se ha encendido"
                GPIO.output(20, True) # Pin 2 en alto
                GPIO.output(21, True)
            else:
                answer = "Usted no se ha identificado"

            self.toLower(textmsg(answer, to = recipient ))
            print answer
            
        elif message == 'apagar luces':
            if registros.verificar(numero):
                answer = "La luz se ha apagado"
                GPIO.output(20, False) # Pin 2 en alto
                GPIO.output(21, False)
            else:
                answer = "Usted no se ha identificado"
            
            self.toLower(textmsg(answer, to = recipient ))
            print answer
            
        
        else:
            answer = "Comandos:\n- registrar <usuario> <password>\n- tomar foto\n- activar sistema\n- estado\n- sonar alarma\n- silenciar alarma\n- encender luces\n- apagar luces"
            self.toLower(textmsg(answer, to = recipient ))
            print answer
            print recipient
