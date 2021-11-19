# Escli

Escli is a tool for interacting with an Elasticsearch service via the command line.

It began as an experimental side project during November 2021, implementing a limited set of functionality.
It is currently considered prototypical, and not suitable for production use.


## Installation

To install `escli` in the current virtualenv or for the entire system, simply use `pip`:

```bash
$ pip install escli
```

To instead install just for the current user, include the `--user` option:

```bash
$ pip install --user escli
```


## Basic Usage

### Quick Example

```bash
$ export ES_PASSWORD=XXXXXXXXXXXXXXXXXXXX
$ escli search kibana_sample_data_flights -f github -i "FlightNum,OriginAirportID,DestAirportID" -n 15
| FlightNum   | DestAirportID   | OriginAirportID   |
|-------------|-----------------|-------------------|
| 9HY9SWR     | SYD             | FRA               |
| X98CCZO     | VE05            | CPT               |
| UFK2WIZ     | VE05            | VE05              |
| EAYQW69     | TV01            | NA01              |
| 58U013N     | XIY             | AICM              |
| XEJ78I2     | GE01            | CYEG              |
| EVARI8I     | ZRH             | ZRH               |
| 1IRBW25     | YOW             | RM12              |
| M05KE88     | HYD             | MI11              |
| SNI3M1Z     | TV01            | SVO               |
| JQ2XXQ5     | HEL             | ABQ               |
| V30ITD0     | VIE             | VE05              |
| P0WMFH7     | PVG             | AICM              |
| VT9O2KD     | YOW             | NA01              |
| NRHSVG8     | SJU             | RM12              |
```

### Connectivity & Authentication

The `escli` tool relies on connection details and credentials supplied through environment variables.
The following list of variable are accepted:
- `ES_HOST` - one or more host names to which to connect; multiple hosts can be separated by commas and a port number can be appended after a colon (e.g. `a.example.com:8888,b.example.com:9999`)
- `ES_USER` - user name for HTTP auth (default = `elastic`)
- `ES_PASSWORD` - password for HTTP auth (no default)

If no password is available, `escli` assumes no HTTP auth is intended, and connects without.


### Version

The version of `escli` can be shown using the `escli version` command.


### Verbosity

Verbosity can be increased using the `-v` command line option and decreased using the `-q` option.
This can be passed multiple times (e.g. `-vv`) for a higher level of detail with each `v` or `q` increasing or decreasing the level respectively.
Any `-v` and `-q` options passed must be included _before_ the command, i.e. `escli -v COMMAND ARGS...`

The table below shows the available verbosity levels and the options required to select each.
Verbosity level zero is the default and does not require any explicit options to be passed.
Note that critical errors cannot be hidden.

| Verbosity    | Options | DEBUG | INFO  | WARNING | ERROR | CRITICAL |
| :----------: | :-----: | :---: | :---: | :-----: | :---: | :------: |
| +2           | `-vv`   | show  | show  | show    | show  | show     |
| +1           | `-v`    | hide  | show  | show    | show  | show     |
|  0           |         | hide  | hide  | show    | show  | show     |
| -1           | `-q`    | hide  | hide  | hide    | show  | show     |
| -2           | `-qq`   | hide  | hide  | hide    | hide  | show     |


## Searching

A search can be performed using the `escli search` command.
Each search operation requires a target index and search criteria in the form `FIELD=VALUE`.
Column selection and output format can also be tuned by command line options.

If no criteria are passed, a 'match_all' search will be carried out.
The example below searches the _kibana_sample_data_flights_ index, returning the _FlightNum_, _Origin_ and _Dest_ fields for the first 5 hits.

```bash
$ escli search -n=5 -i=FlightNum,Origin,Dest kibana_sample_data_flights
FlightNum    Origin                                          Dest
-----------  ----------------------------------------------  --------------------------------------------
9HY9SWR      Frankfurt am Main Airport                       Sydney Kingsford Smith International Airport
X98CCZO      Cape Town International Airport                 Venice Marco Polo Airport
UFK2WIZ      Venice Marco Polo Airport                       Venice Marco Polo Airport
EAYQW69      Naples International Airport                    Treviso-Sant'Angelo Airport
58U013N      Licenciado Benito Juarez International Airport  Xi'an Xianyang International Airport
```

