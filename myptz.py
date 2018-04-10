#! /usr/bin/env python
# -*- coding: utf-8 -*-
from onvif import ONVIFCamera
from time import sleep

print 'INIT'

mycam = ONVIFCamera('192.168.13.12', 80, 'admin', 'Supervisor', '/etc/onvif/wsdl/')

print 'Connected to ONVIF camera'
media = mycam.create_media_service()
print 'Created media service object'
media_profile = media.GetProfiles()[0]
token = media_profile._token

#image = mycam.create_imaging_service()
#reqi = image.create_type('SetImagingSettings')
#reqi.VideoSourceToken = media_profile.VideoSourceConfiguration.SourceToken
#reqi.Brightness = 50
#image.SetImagingSettings(reqi)


print 'Creating PTZ object'
ptz = mycam.create_ptz_service()

request = ptz.create_type('GetServiceCapabilities')
Service_Capabilities = ptz.GetServiceCapabilities(request)
print 'PTZ service capabilities:'
print Service_Capabilities

status = ptz.GetStatus({'ProfileToken':token})
print 'PTZ status:'
print status
print 'Pan position:', status.Position.PanTilt._x
print 'Tilt position:', status.Position.PanTilt._y
print 'Zoom position:', status.Position.Zoom._x

reqconmv = ptz.create_type('ContinuousMove')
reqconmv.ProfileToken = media_profile._token

requests = ptz.create_type('Stop')
requests.ProfileToken = media_profile._token

def stop():
        requests.PanTilt=True
        requests.Zoom=True
        ptz.Stop(requests)
        print 'Stopped'



print
stop()

def move(pan, tilt, zoom, velocity):
        print 'Start moving'
        reqconmv.Velocity.PanTilt._x = velocity
        reqconmv.Velocity.PanTilt._y = velocity
        reqconmv.Velocity.Zoom._x = velocity
        token = media_profile._token
	status = ptz.GetStatus({'ProfileToken':token})
        sig = 0.01
        print 'Pan position:', status.Position.PanTilt._x
        print 'Tilt position:', status.Position.PanTilt._y
        while abs(pan - status.Position.PanTilt._x) > sig  and abs(tilt - status.Position.PanTilt._y) > sig:
            if pan > status.Position.PanTilt._x:
                reqconmv.Velocity.PanTilt._x = velocity*0.9
                print 'going x'
            else:
                reqconmv.Velocity.PanTilt._x = -1*velocity*0.9
                print 'going -x'
            if tilt > status.Position.PanTilt._y:
                reqconmv.Velocity.PanTilt._y = velocity
                print 'going y'
            else:
                reqconmv.Velocity.PanTilt._y = -1*velocity
                print 'going -y'
            if abs(pan - status.Position.PanTilt._x) < sig:
                reqconmv.Velocity.PanTilt._x = 0
                break
            if abs(tilt - status.Position.PanTilt._y) < sig:
                reqconmv.Velocity.PanTilt._y = 0
                break
            if abs(zoom - status.Position.Zoom._x) < sig:
                reqconmv.Velocity.Zoom._x = 0
                break
            ptz.ContinuousMove(reqconmv)
            status = ptz.GetStatus({'ProfileToken':token})
            print 'Pan position:', status.Position.PanTilt._x
            print 'Tilt position:', status.Position.PanTilt._y
	    print 'Zoom position:', status.Position.Zoom._x
            print '-----------------------------------------------'
        stop()

move(0.85,0.3,0.7,0.5)

sleep(2)

