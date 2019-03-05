Pared down planetlab CLI.

You can get a list of the current best nodes from the monitoring site, e.g.:

```
wget http://34.215.231.11/best/20
```

to fetch a list of the 20 best nodes.

## Commands

```
./pl-cli [deploy|kill|start|getlogs]
```

Optional arguments:
- `--host=host.name.tld`
- `--host_file=/path/to/hosts`
- `--ssh_key=/path/to/key`
- `--port=12345`

If no ssh_key is specified, the playbooks will try to use `~/.ssh/id_rsa`.

The `node_file_name` is generated when starting the server. By default, it is 
saved as `servers.txt`, but this can be overridden.

### Deploying new server binaries

**NOTE: The server binary and server configuration files must be saved in the `deploy` directory as `server.jar` and `server.properties`, respectively.**

Example command to deploy to all nodes in the file `servers.txt`:

```
./pl-cli deploy --host_file=servers.txt
```

This copies the `server.jar` and `server.properties` files from the 
`deploy` directory to the hosts listed in the file.

### Starting the servers

Example command to start servers on port 15151 on all nodes in `servers.txt`:

```
./pl-cli start --host_file=servers.txt --port=15151
```

This will start the server on all the nodes listed in the file `servers.txt`. 
This will kill any servers that were already running.

### Killing a server

Example command to kill servers on all nodes in the file `servers.txt`:

```
./pl-cli kill --host_file=./hosts
```

This will kill the server process on all the nodes listed in the file `servers.txt`,
if there is one running.
