#!/usr/bin/python

"""
CPEN 431 group 1A's planet-lab CLI.

See `./pl-cli.py --help` for usage instructions.
"""

import argparse
import os
import subprocess
import sys


ANSIBLE_CMD = ("ansible-playbook -i {host} playbooks/{playbook}.yml "
               + "-u ubc_cpen431_1 --private-key={ssh_key} ")


def has_ansible():
    """Check if ansible is installed on this."""
    try:
        subprocess.call(["which", "ansible-playbook"])
        return True
    except:
        return False


def parse_args():
    parser = argparse.ArgumentParser(description="Planetlab CLI tool")
    parser.add_argument("command", help="[deploy|kill|start|getlogs]")

    # host args
    host_group = parser.add_mutually_exclusive_group()
    host_group.add_argument("--host_file",
                            help="Specify a path to the host file")
    host_group.add_argument("--host",
                            help="Specify a single hostname")

    # optional arguments
    parser.add_argument("--ssh_key", default="~/.ssh/id_rsa",
                        help="Specify an ssh key to use")
    parser.add_argument("--port", type=int,
                        help="Specify the server's port")
    parser.add_argument("--node_file_name", default="servers.txt",
                        help="What to call the node file. Default: servers.txt")

    args = parser.parse_args()

    # do some validation
    if args.host is None and args.host_file is None:
        parser.error("You need to specify the host(s).")

    if args.command in ["deploy", "start"] and args.host_file is None:
        parser.error("This command can only be run against a host file.")

    if args.command not in ["deploy", "kill", "start", "getlogs"]:
        parser.error("Unknown command. See ./pl-cli.py --help for options.")

    if args.command == "start" and args.port is None:
        parser.error("Specify the port number to run on.")

    return args


def create_nodes_txt(host_file, port, output_name):
    with open(host_file, "r") as hf:
        nodes = ["{}:{}".format(host.strip(), port)
                 for host in hf.readlines() if not host.isspace()]

    with open("deploy/{}".format(output_name), "w+") as nt:
        nt.write("\n".join(nodes))


def move_logs(host_file):
    print("Moving logs...")
    with open(host_file, "r") as hf:
        nodes = [x.strip() for x in hf.readlines() if not x.isspace()]

    for node in nodes:
        os.system("mv logs/{}/server.log logs/{}.log".format(node, node))
        os.system("rm -rf logs/{}".format(node))


if __name__ == "__main__":
    if not has_ansible():
        print("pl-cli requires ansible version 2.3.3.")
        print("You can install ansible using pip:")
        print("\tpip install -Iv ansible==2.3.3")
        sys.exit()

    args = parse_args()

    os.environ['ANSIBLE_HOST_KEY_CHECKING'] = 'False'

    if args.host is not None:
        host = "\"{},\"".format(args.host)
    elif args.host_file is not None:
        host = "\"./{}\"".format(args.host_file)

    os.system("export ANSIBLE_CONFIG=./ansible.cfg")

    cmd = ANSIBLE_CMD.format(host=host, playbook=args.command, 
                             ssh_key=args.ssh_key)

    if args.command == "start":
        create_nodes_txt(args.host_file, args.port, args.node_file_name)
        cmd += "--extra-vars \"port_num={}\"".format(args.port)

    if args.command == "getlogs":
        os.system("rm -rf logs && mkdir logs")

    os.system(cmd)

    if args.command == "getlogs" and args.host_file:
        move_logs(args.host_file)

    print("\n{}: done.".format(args.command))
