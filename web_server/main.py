try:
    import usocket as socket
except:
    import socket

response_404 = """HTTP/1.0 404 NOT FOUND

<h1>404 Not Found</h1>
"""

response_500 = """HTTP/1.1 500 Internal Server KeyError

<h1>500 Internal Server Error<h1>
"""

response_template = """HTTP/1.0 200 OK

{:s}
"""
import machine
from time import sleep
from machine import RTC, Pin


wled = Pin(13)
wled = machine.PWM(wled)
bled = Pin(2)
bled = machine.PWM(bled)
gled = Pin(5)
gled = machine.PWM(gled)
yled = Pin(12)
yled = machine.PWM(yled)
rled = Pin(4)
rled = machine.PWM(rled)
switch = Pin(10)

adc = machine.ADC(0)

def light_on():
    wled.value(1)

    body = """<html>
    <body>
    <p>The LED is on!</p>
    </body>
    </html>
    """

    return response_template.format(body)

def lights_off():
    for led in [wled, bled, yled, gled, rled]:
        led.duty(0)

    body = """<html>
    <body>
    <p>The LED is off!</p>
    </body>
    </html>
    """

    return response_template.format(body)

def switch_status():
    body = "{state: " + str(switch.value()) + "}"
    return response_template.format(body)

def light():
    body = "{value: " + str(adc.read()) + "}"
    return response_template.format(body)

def party_mode():
    body = "Let's get the party started!"
    leds = [wled, bled, yled, gled, rled]
    while True:
        for led in leds:
            led.duty(int(1.00679**adc.read()))
            sleep(0.05)
            print(int(1.00679**adc.read()))

        for led in leds:
            led.duty(0)
            sleep(0.05)

    return response_template.format(body)

def dummy():
    body = "This is a dummy endpoint"

    return response_template.format(body)

handlers = {
    'time': time,
    'dummy': dummy,
    'light_on': light_on,
    'lights_off': lights_off,
    'switch_status': switch_status,
    'light': light,
    'party_mode': party_mode,
}

def main():
    s = socket.socket()
    ai = socket.getaddrinfo("0.0.0.0", 8080)
    addr = ai[0][-1]

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind(addr)
    s.listen(5)
    print("Listening, connect your browser to http://<this_host>:8080/")

    while True:
        res = s.accept()
        client_s = res[0]
        client_addr = res[1]
        req = client_s.recv(4096)
        print("Request:")
        print(req)

        # The first line of a request looks like "GET /arbitrary/path/ HTTP/1.1".
        # This grabs that first line and whittles it down to just "/arbitrary/path/"

        try:
            # Given the path, identify the correct handler to use
            path = req.decode().split("\r\n")[0].split(" ")[1]
            handler = handlers[path.strip('/').split('/')[0]]
            response = handler()
        except KeyError:
            response = response_404
        except Exception as e:
            response = response_500
            print(str(e))

        # A handler returns an entire response in the form of a multi-line string.
        # This breaks up the response into single strings, byte-encodes them, and
        # joins them back together with b"\r\n". Then it sends that to the client.
        client_s.send(b"\r\n".join([line.encode() for line in response.split("\n")]))

        client_s.close()
        print()

main()
