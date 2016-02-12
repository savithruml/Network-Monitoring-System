import datetime
import smtplib
from twilio.rest import TwilioRestClient
import config_fetch
import sys

def parse_data(input, time):

    out1 = open('/home/netman/traps/trapsinfo.log', 'a')

    if input.startswith('SNMPv2-MIB::snmpTrapOID.0 IF-MIB'):
        state = input.split(':')[-1]
        temp_time = str(datetime.datetime.now()).split('.')
        out1.write(temp_time[0] + ': ' + state.upper() + ' on ')


    elif input.startswith('IF-MIB::ifDescr'):
        info = input.split(' ')
        interface = info[-1]
        out1.write('INTERFACE: ' + interface + '\n')
        send_mail(interface)

    elif input.startswith('SNMPv2-MIB::snmpTrapOID.0 SNMPv2-SMI'):
        config_fetch


    else:
        pass



def send_mail(interface):

    sender_mail = 'test@gmail.com'
    receiver_mail = ['test1@gmail.com']
    content = open('/home/netman/traps/trapsinfo.log', 'r')
    data = content.read().strip('\n').split('\n')
    msg = """From: From SNMP Monitoring System <snmp@cisco.com>
To: Network Admins <admin@savilabs.com>
MIME-Version: 1.0
Content-type: text/html
Subject: IMPORTANT: INTERFACE CHANGE DETECTED

<h3><b>*** IMMEDIATE ATTENTION REQUIRED ***</b></h3>
<h2><font color="red">LINK CHANGE DETECTED</font></h2>
"""

    msg1 = '\n\n' + str(data[-1]) + interface
    message_twilio(msg1)

    try:
        smtp_session = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_session.ehlo()
        smtp_session.starttls()
        smtp_session.ehlo()
        smtp_session.login(sender_mail, '<password>')
        smtp_session.sendmail(sender_mail, receiver_mail, msg + msg1)
        smtp_session.quit()

    except smtplib.SMTPException:
        pass



def message_twilio(msg):

    sid = "<sid>"
    token = "<authtoken>"

    client = TwilioRestClient(sid, token)
    body = '\nIMMEDIATE ACTION REQUIRED' + '\n' + msg + '\n'
    msg1 = msg.split(':')[-1]
    msg2 = msg1.split(' ')
    msg3 = msg2[-1].split('/')



    url_msg = 'http://twimlets.com/message?Message%5B0%5D=ALL%20NETWORK%20ADMINISTRATORS%20IMMEDIATE%20ATTENTION%20REQUIRED&Message%5B1%5D=' + msg2[0] + '%20' + msg2[1] + '%20on%20' + msg3[0] +'%2F'+ msg3[1] + '&'

    client.messages.create(to = '<mobile number>', from_= '<twilio number>',
                            body=body,)

    call = client.calls.create(to='<mobile number>', from_='<twilio number>',
            url=url_msg, method='GET', fallback_method='GET',
            status_callback_method='GET', record='false')

    print call.sid

def main():

    running = True
    time = 'TRAP RECEIVED AT: ' + str(datetime.datetime.now())
    out = open('/home/netman/traps/traps.log', 'a')
    out.write('\n')
    out.write(time + '\n')

    while running:

        try:
            input = raw_input()
            parse_data(input, time)
            out.write(input + '\n')

        except EOFError:
            running = False

    out.close()


if __name__ == '__main__':
    main()
