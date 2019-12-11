#!/usr/bin/python3
############
# @Author Ibonok
#
# Dump Apache Cassandra Databases
#
# Do not use this in productiv enviroments.
# For educational use only. 
# 
############ 

from colorama import init, Fore, Style
from cassandra import ConsistencyLevel
#from cassandra.cluster import Cluster
from cassandra import cluster
from cassandra import metadata 

import os, errno, sys, logging, pprint, socket
import argparse

def getVersion ( session):
    rows = session.execute ("SELECT cql_version, cluster_name, listen_address, broadcast_address, native_protocol_version FROM system.local")

    for row in rows:
        print ( Fore.BLUE + Style.BRIGHT + 'Version: ' + Style.RESET_ALL + row[0], end=' | ')
        print ( Fore.BLUE + Style.BRIGHT + 'cluster_name: ' + Style.RESET_ALL + row[1], end=' | ')
        print ( Fore.BLUE + Style.BRIGHT + 'listen_address: ' + Style.RESET_ALL + row[2], end=' | ')
        print ( Fore.BLUE + Style.BRIGHT + 'broadcast_address: ' + Style.RESET_ALL + row[3], end=' | ')
        print ( Fore.BLUE + Style.BRIGHT + 'native_protocol_version: ' + Style.RESET_ALL + row[4])

def connectCassandra ( ip):
    try:
        connection = cluster.Cluster([ip])
        session = connection.connect()
        return connection, session
    except Exception:
        logging.exception(Fore.RED + "Connection failed:")
        return None, None

def disconnectCassandra ( connection):
    connection.shutdown()

def getRowEntries (session, keyspace, table, limit):
    tablerow = []
    try:
        tablerow = session.execute ("SELECT * FROM " + keyspace + "." + table + " LIMIT " + str(limit))
        return tablerow
    except Exception:
        logging.exception(Fore.RED + "Operation failed:")

def getMetaData ( connection, session, dump, limit, ignoresystemkeyspaces):
    meta = connection.metadata
    pp = pprint.PrettyPrinter(indent=1, compact=True, width=1000)
    for keyspace in meta.keyspaces:
        if ignoresystemkeyspaces and keyspace.startswith('system'):
            continue
        else:
            print ('\n')
            print ( Fore.BLUE + Style.BRIGHT + 'Schema: ' + Style.RESET_ALL + keyspace)
        tables = []
        columns = []
        for table in meta.keyspaces[keyspace].tables:
            if ignoresystemkeyspaces and keyspace.startswith('system'):
                continue
            else:
                tables.append( table)
                for column in meta.keyspaces[keyspace].tables[table].columns:
                    columns.append( column)
                if dump:
                    tablerow = getRowEntries( session, keyspace, table, limit)

        print ( Fore.BLUE + Style.BRIGHT + 'Tables: ' + Style.RESET_ALL, end='')
        pp.pprint ( tables)
        print ( Fore.BLUE + Style.BRIGHT + 'Columns: ' + Style.RESET_ALL, end='')
        pp.pprint ( columns)
        if dump:
            print ( Fore.BLUE + Style.BRIGHT + 'Data: ' + Style.RESET_ALL, end='')
            if tablerow:
                for row in tablerow:
                    pp.pprint ( row)
            else:
                print ('Can not get any data from table')

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def check_args ():
    init(autoreset=True)
    pars = argparse.ArgumentParser(description=Fore.GREEN + Style.BRIGHT + 'Dump Apache cassandra databases. Default port 9042 hardcoded!' + Style.RESET_ALL)

    pars.add_argument('-k', '--keyspaces', nargs='?', type=str2bool, default=True, const=True, help='Show all keyspaces, Default = True')
    pars.add_argument('-i', '--info', nargs='?', type=str2bool, default=True, const=True, help='Show cassandra version and additional informations, Default = True')
    pars.add_argument('-d', '--dump', nargs='?', type=str2bool, default=False, const=True, help='Dump data from all keyspaces, Default = False')
    pars.add_argument('-t', '--timeout', nargs='?', type=int, default=3, help='Connection Timeout, Default = 3s')
    pars.add_argument('-l', '--limit', nargs='?', type=int, default=1, help='Lines to dump, Default = 1')
    pars.add_argument('-s', '--ignoresystemkeyspaces', nargs='?', type=str2bool, default=False, const=True, help='Ignore system keyspaces, Default = False')

    pars.add_argument('--ip', nargs='?', help='Target IP:PORT')
    pars.add_argument('-f', '--filename', nargs='?', help='File with IP:PORT')

    args = pars.parse_args()

    if args.ip is None and args.filename is None:
        pars.error(Fore.RED + '-f/--filename or --ip required')        
    elif args.ip and args.filename is None: 
        return args.ip, True, args.info, args.keyspaces, args.dump, args.timeout, args.limit, args.ignoresystemkeyspaces
    elif args.ip is None and args.filename: 
        return args.filename, False, args.info, args.keyspaces, args.dump, args.timeout, args.limit, args.ignoresystemkeyspaces
    elif args.ip and args.filename: 
        pars.error(Fore.RED + 'To many Parameters, please choose -f/--filename or --ip')

def single_ip(ip, info, keyspaces, dump, timeout, limit, ignoresystemkeyspaces):
    if isOpen(ip, 9042, timeout):
        (connection, session) = connectCassandra ( ip)
        if connection:
            if info:
                getVersion ( session)
            if keyspaces:
                getMetaData ( connection, session, dump, limit, ignoresystemkeyspaces)
        else:
            sys.exit()
    else:
        sys.exit()

def input_file(filename, info, keyspaces, dump, timeout, limit, ignoresystemkeyspaces):
    file = open (filename, 'r')
    for ip in file:
        print (ip)
        if isOpen(ip.strip('\n'), 9042, timeout):
            (connection, session) = connectCassandra ( ip.strip('\n'))
            if connection:
                if info:
                    getVersion ( session)
                if keyspaces:
                    getMetaData ( connection, session, dump, limit, ignoresystemkeyspaces)
            
def isOpen( ip, port, timeout):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.settimeout(int(timeout))
        s.connect((ip, int(port)))
        s.shutdown(2)
        return True
    except:
        print (Fore.RED + "Port is not open")
        return False

if __name__ == "__main__":
    try:
        (value, typ, info, keyspaces, dump, timeout, limit, ignoresystemkeyspaces) = check_args()
        if typ:
            single_ip(value, info, keyspaces, dump, timeout, limit, ignoresystemkeyspaces)
        else:
            input_file(value, info, keyspaces, dump, timeout, limit, ignoresystemkeyspaces) 
    except KeyboardInterrupt:
        sys.exit()
