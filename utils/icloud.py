from pyicloud import PyiCloudService

icloud = None

# initial icloud
def initIcloud(username, password):
	global icloud
	if not icloud:
		icloud = PyiCloudService(username, password)
		# two-factor authentication
		if icloud.requires_2fa:
			import click
			print "Two-factor authentication required. Your trusted devices are:"

			devices = icloud.trusted_devices
			for i, device in enumerate(devices):
				print "  %s: %s" % (i, device.get('deviceName',
			"SMS to %s" % device.get('phoneNumber')))

			device = click.prompt('Which device would you like to use?', default=0)
			device = devices[device]
			if not icloud.send_verification_code(device):
				print "Failed to send verification code"
				return False

			code = click.prompt('Please enter validation code')
			if not icloud.validate_verification_code(device, code):
				print "Failed to verify verification code"
				return False
	return True

