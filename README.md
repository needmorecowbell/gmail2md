# Obsidian Helper Script: Export Gmail Receipts

This script is used to help me take emails I label as receipts and load them into my [obsidian](https://obsidian.md) vault. This allows me to keep track of receipts in a relational way. 

## Usage

Edit the file to fit your needs, then run `python export_gmail_receipts.py` on a regular basis to keep your inbox synced to obsidian.

## Requirements

- python3

## Tips

- This file can (and should) be modified to fit your liking, receipts are just a useful example I used. 

- The template is formed to be compatible with the dataview plugin for obsidian so long as you have the inline attributes option enabled.

## Output

This is what a file might look like:

```markdown
---
tags: ['receipt','email']
aliases: []
---
    
# Your Electronic Receipt - The Home Depot <HomeDepot@order.homedepot.com>

-----------
**From**:: The Home Depot <HomeDepot@order.homedepot.com>
**To**::  
**Bcc**::
**Date**:: Apr D YYYY HH:MM PM
**Subject**:: Your Electronic Receipt

-----------

## Associations
- [[Big Construction Project]]
- [[Contractor]]
- [[Me]]

## Contents

**EML**:: [[Obsidian Attachments/DD-MM-YYY_THH_MM_Your Electronic Receipt.eml]]

**PDF Attachment**:: ![[Obsidian Attachments/DD-MM-YYY_THH_MM_Your Electronic Receipt.pdf]]
```


