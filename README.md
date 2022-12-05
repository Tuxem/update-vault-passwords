# update_vault_passwords
Python script to ate vaulted keys with random values.

## Dependencies

### Packages

* python

### Python module
* ansible-vault
* click

## Usage

```
$ ./update_vault_passwords.py -k vault_password_entry
Vault password:
INFO: Change CjgPZI2gMuk2UUqK0mr7 to 6OCwtyb0DI9CEHM7xlou in /home/tuxem/dev/update_vault_passwords/group_vars/databases/vault
INFO: Change GwfZEC01yLDW9KSL5Jks to 7xIiDui1mIoY0pHL1Pde in /home/tuxem/dev/update_vault_passwords/group_vars/webservers/vault.yml
INFO: Change qBmSpCfU7zsqOq1p3Jie to 24r1BEsv2tuR8vebNsXd in /home/tuxem/dev/update_vault_passwords/tests/host_vars/web01/vault.yml
```

Help command
```
$ ./update_vault_passwords.py --help
Usage: update_vault_passwords.py [OPTIONS]

Options:
  -k, --key-values TEXT          Keys to update on vault
  -d, --directory TEXT           Path to the directory.  [default:
                                 /home/emeric/dev/update_vault_passwords]
  -l, --password-length INTEGER  numbers of characters for the generated
                                 password.  [default: 20]
  --check                        Do nothing just print what would be done
  --confirm                      Always ask confirmation before updating
                                 passwords
  --help                         Show this message and exit.
```

