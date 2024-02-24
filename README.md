# Clictune-Api-Wrapper

Simple python package that uses the Clictune Api to do tasks.

## Install

install package using pip :
```
pip install pyClictune
```
## Example

```py
from pyClictune import Clictune
clictune = Clictune()

clictune.register()
# return mail and password of the created account


clictune.login('mail', 'password')
clictune.create_links(['https://discord.gg/DaEBWuYUUJ', 'https://joinplease.discord'], 10)
# create 10 link of each links and return a dict: {link: id}

clictune.delete_links(['65d9eed82ac5f245624381a4', '65d9eed82ac5f245624381a2'])


clictune.get_profit()
# return the money on the account

clictune.earn(['https://www.clictune.com/jzKI'])
```
