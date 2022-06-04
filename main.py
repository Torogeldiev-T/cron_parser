import sys
from cron_parser import Cron

parser = Cron(sys.argv[1])
parser.parse()
parser.dislpay()
