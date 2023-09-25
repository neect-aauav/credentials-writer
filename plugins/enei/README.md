# ENEI Plugin - Credentials Writer

This plugin is meant to be used with the program [credentials-writer](https://github.com/neect-aauav/credentials-writer).

Some of the features of this plugin are:
- Always write only the first and last names for each person (even if more are provided in the file listing the names)
- Names that are too long are broken into two lines
- Generic credentials can be created for each tier

The tiers are: `[convidado, empresa, orador, organização, participante, voluntário]`

## Generic Credentials

To create generic credentials, with only the name of the tier, write the following in the list of names for that tier:
```
type=generic
times=100
```
Where `times` is the number of credentials to be created.

## Text Layout

```
-------------------
|                 |
|                 |
|                 |
|                 |
|                 |
|   PERSON NAME   |
|                 |
|       TIER      |
|                 |
|                 |
|                 |
-------------------
```