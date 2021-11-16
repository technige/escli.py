# Escli

Escli is a tool for interacting with an Elasticsearch service via the command line.

It began as an experimental side project during November 2021, implementing a limited set of functionality.
It is currently considered prototypical, and not suitable for production use.


## Usage

### Quick Example

```bash
$ export ES_PASSWORD=XXXXXXXXXXXXXXXXXXXX
$ escli search kibana_sample_data_flights -f github -i "FlightNum,OriginAirportID,DestAirportID" -n 15
Got 10000 Hits:
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

### Authentication

The `escli` tool relies on credentials supplied through environment variables.
The following list of variable are accepted:
- `ES_USER` - the Elasticsearch user name (default = `elastic`)
- `ES_PASSWORD` - the Elasticsearch password (no default)

If no password is available, `escli` assumes no HTTP auth is intended, and connects without.


### Search

A search can be performed using the `escli search` command.


### Version

The version of `escli` can be shown using the `escli version` command.
