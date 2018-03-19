# LDAP Authentication for Dash Apps

According to the Dash [documentation](https://dash.plot.ly/authentication), LDAP authentication is only supported with Plotly On-Premise. This repository contains a simple work-around for using LDAP with your non-paid Dash implementation.

The provided class `LDAPAuth` authenticates users by checking their log-in credentials against an LDAP server. The class is simply a modified version of Dash's [`BasicAuth`](https://github.com/plotly/dash-auth/blob/master/dash_auth/basic_auth.py) class, but instead of checking against a list of valid credentials, it checks whether they're valid according to LDAP.

To use this module, you'll need to edit 2 lines in the file (denoted with comments in the file) to specify the location of your active directory server, as well as the possible extension you want applied to the username. You'll also need to install [python-ldap](https://www.python-ldap.org/en/latest/index.html), dash_auth and its dependencies (and Dash of course).

You can invoke the LDAP authentication similar to this minimal example:

```py
import dash
from dash_ldap_auth import LDAPAuth

app = dash.Dash()
auth = LDAPAuth(app)
```
