import mido
out_port = 'CircuitPlayground Express:CircuitPlayground Express Circu 32:0'

cpOut = mido.open_output(out_port)
#linuxOut = mido.open_output('Midi Through:Midi Through Port-0 14:0')

# system real time messages
cpOut.send(mido.Message('clock'))
cpOut.send(mido.Message('start'))
cpOut.send(mido.Message('continue'))
cpOut.send(mido.Message('stop'))
cpOut.send(mido.Message('active_sensing'))
cpOut.send(mido.Message('reset'))
# system common messages
cpOut.send(mido.Message('tune_request'))

cpOut.send(mido.Message('note_on', channel=0, note=64, velocity=127))
cpOut.send(mido.Message('polytouch', channel=0, note=48))
cpOut.send(mido.Message('note_off', channel=0, note=64, velocity=0))

