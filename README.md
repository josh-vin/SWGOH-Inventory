# SWGOH Inventory

This is a little script I wrote that extracts the quantities of character shards and gear inventory in Star Wars Galaxy of Heroes from the C3PO bot. 

https://web.c3po.wtf/help

You must use these commands in order to allow C3PO to pull your inventory.json:
> /allycode add `XXXXXXXXX`
> /allycode auth `android/ea_connect`
> /inventory export 

Once you have the json, move the file into this directory and copy the file name into the quotes on line 5 
``` inventory_file = '' ```

This then pretifies the quantities into a csv named `inventory_output.csv` which has the exact "pretty" names of gear in the game. 

I copy and paste these values into another sheet where I reference csv export that I get from https://gear.swgohevents.com/. Then I can compare how many I am missing with how many are required.

I will update this README with a link to my Google Sheet I use for tracking soon. Feel free to reach out if you would like access to that sheet for tracking purposes. 

## Comlink
I am also referencing the [SWGOH Comlink API](https://github.com/swgoh-utils/swgoh-comlink) to check my roster's current star count so that I can calculate how many shards I have left on my spreadsheet. A valid API Url is needed for checking that on line 24
``` url = "" ```