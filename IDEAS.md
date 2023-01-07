# granavi

Graph navigation ist ein Tool zur interaktiven Graph-Erstellung mit individueller Gewichtung.

Beispiel:

```

context <name> [<description>] # select context
node    <name> [<description>] # create node
connect <node-1> <node-2> [<atomic-nodes|nodes>]
        additional nodes are only for the connection

Atomic nodes (no creation needed):

2022-12-31   # date
31.12.2022   # date
14:30        # time
mo, monday   # weekday
13           # integer
3.3          # float
3h           # 3 hours
3min         # 3 minutes
3sec         # 3 seconds
3m           # 3 meter
3km          # 3 kilometer
bi           # bidirectional
"string"     # string
route        # rule is for all connections between nodes
disconnect   # rule disconnects all same connections (filter)
```

## Beispiele

```
context travel

node ubahn-16
node zufuß


context unterwegs

node Ubahn-Wesseling-Mitte
node Ubahn-Buschdorf
node Zuhause-Westring28

connect Ubahn-Wesseling-Mitte Ubahn-Buschdorf        bi 12min travel:ubahn-16
connect Zuhause-Westring28    Ubahn-Wesseling-Mitte  bi  7min travel:zufuß

route Zuhause-Westring28      Ubahn-Buschdorf

- Zuhause-Westring28
  -  7 min travel:zufuß
- Ubahn-Wesseling-Mitte
  - 12 min travel:ubahn-16
- Ubahn-Buschdorf

=> 19 min [zufuß, ubahn-16]

context westring28

node Treppenhaus
node Küche
node Flur
node Bad
node Schlafzimmer
node Samuel
node Wohnzimmer
node Balkon

connect Treppenhaus Flur Haustür
connect Flur Küche
connect Flur Bad
connect Flur Schlafzimmer
connect Flur Samuel
connect Flur Wohnzimmer
connect Wohnzimmer Balkon Balkontür
connect Samuel Balkon Fenster
connect Schlafzimmer Balkon Fenster

route Balkon Treppenhaus

- Balkon
  - Balkontür
- Wohnzimmer
- Flur
  - Haustür
- Treppenhaus

route Wohnzimmer unterwegs::Ubahn-Wesseling-Mitte

! Error !

connect Treppenhaus unterwegs::Zuhause-Westring28

route Wohnzimmer unterwegs::Ubahn-Wesseling-Mitte

@westring28
- Wohnzimmer
- Flur
  - Haustür
- Treppenhaus
@unterwegs
- Zuhause-Westring28
  -  7m zufuß
- Ubahn-Wesseling-Mitte

connect Wohnzimmer   objekte::Fenster   2
connect Wohnzimmer   objekte::Balkontür 1
connect Flur         objekte::Haustür   1
connect Schlafzimmer objekte::Fenster   1
connect Samuel       objekte::Fenster   1
connect Küche        objekte::Fenster   1


context objekte

node Fenster
node Balkontür
node Haustür

-

context unterwegs
connect Ubahn-Wesseling-Mitte Ubahn-Buschdorf \
    bi \                           # atomic node
	travel:ubahn-16                # node
	31.12.2022-01.01.2023 \        # atomic node
	"Ausfall auf der Strecke" \    # atomic node
	route \                        # atomic node
	disconnect                     # atomic node

```

### Beispiel Geschirr

```
context objekte::geschirr

node tassen
node gläser
node teller
node besteck

context räume::küche

node geschirrschrank
node geschirrspüler

connect objekte::geschirr::* geschirrschrank "sauber"
connect objekte::geschirr::* geschirrspüler "dreckig"
connect "dreckig" "sauber" geschirrspüler 1h


context objekte::geschirr

node kaffeetasse-1234
connect kaffeetasse-1234 "rot"
connect kaffeetasse-1234 räume::wohnzimmer
connect kaffeetasse-1234 "dreckig"

route kaffeetasse-1234 räume::küche::geschirrschrank

- kaffeetasse-1234
- räume::wohnzimmer
- räume::küche
- räume::küche::geschirrspüler
- "dreckig"
- 1h
- "sauber"
- räume::küche::geschirrschrank
```
