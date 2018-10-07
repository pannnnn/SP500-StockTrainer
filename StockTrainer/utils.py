from django.conf import settings

from influxdb import InfluxDBClient

import logging

logger = logging.getLogger(__name__)

sp500 = ["MMM", "ABT", "ABBV", "ABMD", "ACN", "ATVI", "ADBE", "AMD", "AAP", "AES", "AET", "AMG", "AFL", "A", "APD",
         "AKAM", "ALK", "ALB", "ARE", "ALXN", "ALGN", "ALLE", "AGN", "ADS", "LNT", "ALL", "GOOGL", "GOOG", "MO", "AMZN",
         "AEE", "AAL", "AEP", "AXP", "AIG", "AMT", "AWK", "AMP", "ABC", "AME", "AMGN", "APH", "APC", "ADI", "ANSS",
         "ANTM", "AON", "AOS", "APA", "AIV", "AAPL", "AMAT", "APTV", "ADM", "ARNC", "AJG", "AIZ", "T", "ADSK", "ADP",
         "AZO", "AVB", "AVY", "BHGE", "BLL", "BAC", "BK", "BAX", "BBT", "BDX", "BBY", "BIIB", "BLK", "HRB", "BA",
         "BKNG", "BWA", "BXP", "BSX", "BHF", "BMY", "AVGO", "BR", "CHRW", "CA", "COG", "CDNS", "CPB", "COF", "CAH",
         "KMX", "CCL", "CAT", "CBOE", "CBRE", "CBS", "CELG", "CNC", "CNP", "CTL", "CERN", "CF", "SCHW", "CHTR", "CVX",
         "CMG", "CB", "CHD", "CI", "XEC", "CINF", "CTAS", "CSCO", "C", "CFG", "CTXS", "CLX", "CME", "CMS", "KO", "CTSH",
         "CL", "CMCSA", "CMA", "CAG", "CXO", "COP", "ED", "STZ", "COO", "CPRT", "GLW", "COST", "COTY", "CCI", "CSX",
         "CMI", "CVS", "DHI", "DHR", "DRI", "DVA", "DE", "DAL", "XRAY", "DVN", "DLR", "DFS", "DISCA", "DISCK", "DISH",
         "DG", "DLTR", "D", "DOV", "DWDP", "DTE", "DRE", "DUK", "DXC", "ETFC", "EMN", "ETN", "EBAY", "ECL", "EIX", "EW",
         "EA", "EMR", "ETR", "EVHC", "EOG", "EQT", "EFX", "EQIX", "EQR", "ESS", "EL", "ES", "RE", "EXC", "EXPE", "EXPD",
         "ESRX", "EXR", "XOM", "FFIV", "FB", "FAST", "FRT", "FDX", "FIS", "FITB", "FE", "FISV", "FLT", "FLIR", "FLS",
         "FLR", "FMC", "FL", "F", "FTV", "FBHS", "BEN", "FCX", "GPS", "GRMN", "IT", "GD", "GE", "GIS", "GM", "GPC",
         "GILD", "GPN", "GS", "GT", "GWW", "HAL", "HBI", "HOG", "HRS", "HIG", "HAS", "HCA", "HCP", "HP", "HSIC", "HSY",
         "HES", "HPE", "HLT", "HFC", "HOLX", "HD", "HON", "HRL", "HST", "HPQ", "HUM", "HBAN", "HII", "IDXX", "INFO",
         "ITW", "ILMN", "IR", "INTC", "ICE", "IBM", "INCY", "IP", "IPG", "IFF", "INTU", "ISRG", "IVZ", "IPGP", "IQV",
         "IRM", "JEC", "JBHT", "SJM", "JNJ", "JCI", "JPM", "JNPR", "KSU", "K", "KMB", "KIM", "KMI", "KLAC", "KSS",
         "KHC", "KR", "LB", "LLL", "LH", "LRCX", "LEG", "LEN", "LLY", "LNC", "LKQ", "LMT", "L", "LOW", "LYB", "MTB",
         "MAC", "M", "MRO", "MPC", "MAR", "MMC", "MLM", "MAS", "MA", "MKC", "MCD", "MDT", "MRK", "MET", "MTD", "MGM",
         "KORS", "MCHP", "MU", "MSFT", "MAA", "MHK", "TAP", "MDLZ", "MCO", "MOS", "MSI", "MSCI", "MYL", "NDAQ", "NOV",
         "NKTR", "NTAP", "NFLX", "NWL", "NFX", "NEM", "NWSA", "NWS", "NEE", "NLSN", "NKE", "NI", "NBL", "JWN", "NSC",
         "NTRS", "NOC", "NCLH", "NRG", "NUE", "NVDA", "ORLY", "OXY", "OMC", "OKE", "ORCL", "PCAR", "PKG", "PH", "PAYX",
         "PYPL", "PNR", "PBCT", "PEP", "PKI", "PRGO", "PFE", "PCG", "PM", "PSX", "PNW", "PXD", "PNC", "RL", "PPG",
         "PPL", "PX", "PFG", "PG", "PGR", "PLD", "PRU", "PEG", "PSA", "PHM", "PVH", "QRVO", "PWR", "QCOM", "DGX", "RJF",
         "RTN", "O", "RHT", "REG", "REGN", "RF", "RSG", "RMD", "RHI", "ROK", "COL", "ROL", "ROP", "ROST", "RCL", "CRM",
         "SBAC", "SCG", "SLB", "STX", "SEE", "SRE", "SHW", "SPG", "SWKS", "SLG", "SNA", "SO", "LUV", "SPGI", "SWK",
         "SBUX", "STT", "SRCL", "SYK", "STI", "SIVB", "SYMC", "SYF", "SNPS", "SYY", "TROW", "TTWO", "TPR", "TGT", "TEL",
         "FTI", "TXN", "TXT", "TMO", "TIF", "TWTR", "TJX", "TMK", "TSS", "TSCO", "TDG", "TRV", "TRIP", "FOXA", "FOX",
         "TSN", "UDR", "ULTA", "USB", "UAA", "UA", "UNP", "UAL", "UNH", "UPS", "URI", "UTX", "UHS", "UNM", "VFC", "VLO",
         "VAR", "VTR", "VRSN", "VRSK", "VZ", "VRTX", "VIAB", "V", "VNO", "VMC", "WMT", "WBA", "DIS", "WM", "WAT", "WEC",
         "WCG", "WFC", "WELL", "WDC", "WU", "WRK", "WY", "WHR", "WMB", "WLTW", "WYNN", "XEL", "XRX", "XLNX", "XYL",
         "YUM", "ZBH", "ZION", "ZTS"]


def get_influxdb_client():
    """Returns an ``InfluxDBClient`` instance."""
    client = InfluxDBClient(
        settings.INFLUXDB_HOST,
        settings.INFLUXDB_PORT,
        settings.INFLUXDB_USERNAME,
        settings.INFLUXDB_PASSWORD,
        settings.INFLUXDB_DATABASE,
        timeout=getattr(settings, 'INFLUXDB_TIMEOUT', 10),
        ssl=getattr(settings, 'INFLUXDB_SSL', False),
        verify_ssl=getattr(settings, 'INFLUXDB_VERIFY_SSL', False),
    )
    return client


def query(client, stock_symbol):
    query = 'select "' + stock_symbol + '" from price;'
    print("Querying data: " + query)
    result = client.query(query, epoch='ms')
    print("Result: {0}".format(result))
    return result
