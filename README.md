## LankaSymbols
LankaSymbols is a free and open source project maintained by [Mooniak](https://mooniak.com) with the support of the community. See [CONTRIBUTORS](https://github.com/mooniak/lankasymbols/blob/main/CONTRIBUTORS.md)

### How to use on desktop
- Download the [fonts](https://github.com/mooniak/lankasymbols/releases)
- Use the following chart to find the symbol you want to use and copy and paste the icon from TEXT column in the symbols chart.
- Or use the `Glyph` panel in your application to use any symbol.

### How to use on web (HTML)
Add the following inside `<head>` and use the correct string from the HTML column in the symbols chart below.
```
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/mooniak/lankasymbols@main/docs/webfonts/lankasymbols.css">
```
!IMPORTANT: This project is still in early development and things keep changing. Do not use for production websites.

### Unicode ranges
Project uses Unicode standard Private User Area. We have simple guidelines on how we assign code points to symbols for now.

| RANGE     | DESCRIPTION                             |
| :---      | :---                                    |
|`E000–E215`|	                                        |
|`E216–E42A`|	                                        |
|`E42B–E63F`|	                                        |
|`E640–E854`|	                                        |
|`E855–EA69`|	                                        |
|`EA6A–EC7E`|	                                        |
|`EC7F–EE93`|	Official and brands                     |
|`EE94–F0A8`|	Typographic symbols                     |
|`F0A9–F2BD`|	Historical cultural symbols             |
|`F2BE–F4D2`|	Historical cultural symbols – Border    |
|`F4D3–F6E7`|	Cultural symbols                        |
|`F6E8–F8FC`|	Cultural symbols – Borders              |

### How to contribute
This is an open source project. If you would like to contribute by drawing a few symbols please get in touch on [Github issues](https://github.com/mooniak/lankasymbols/issues)

#### Draw using a font editor [RECOMMENDED]
- Fork the [Github project](https://github.com/mooniak/lankasymbols) or [download](https://github.com/mooniak/lankasymbols/archive/main.zip) the source files.
- Download [TruFont](http://trufont.github.io/), [FontForge](https://fontforge.github.io/en-US/) or any other font editor that can edit `.ufo` files.
- Open the `LankaSymbols.ufo` file inside `sources/` with your font editor.
- Add a new glyph and name it `lks-<SOMETHING>` Look at existing names to get an idea.
- Draw your new symbol inside the glyph.
- Don't worry about the UNICODE value, maintainers will sort it out.

#### Draw using a vector editor (Inkscape or Illustrator)
- Fork the [Github project](https://github.com/mooniak/lankasymbols) or [download](https://github.com/mooniak/lankasymbols/archive/main.zip) the source files.
- Find the template files inside `docs/templates`, make a copy of the file format and version that works for you.
- Rename the file `lks-<SOMETHING>` Look at existing symbol names to get an idea.
- Draw your new symbol. When you are ready to submit save the file as a `.eps` or `.svg`

#### Submit with Github
- Submit your file using [Github issues](https://github.com/mooniak/lankasymbols/issues)
- Attach your `.ufo`, `.eps` or `.svg` file in the issue.
- Please include a description and an image of the actual symbol as well.
- Include your name and details, so we can assign credits to you:)

#### Submit with git
- Send a pull request. Also include all the info as above.

### Licence
This Font Software is licensed under the SIL Open Font License, Version 1.1. This license is available with a FAQ at: http://scripts.sil.org/OFL
