from scapy.all import *
from scapy.layers.inet import IP, TCP, ICMP


async def syn_scan(ctx, target, ports):
    sport = RandShort()
    for port in ports:
        pkt = sr1(IP(dst=target) / TCP(sport=sport, dport=port, flags="S"), timeout=1, verbose=0)
        if pkt is not None:
            if pkt.haslayer(TCP):
                if pkt[TCP].flags == 20:
                    sys.stdout.write("~")
                elif pkt[TCP].flags == 18:
                    print('Opened :: %s:%s' % (target, port))
                    await ctx.send("> ◽ Port: `%s`\tState: `%s`" % (port, 'Opened'))
                else:
                    sys.stdout.write('#')
            elif pkt.haslayer(ICMP):
                sys.stdout.write('&')
            else:
                sys.stdout.write("?")
        else:
            sys.stdout.write(".")
