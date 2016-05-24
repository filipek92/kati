# kati - card system

Kati is access system developed for [club Buben](http://www.buk.cvut.cz) of [CTU Student Union](http://su.cvut.cz).

Authentication and authorization is performed by these steps:

1. user attaches identification card to reader located near the door
2. reader parses identification of the card
3. authorization request is send to IS to perform authorization and authentication
3. access to the door is granted or rejected according to reply from IS server

[RaspberryPi](https://www.raspberrypi.org/) is used as remote controller located near the door.

## Deployment

Assuming you have working SSH key-based login to hosts:

```sh
cd deploy
vim hosts # edit according to your needs
ansible-playbook deploy.yml
```

## Testing

SSH to a testing Raspberry and run:

```sh
cd ~/kati
python3 -m kati
```

You can also try only specific components:

```sh
python3 -m kati.reader
python3 -m kati.lock
```

Or run tests (which are heavily WIP):

```sh
python3 -m nose
```

## Developers

- [Pavel Trutman](https://github.com/PavelTrutman)
- [Tomáš Bedřich](https://github.com/tomasbedrich)
- [Tomáš Kukrál](https://github.com/tomkukral)
