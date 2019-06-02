# StarPars CFG

A sentence generator trained on Star Wars opening crawls.

![Opening
Crawl](https://proxy.duckduckgo.com/iu/?u=http%3A%2F%2Fnerdist.com%2Fwp-content%2Fuploads%2F2016%2F12%2Fimages2Farticle2F20162F072F182Fanigif_enhanced-2824-1450724242-10.gif&f=1)

NTLK project for [taaltheorie en
taalverwerking](http://studiegids.uva.nl/xmlpages/page/2018-2019/zoek-vak/vak/62671).

The multiple sources that form the corpus can be found in the corpus itself:
[data/corpus.txt](data/corpus.txt).

### Generating sentences
```python
$ python3 -i starpars.py
>>> generate_sentences(CFG, sample_size=500, num=9000)
```

### Some generated sentences
- These daring spaceships can restore.
- This first knights will gather rescue.
- All evil ashes fly.
- These hutt reigns luke.
- This few fighters find this difficult planet.
- These dooku custodian swept canon sides to these send farmers more and more.
- When tyranny summers recently deploys that thousand kashyyyk it call majority, these underwater begun spaceships leaving the spell.
- Race more but more lines.
- Shipping from Organa's congress.
- To relax her probes, starfleet grievous sinister declared completed leadership.
- This evil troops more or more when there.
- This can shipping desperate bespin speeds, doom summers kidnapped unbeknownst to an mean victims.
- Group rebel number man no to save.

### License
Licensed under the [MIT license](LICENSE).

A project by [Yochem van Rosmalen](@yochem) and [Lysa Ngouteau](@lysa-n).
