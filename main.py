import sys
from cron_parser import Cron

parser = Cron(sys.argv[1])
print(len(sys.argv))
parser.parse()
parser.dislpay()
