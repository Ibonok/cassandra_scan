# cassandra_scan
> Dump Apache cassandra database

Define an Apache cassandra host and list all keyspaces, tables and data.    
# Installation

```
git clone https://github.com/Ibonok/cassandra_scan.git
cd cassandra_scan

virtualenv .
source bin/activate
pip install -r requirements.txt

Note: Building cassandra-drive takes some time!
```

> Donate: (ETH) 0x489B56bA505F88a054893d5BdE2c8b35f4A33FAb

# Usage

```
python cassandra_scan.py --help                    
usage: cassandra_scan.py [-h] [-k [KEYSPACES]] [-i [INFO]] [-d [DUMP]] [-t [TIMEOUT]] [-l [LIMIT]] [-s [IGNORESYSTEMKEYSPACES]] [--ip [IP]] [-f [FILENAME]]

Dump Apache cassandra databases. Default port 9042 hardcoded!

optional arguments:
  -h, --help            show this help message and exit
  -k [KEYSPACES], --keyspaces [KEYSPACES]
                        Show all keyspaces, Default = True
  -i [INFO], --info [INFO]
                        Show cassandra version and additional informations, Default = True
  -d [DUMP], --dump [DUMP]
                        Dump data from all keyspaces, Default = False
  -t [TIMEOUT], --timeout [TIMEOUT]
                        Connection Timeout, Default = 3s
  -l [LIMIT], --limit [LIMIT]
                        Lines to dump, Default = 1
  -s [IGNORESYSTEMKEYSPACES], --ignoresystemkeyspaces [IGNORESYSTEMKEYSPACES]
                        Ignore system keyspaces, Default = False
  --ip [IP]             Target IP:PORT
  -f [FILENAME], --filename [FILENAME]
                        File with IP:PORT
```

# Example
> Connect to Apache Cassandra and get all keyspaces

```
➜  ~ python3 cassandra_scan.py --ip 127.0.0.1                  
Version: 3.4.4 | cluster_name: testcluster | listen_address: 127.0.0.1 | broadcast_address: 127.0.0.1 | native_protocol_version: 4


Schema: system_auth
Tables: ['resource_role_permissons_index', 'role_members', 'role_permissions', 'roles']
Columns: ['resource', 'role', 'role', 'member', 'role', 'resource', 'permissions', 'role', 'can_login', 'is_superuser', 'member_of', 'salted_hash']


Schema: system_schema
Tables: ['aggregates', 'columns', 'dropped_columns', 'functions', 'indexes', 'keyspaces', 'tables', 'triggers', 'types', 'views']
Columns: ['keyspace_name', 'aggregate_name', 'argument_types', 'final_func', 'initcond', 'return_type', 'state_func', 'state_type', 'keyspace_name', 'table_name', 'column_name', 'clustering_order', 'column_name_bytes', 'kind', 'position', 'type', 'keyspace_name', 'table_name', 'column_name', 'dropped_time', 'type', 'keyspace_name', 'function_name', 'argument_types', 'argument_names', 'body', 'called_on_null_input', 'language', 'return_type', 'keyspace_name', 'table_name', 'index_name', 'kind', 'options', 'keyspace_name', 'durable_writes', 'replication', 'keyspace_name', 'table_name', 'bloom_filter_fp_chance', 'caching', 'cdc', 'comment', 'compaction', 'compression', 'crc_check_chance', 'dclocal_read_repair_chance', 'default_time_to_live', 'extensions', 'flags', 'gc_grace_seconds', 'id', 'max_index_interval', 'memtable_flush_period_in_ms', 'min_index_interval', 'read_repair_chance', 'speculative_retry', 'keyspace_name', 'table_name', 'trigger_name', 'options', 'keyspace_name', 'type_name',
'field_names', 'field_types', 'keyspace_name', 'view_name', 'base_table_id', 'base_table_name', 'bloom_filter_fp_chance', 'caching', 'cdc', 'comment', 'compaction', 'compression', 'crc_check_chance', 'dclocal_read_repair_chance', 'default_time_to_live', 'extensions', 'gc_grace_seconds', 'id', 'include_all_columns', 'max_index_interval', 'memtable_flush_period_in_ms', 'min_index_interval', 'read_repair_chance', 'speculative_retry', 'where_clause']
```

> Dump one entry and ignore the system keyspaces
```
python3 cassandra_scan.py --ip 127.0.0.1 -d -s
Version: 3.4.4 | cluster_name: testcluster | listen_address: 127.0.0.1 | broadcast_address: 127.0.0.1 | native_protocol_version: 4


Schema: tracker
Tables: ['stat_table1', 'stat_table2']
Columns: ['mch_id', 'device_id', 'date', 'key', 'offgas', 'mch_id', 'device_id', 'date', 'key', 'spot']
Data: Row(mch_id=4544, device_id='3243423', date='', key='1024', spot=[t_spot(lng=0.0, lat=0.0, amaplng=0.0, amaplat=0.0, direction=0, pt_time='', speed=0.0, altitude=0, temperature=33, pressure=0, bdlng=None, bdlat=None, pressure1=None), t_spot(lng=0.0, lat=0.0, amaplng=0.0, amaplat=0.0, direction=0, pt_time='', speed=0.0, altitude=0, temperature=33, pressure=0, bdlng=None, bdlat=None, pressure1=None), t_spot(lng=xx.xx, lat=xx.xx, amaplng=xx.xx, amaplat=xx.xx, direction=89, pt_time='', speed=7.0, altitude=89, temperature=33, pressure=0, bdlng=None, bdlat=None, pressure1=None), t_spot(lng=xx.xx, lat=xx.xx, amaplng=xx.xx, amaplat=xx.xx, direction=129, pt_time='', speed=20.0, altitude=86, temperature=33, pressure=0, bdlng=None, bdlat=None, pressure1=None)])
```

# Additional

Ignore the warnings :-)
