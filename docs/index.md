---
layout: home
---

***

## How to use on desktop
- Download the [fonts](http://textual.works/downloads/lankasymbols)
- Use the following chart to find the symbol you want to use and copy and paste the icon from TEXT column in the symbols chart.
- Or use the `Glyph` panel in your application to use any symbol.

## How to use on web (HTML)

Add following inside <head> and use the correct string from  HTML column in the symbols chart below.
```
<link rel="stylesheet" href="https://rawgit.com/textualworks/lankasymbols/master/fonts/webfonts/lankasymbols.css">
```

!IMPORTANT: This project is still in early development and things keep changing. Do not use for production websites.


## Symbols

| ICON                                | DESCRIPTION                  | UNICODE   |   HTML                                         | TEXT                                       |
| :---                                |:-----                 | :-----    | :--------------------------------------------  |:--------------------------------------------  |
| <i class="lks cross"></i> | cross |  `u+271D` |  `<i class="ls cross"></i>`| <span class="display-text">✝</span> |
| <i class="lks starAndCrescent"></i> | starAndCrescent |  `u+262A` |  `<i class="ls starAndCrescent"></i>`| <span class="display-text">☪</span> |
| <i class="lks wheelOfDharma"></i> | wheelOfDharma |  `u+2638` |  `<i class="ls wheelOfDharma"></i>`| <span class="display-text">☸</span> |
| <i class="lks lks-lkflaglion"></i> | lks-lkflaglion |  `u+EC7F` |  `<i class="ls lks-lkflaglion"></i>`| <span class="display-text"></span> |
| <i class="lks lks-flaglion-outline"></i> | lks-flaglion-outline |  `u+EC80` |  `<i class="ls lks-flaglion-outline"></i>`| <span class="display-text"></span> |
| <i class="lks lks-sls"></i> | lks-sls |  `u+EC82` |  `<i class="ls lks-sls"></i>`| <span class="display-text"></span> |
| <i class="lks lks-budusaranayi"></i> | lks-budusaranayi |  `u+EE94` |  `<i class="ls lks-budusaranayi"></i>`| <span class="display-text"></span> |
| <i class="lks lks-bulath"></i> | lks-bulath |  `u+F4D3` |  `<i class="ls lks-bulath"></i>`| <span class="display-text"></span> |
| <i class="lks lks-pahan"></i> | lks-pahan |  `u+F4D4` |  `<i class="ls lks-pahan"></i>`| <span class="display-text"></span> |
| <i class="lks lks-stupa"></i> | lks-stupa |  `u+F0B0` |  `<i class="ls lks-stupa"></i>`| <span class="display-text"></span> |
| <i class="lks lks-elephantL-BR"></i> | lks-elephantL-BR |  `u+F2BE` |  `<i class="ls lks-elephantL-BR"></i>`| <span class="display-text"></span> |
| <i class="lks lks-elephantR-BR"></i> | lks-elephantR-BR |  `u+F2BF` |  `<i class="ls lks-elephantR-BR"></i>`| <span class="display-text"></span> |
| <i class="lks lks-punkalasa"></i> | lks-punkalasa |  `u+F0A9` |  `<i class="ls lks-punkalasa"></i>`| <span class="display-text"></span> |
| <i class="lks lks-bahirawa-BR"></i> | lks-bahirawa-BR |  `u+F2C0` |  `<i class="ls lks-bahirawa-BR"></i>`| <span class="display-text"></span> |
| <i class="lks lks-walakul-BR"></i> | lks-walakul-BR |  `u+F6E9` |  `<i class="ls lks-walakul-BR"></i>`| <span class="display-text"></span> |
| <i class="lks lks-kambi-BR"></i> | lks-kambi-BR |  `u+F6E8` |  `<i class="ls lks-kambi-BR"></i>`| <span class="display-text"></span> |
| <i class="lks lks-tutuk"></i> | lks-tutuk |  `u+F4D6` |  `<i class="ls lks-tutuk"></i>`| <span class="display-text"></span> |
| <i class="lks lks-gov"></i> | lks-gov |  `u+EC81` |  `<i class="ls lks-gov"></i>`| <span class="display-text"></span> |


## About

This is free and open source project maintained by [Textual](http://textual.works) with the support form the community. See [CONTRIBUTORS](https://github.com/textualworks/lankasymbols/blob/master/)

### Unicode ranges
Project uses Unicode standard Private User Area. We have a simple guidelines on how we assign code points to symbols for now.

| RANGE     | DESCRIPTION                             | SAMPLE   |                                         
| :---      | :---                                    | :--- |
|`E000–E215`|	                                        | |           
|`E216–E42A`|	                                        | |
|`E42B–E63F`|	                                        | |
|`E640–E854`|	                                        | |
|`E855–EA69`|	                                        | |
|`EA6A–EC7E`|	                                        | |
|`EC7F–EE93`|	Official and brands                     | |         
|`EE94–F0A8`|	Typographic symbols                     | |                           
|`F0A9–F2BD`|	Historical cultural symbols             | |                             
|`F2BE–F4D2`|	Historical cultural symbols – Border    | |                             
|`F4D3–F6E7`|	Cultural symbols                        | |            
|`F6E8–F8FC`|	Cultural symbols – Borders              | |                 



## How to contribute

This is an open source project. If you would like to contribute by drawing a few symbols please get in touch on [Github issues](https://github.com/textualworks/lankasymbols/issues)
### RECOMMENDED: Draw using a font editor

- Fork the [Github project](https://github.com/textualworks/lankasymbols) or [download](https://github.com/textualworks/lankasymbols/archive/master.zip) the source files.
- Download [TruFont](http://trufont.github.io/), [FontForge](https://fontforge.github.io/en-US/) or any other font editor that can edit `.ufo` files.
- Open the `LankaSymbols.ufo` file inside `source/1-drawing`  with your font editor.
- Add a new glyph and name it `lks-<SOMETHING>` Look at existing names to get an idea.
- Draw your new symbol inside the glyph.
- Don't worry about the UNICODE value, maintainers will sort it out.

### Draw using a vector editor (Inkscape or Illustrator)

- Fork the [Github project](https://github.com/textualworks/lankasymbols) or [download](https://github.com/textualworks/lankasymbols/archive/master.zip) the source files.
- Find the template files inside `docs/templates`, make a copy of the file format and version that works for you.
- Rename the file `lks-<SOMETHING>` Look at existing symbol names to get an idea.
- Draw your new symbol. When you are ready to submit save the file as a `.eps` or `.svg`

### Submit with Github
- Submit your file using [Github issues](https://github.com/textualworks/lankasymbols/issues)
- Attach your `.ufo`, `.eps` or `.svg` file in the issue.
- Please include a description and an image of the actual symbol as well.
- Include your name and details, so we can assign credits to you:)

### Submit with git
- Send a pull request. Also include all the  info as above.




## LICENSE

This Font Software is licensed under the SIL Open Font License, Version 1.1. This license is available with a FAQ at: http://scripts.sil.org/OFL
