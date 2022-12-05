#/bin/env python3
"""
Script to update vaulted keys with random values
"""

import yaml
import string
import secrets
from re import search
from os import walk, getcwd, path
import logging
from getpass import getpass

import click
from ansible_vault import Vault


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
DEFAULT_CFG = 'config.ini'


def genpwd(password_length):
    alphabet = string.ascii_letters + string.digits
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(password_length))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and sum(c.isdigit() for c in password) >= 3):
            break
    return password


def update_entry(vault, fpath, key_values, password_length, confirm, check):
    for key in key_values:
        new_password = genpwd(password_length)
        data_vault = vault.load(open(fpath).read())

        try:
            logging.info(f"Change {data_vault[key]} to {new_password} in {fpath}")
            data_vault[key] = new_password
        except KeyError:
            logging.info(f"{key}, not in {fpath}")
            continue
        # Update vault file
        if not check:
            if confirm:
                answer = "unknown"
                while answer.lower() not in ["yes", "y", "no", "n", ""]:  
                    answer = input("Confirm change ? [Y/n]")
                if answer.lower() in ["n", "no"]:
                    continue

            vault.dump(data_vault, open(fpath, 'w'))

def walk_directory(vault, directory, key_values, password_length, confirm, check):
    for dname, dirs, files in walk(directory): 
        for fname in files:
            if search(r'vault\b', fname.lower()): 
                fpath = path.join(dname, fname)

                update_entry(vault, fpath, key_values, password_length, confirm, check)


@click.command()
@click.option('-k', '--key-values', multiple=True, help='Keys to update on vault')
@click.option('-d', '--directory', default=getcwd(), help ='Path to the directory.', show_default=True)
@click.option('-l', '--password-length', type=int, default=20, help='numbers of characters for the generated password.', show_default=True)  
@click.option('--check', is_flag=True, help='Do nothing just print what would be done')
@click.option('--confirm', is_flag=True, help='Always ask confirmation before updating passwords')
def main(directory, key_values, password_length, confirm, check):
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    if not key_values:
        ctx = click.get_current_context()
        click.echo(ctx.get_help())
        ctx.fail("At least one --key-values should be used")

    vault_password = getpass(prompt="Vault password: ")

    vault = Vault(vault_password)

    walk_directory(vault, directory, key_values, password_length, confirm, check)

if __name__=="__main__":
    logger = logging.getLogger('cluster-users')

    main()
