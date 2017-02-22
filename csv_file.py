import csv

class Loans:
    """This class processes CSV input files"""

    # Dict to hold CSV data
    data = None

    # Header information
    header = None

    MSISDN = 'MSISDN'
    NETWORK = 'Network'
    DATE = 'Date'
    PRODUCT = 'Product'
    AMOUNT = 'Amount'

    #These are the initial assignment values for header indices
    msisdn = -1
    network = -1
    date = -1
    product = -1
    amount = -1

    def __init__(self):
        self.data = {}

    def read_input(self, filename):
        """Reads an input CSV and processes the rows

        :param filename: The file to be read in.
        NB We're making some assumptions here around the file being a reliable, stable format.
        For example, specifying a single-quote character when reading the CSV. The chances are
        that input files are being generated automatically, so should be consistent, but we'd
        want to test this assumption by looking at real data coming out of production systems.
        """
        # Read CSV file
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile, quotechar="'")
            for row in reader:
                if self.header is None:
                    self.header = row
                    self._index_headers(row)
                else:
                    self._process_row(row)

    def _index_headers(self, header):
        """This method processes the indices of the headers. These are the
            various categories of the data we ought to get from the csv file.
            This is also how different data is categorised in the csv.

        Args:
            header: This is any instance in first row of the csv that is mainly
            used to sub-class and categorise the data.

        """
        for i in range(0, len(header)):
            if self.header[i] == self.MSISDN:
                self.msisdn = i
            elif self.header[i] == self.NETWORK:
                self.network = i
            elif self.header[i] == self.DATE:
                self.date = i
            elif self.header[i] == self.PRODUCT:
                self.product = i
            elif self.header[i] == self.AMOUNT:
                self.amount = i
            #print(repr(i) + " - " + repr(self.header[i]))

        # NB we could raise a value error here if any of the heading indices
        # have not been updated from -1

    def _process_row(self, row):
        """ This method processes data for any given row of the csv file.
            The data is sorted and aggregated to specifc groups. The method checks for the
            of existence of a given data and adds it to a dictionary item.

            The number of occurence of a specific type is then counted and updated.abs
            The total amount for all loans for a specified category i.e network, date(month) e.t.c
            is calculated and the total value obtained

            Args:
                row

        """

        # Extract the values from the row
        network = row[self.network]
        product = row[self.product]
        date = row[self.date]
        month =date[3:6]
        amount = row[self.amount]

        # Ensure the Dict has the necessary entries
        if network not in self.data:
            self.data[network] = {}
        if product not in self.data[network]:
            self.data[network][product] = {}
        if month not in self.data[network][product]:
            self.data[network][product][month] = {"count": 0, "total": 0}

        # Update count and total
        self.data[network][product][month]["count"] += 1
        self.data[network][product][month]["total"] += int(float(amount))

    def count(self, network, product, month):
        """ This method is supposed to count the number of occurence a given
            loan loan occurs in a specific network and month

            Args:
                network
                product
                month

            Returns:
                returns the count instances a given parameter has occured
        """
        count = 0
        if network in self.data:
            if product in self.data[network]:
                if month in self.data[network][product]:
                    count = self.data[network][product][month]["count"]
        return count

    def total(self, network, product, month):
        """ This method counts the total amount of loan for any given set of
            parameters. e.g Total amount for network 1


            Args:
                network: give data on all loan amounts for any given network
                product: give data on all loan amounts for any given product type
                month: give data on all loan amounts for any given month

            Returns:
                returns the total loan amount for instances of any given parameter
        """
        total = 0
        if network in self.data:
            if product in self.data[network]:
                if month in self.data[network][product]:
                    total = self.data[network][product][month]["total"]
        return total


if __name__ == '__main__':

    loan = Loans()
    loan.read_input("Loans.csv")

    with open('Output.csv', 'w') as output_file:
        for network in loan.data:
            for product in loan.data[network]:
                for month in loan.data[network][product]:
                    record = loan.data[network][product][month]
                    total = record["total"]
                    count = record["count"]
                    print(network + ", " + product + ", " + month + ": total=" + str(total) + " count=" + str(count), file=output_file)
