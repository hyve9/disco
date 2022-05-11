# Disco

### Build public server

`make run-ngrok`

### Show QR code

`make show-qr`

### Print server location

`make print-ngrok`

### Cleanup

`make cleanup`

## Troubleshooting

If `disco-player.py` is hanging or not working, try modifying your JACK server settings. First, make sure your ALSA settings are from ALSA -> JACK (plugin), and not set up to use PulseAudio bridging. Second, make sure to prepend it with `pasuspender -- disco-player.py <file>`.
