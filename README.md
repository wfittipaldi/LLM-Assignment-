# LLM Assignment - Craig

Link to [presentation](https://docs.google.com/presentation/d/1QqHcad7JCD3IZCV7FeXc7cvusLqQHAiUNhoUKpX7eRM/edit?usp=sharing)

## Author Information:

**Name(s)**: Curtis Barnhart, Will Fittipaldi, Levi Wicks
**Email(s)**: cbarnhart@westmont.edu, wfittipaldi@westmont.edu, lwicks@westmont.edu

## License Information

This project is licensed under the GNU General Public License v3.0 `GPL-3.0`.

## How To

First, make sure that you have valid [OpenAI API keys](https://platform.openai.com/docs/api-reference/authentication).

Craig is a really simple tool to use. Just run 

```
python main.py file.txt
```

from the terminal, where file.txt is the path to your inventory. 
Since our tool makes use of OpenAI's ChatGPT
API you must also provide a valid API key to make the necessary API calls. 

## Data Format Requirements

In order to use Craig your inventory data must be formatted correctly. 
It expects inventory data to be a plain text file with items 
separated by a horizontal line in Markdown ('---'). 


Example: 

```
*Vintage Wooden Dresser (4 Drawers)**  
**Price:** $75  
**Description:** A classic wooden 4-drawer dresser in good condition. It has a natural wood finish with a few minor scuff marks from age. The drawers open and close smoothly, and it’s perfect for adding rustic charm to any bedroom.

---

**Full-Sized Pool Table (Includes Cues & Balls)**  
**Price:** $200  
**Description:** A full-sized pool table with felt in great condition. Comes with a full set of cues, balls, and a rack. The table has some minor wear on the edges but is sturdy and ready for games.

---

```

## Citations

 - [Open AI Doc Reference](https://platform.openai.com/docs/api-reference/introduction)

