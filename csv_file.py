class LoanAggregator:
   
    data = None

    # Header information
    header = None

    MSISDN = 'MSISDN'
    NETWORK = 'Network'
    DATE = 'Date'
    PRODUCT = 'Product'
    AMOUNT = 'Amount'

    msisdn = -1
    network = -1
    date = -1
    product = -1
    amount = -1

    def __init__(self):
        self.data = {}

    def read_input(self, filename):