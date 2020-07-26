from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

app = FastAPI(debug=True)
templates = Jinja2Templates("templates")

df: pd.DataFrame = sns.load_dataset('tips')


@app.get("/")
async def root(req: Request):
    return templates.TemplateResponse("index.html", 
    {
        'request': req,
        'mintip': 0,
        'df': df.to_html(classes=['table table-sm']),
    }
    )

@app.post("/")
async def root(req: Request, mintip: str = Form(...)):
    mintip = float(mintip)
    view = df.query("tip >= @mintip")
    sns.distplot(view.total_bill)
    plt.savefig("static/plot.png")
    plt.close()

    return templates.TemplateResponse("index.html", 
    {
        'request': req,
        'mintip': mintip,
        'df': view.to_html(classes=['table table-sm']),
        'fileName': 'plot.png',
    }
    )