This second example applies criteria to select only those results with "London" within the _OriginCityName_.

```bash
$ escli search -n=5 -i=FlightNum,Origin,Dest kibana_sample_data_flights OriginCityName=London
FlightNum    Origin                  Dest
-----------  ----------------------  -------------------------------------------------------
46J5N4Y      London Gatwick Airport  Ottawa Macdonald-Cartier International Airport
R0JFGVC      London Luton Airport    Stockholm-Arlanda Airport
X8NT4WO      London Gatwick Airport  New Chitose Airport
T0939V5      London Gatwick Airport  London Gatwick Airport
AGZPJJ3      London Luton Airport    Montreal / Pierre Elliott Trudeau International Airport
```


## Output Formats

Escli supports a number of different output formats for search results.
The `escli formats` command shows the full list of formats available.

```bash
$ escli formats
Output formats for search results:
  fancy_grid         fancy_outline      github             grid               
  html               jira               latex              latex_booktabs     
  latex_longtable    latex_raw          mediawiki          moinmoin           
  orgtbl             pipe               plain              presto             
  pretty             psql               rst                simple             
  textile            tsv                unsafehtml         youtrack           
```

This list includes all formats supported by [_tabulate_](https://pypi.org/project/tabulate/) which is used internally by Escli. 


## Ingestion

To ingest data, use the `escli ingest` command.
One or more JSON-formatted files can be supplied with the document content, or data can be read from _stdin_.

A simple import from _stdin_ might look like this:

```bash
$ echo '{"name": "Alice", "age": 33}' | escli -v ingest people
INFO: [elasticsearch] GET http://localhost:9200/ [status:200 request:0.002s]
INFO: [elasticsearch] POST http://localhost:9200/people/_doc [status:201 request:0.177s]
INFO: [escli.commands.ingest] Ingested JSON data from file '<stdin>' with result {...}
```

Whereas an import from a file would look like this:

```bash
$ escli -v ingest people bob.json
INFO: [elasticsearch] GET http://localhost:9200/ [status:200 request:0.002s]
INFO: [elasticsearch] POST http://localhost:9200/people/_doc [status:201 request:0.008s]
INFO: [escli.commands.ingest] Ingested JSON data from file 'bob.json' with result {...}
```

A quick search shows that the documents have been successfully ingested:

```bash
$ escli search people
name      age
------  -----
Alice      33
Bob        44
```

While JSON is the default format required for source data, the `-f` option allows for explicit selection of any one of the available formats, listed below:
- `json`
- `ndjson`


## Chaining Input and Output

Newline-delimited JSON ([ndjson](http://ndjson.org/)) is supported as both an input and an output format.
This allows data to be easily streamed out of one `escli` process and into another.

The example below extracts five documents from the _kibana_sample_data_flights_ index and feeds them directly into the _flights2_ index.

```bash
$ escli search kibana_sample_data_flights -n 5 -f ndjson | escli -v ingest flights2 -f ndjson
INFO: [elasticsearch] GET http://localhost:9200/ [status:200 request:0.002s]
INFO: [elasticsearch] POST http://localhost:9200/flights2/_doc [status:201 request:0.150s]
INFO: [escli.commands.ingest] Ingested JSON data from file '<stdin>', line 1 with result {...}
INFO: [elasticsearch] POST http://localhost:9200/flights2/_doc [status:201 request:0.005s]
INFO: [escli.commands.ingest] Ingested JSON data from file '<stdin>', line 2 with result {...}
INFO: [elasticsearch] POST http://localhost:9200/flights2/_doc [status:201 request:0.004s]
INFO: [escli.commands.ingest] Ingested JSON data from file '<stdin>', line 3 with result {...}
INFO: [elasticsearch] POST http://localhost:9200/flights2/_doc [status:201 request:0.004s]
INFO: [escli.commands.ingest] Ingested JSON data from file '<stdin>', line 4 with result {...}
INFO: [elasticsearch] POST http://localhost:9200/flights2/_doc [status:201 request:0.005s]
INFO: [escli.commands.ingest] Ingested JSON data from file '<stdin>', line 5 with result {...}
```

Note that `-f ndjson` is used for format selection for both the `search` and `ingest` processes.
