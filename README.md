#ZaraMining

##Execution

###Standalone (also verbose mode)

`python3 main.py fr homme jeans` or, for example, `python3 main.py en man jeans`

###Web service (Flask)

`python3 webapp.py` and you can access by [http://localhost:5000/api/en/man/jeans/](http://localhost:5000/api/en/man/jeans/) (same than previous example).

This Web service return a JSON object which will probably look like this (obviously more bigger).

```json
{
  "meta": {
    "lang": "en"
  },
  "content": [{
    "name": "DENIM TROUSERS WITH FAUX LEATHER DETAILS", 
    "color": {
      "name": "Mid-blue", 
      "value": "427"
    }, 
    "path": "download/en/man/jeans/0-DENIM TROUSERS WITH FAUX LEATHER DETAILS", 
    "url": "http://static.zara.net/photos//2013/I/0/2/p/0840/332/427/2/w/400/0840332427_6_1_1.jpg?timestamp=1377799652987"
  }]
}
```
`path` field is only useful in "download mode". This mode is activated by default on the standalone version but **NOT** in the Web app.
