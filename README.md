# 6box

The 6box is the wooden casing around the 6element sensor. You can find more information about 6element [here](https://medium.com/ants-blog/6element-534ffbe2a60f) and about the laser cutting part [here](https://medium.com/p/7c3efcb5c89f).

Here are the scripts that will generate the pdf needed to laser cut the 6box.

### Usage

You'll need to generate the field lines (yes my design includes the calculation of an electromagnic field and yes I use the real solution to draw the sides of the box):

```
python compute-field.py
```

that will solve Maxwell equations and output the field lines in `field.json`.
Then, you can use 

```
python make_6box.py
```

to generate the pdf. The code is straigthforward.

### Requirements

You'll need python, numpy, scipy, matplotlib and reportlab that can be installed via pip:

```
pip install reportlab
```

### Licence

MIT
