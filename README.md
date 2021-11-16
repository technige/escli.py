# Escli

Escli is a tool for interacting with an Elasticsearch service via the command line.

It began as an experimental side project during November 2021, implementing a limited set of functionality.
It is currently considered prototypical, and not suitable for production use.


## Installation

To install `escli`, simply use `pip`:

```bash
$ pip install escli
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
- `ES_PASSWORD` - password for HTTP auth(no default)

If no password is available, `escli` assumes no HTTP auth is intended, and connects without.


### Version

The version of `escli` can be shown using the `escli version` command.


## Search

A search can be performed using the `escli search` command.
Each search operation requires a target index and the column selection and output format can be tuned by command line options.

### 'Match All' Search Queries

The simplest (and default) form of search is a basic 'match_all'.
The example below searches the _kibana_sample_data_flights_ index, returning the _FlightNum_, _Origin_ and _Dest_ fields for the first 5 hits.

```bash
$ escli search kibana_sample_data_flights -n 5 -i FlightNum,Origin,Dest
FlightNum    Origin                                          Dest
-----------  ----------------------------------------------  --------------------------------------------
9HY9SWR      Frankfurt am Main Airport                       Sydney Kingsford Smith International Airport
X98CCZO      Cape Town International Airport                 Venice Marco Polo Airport
UFK2WIZ      Venice Marco Polo Airport                       Venice Marco Polo Airport
EAYQW69      Naples International Airport                    Treviso-Sant'Angelo Airport
58U013N      Licenciado Benito Juarez International Airport  Xi'an Xianyang International Airport
```

### 'Match' Search Queries

A more selective query can be achieved using the `match` subcommand.
The example below selects only those results with "London" within the _OriginCityName_.

```bash
$ escli search kibana_sample_data_flights -n 5 -i FlightNum,Origin,Dest match OriginCityName=London
FlightNum    Origin                  Dest
-----------  ----------------------  -------------------------------------------------------
46J5N4Y      London Gatwick Airport  Ottawa Macdonald-Cartier International Airport
R0JFGVC      London Luton Airport    Stockholm-Arlanda Airport
X8NT4WO      London Gatwick Airport  New Chitose Airport
T0939V5      London Gatwick Airport  London Gatwick Airport
AGZPJJ3      London Luton Airport    Montreal / Pierre Elliott Trudeau International Airport
```

### 'Term' Search Queries

An exact match can be obtained using the `term` subcommand.
The example below looks for the exact value "Rain" in the _DestWeather_ field.

```bash
$ escli search kibana_sample_data_flights -n 5 -i FlightNum,Dest,DestWeather term DestWeather=Rain
FlightNum    Dest                                            DestWeather
-----------  ----------------------------------------------  -------------
9HY9SWR      Sydney Kingsford Smith International Airport    Rain
SNI3M1Z      Treviso-Sant'Angelo Airport                     Rain
JQ2XXQ5      Helsinki Vantaa Airport                         Rain
VT9O2KD      Ottawa Macdonald-Cartier International Airport  Rain
7SFSTEH      Narita International Airport                    Rain
```
