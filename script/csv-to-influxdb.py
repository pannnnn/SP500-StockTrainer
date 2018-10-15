import argparse
import csv
# from StockTrainer.utils import query
from influxdb import InfluxDBClient

host = "localhost"
port = 8086
user = ""
password = ""
dbname = "sp500"
measurement = "price"
batchSize = 1000


def isfloat(value):
    try:
        float(value)
        return True
    except:
        return False



def loadCsv(inputFile):
    client = InfluxDBClient(host, port, user, password, dbname)
    print('Deleting database %s' % dbname)
    client.drop_database(dbname)
    print('Creating database %s' % dbname)
    client.create_database(dbname)

    datapoints = []
    count = 0

    with open(inputFile, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            time = row["Date"]
            del row["Date"]

            fields = {key: float(value) if isfloat(value) else value for key, value in row.items()}
            point = {"measurement": measurement, "time": time, "fields": fields}
            datapoints.append(point)

            count += 1

            if len(datapoints) % batchSize == 0:
                print('Read %d lines' % count)
                print('Inserting %d datapoints...' % (len(datapoints)))
                response = client.write_points(datapoints)

                if response == False:
                    print('Problem inserting points, exiting...')
                    exit(1)

                print("Wrote %d, response: %s" % (len(datapoints), response))

                datapoints = []

    # write the rest
    if len(datapoints) > 0:
        print('Read %d lines' % count)
        print('Inserting %d datapoints...' % (len(datapoints)))
        response = client.write_points(datapoints)

        if response == False:
            print('Problem inserting points, exiting...')
            exit(1)

        print("Wrote %d, response: %s" % (len(datapoints), response))

    print('Done')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Csv to influxdb.')

    parser.add_argument('-i', '--input', nargs='?', required=True,
                        help='Input csv file.')

    args = parser.parse_args()
    loadCsv(args.input)
